-- Trigger function for auditing grade changes
CREATE OR REPLACE FUNCTION audit_grade_changes()
RETURNS TRIGGER AS $$
BEGIN
    -- Only log if grade actually changed
    IF OLD.grade != NEW.grade THEN
        INSERT INTO grade_history (
            grade_id,
            old_value,
            new_value,
            changed_by,
            reason
        ) VALUES (
            NEW.id,
            OLD.grade,
            NEW.grade,
            COALESCE(current_setting('app.current_user', true), 'system'),
            COALESCE(current_setting('app.change_reason', true), 'Grade update')
        );
    END IF;

    -- Update the updated_at timestamp
    NEW.updated_at = CURRENT_TIMESTAMP;

    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- Create trigger on grades table
CREATE TRIGGER grades_audit_trigger
    BEFORE UPDATE ON grades
    FOR EACH ROW
    EXECUTE FUNCTION audit_grade_changes();

-- Function to set audit context (optional, for tracking who made changes)
CREATE OR REPLACE FUNCTION set_audit_context(
    p_user VARCHAR(50) DEFAULT 'system',
    p_reason TEXT DEFAULT 'Grade update'
)
RETURNS VOID AS $$
BEGIN
    PERFORM set_config('app.current_user', p_user, false);
    PERFORM set_config('app.change_reason', p_reason, false);
END;
$$ LANGUAGE plpgsql;
