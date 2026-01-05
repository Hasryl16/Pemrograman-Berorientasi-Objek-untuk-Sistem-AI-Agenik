-- View for grade change history per student
CREATE OR REPLACE VIEW student_grade_history AS
SELECT
    s.nim,
    s.nama,
    g.course_code,
    g.course_name,
    g.semester,
    g.academic_year,
    gh.old_value,
    gh.new_value,
    gh.changed_by,
    gh.changed_at,
    gh.reason
FROM
    students s
JOIN
    grades g ON s.nim = g.student_id
JOIN
    grade_history gh ON g.id = gh.grade_id
ORDER BY
    s.nim, gh.changed_at DESC;

-- View for current grades per student
CREATE OR REPLACE VIEW student_current_grades AS
SELECT
    s.nim,
    s.nama,
    s.program_studi,
    s.angkatan,
    g.course_code,
    g.course_name,
    g.sks,
    g.grade,
    g.semester,
    g.academic_year
FROM
    students s
LEFT JOIN
    grades g ON s.nim = g.student_id
ORDER BY
    s.nim, g.semester, g.course_code;
