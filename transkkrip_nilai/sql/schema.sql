-- Create grades table
CREATE TABLE grades (
    id SERIAL PRIMARY KEY,
    student_id VARCHAR(20) NOT NULL,
    course_code VARCHAR(10) NOT NULL,
    course_name VARCHAR(100) NOT NULL,
    sks INTEGER NOT NULL,
    grade VARCHAR(2) NOT NULL,
    semester INTEGER NOT NULL,
    academic_year VARCHAR(10) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create grade_history table for auditing changes
CREATE TABLE grade_history (
    id SERIAL PRIMARY KEY,
    grade_id INTEGER NOT NULL REFERENCES grades(id),
    old_value VARCHAR(2),
    new_value VARCHAR(2) NOT NULL,
    changed_by VARCHAR(50) NOT NULL,
    changed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    reason TEXT
);

-- Create students table for biodata
CREATE TABLE students (
    nim VARCHAR(20) PRIMARY KEY,
    nama VARCHAR(100) NOT NULL,
    program_studi VARCHAR(100) NOT NULL,
    angkatan INTEGER NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Indexes for better performance
CREATE INDEX idx_grades_student_id ON grades(student_id);
CREATE INDEX idx_grades_course_code ON grades(course_code);
CREATE INDEX idx_grade_history_grade_id ON grade_history(grade_id);
CREATE INDEX idx_grade_history_changed_at ON grade_history(changed_at);
