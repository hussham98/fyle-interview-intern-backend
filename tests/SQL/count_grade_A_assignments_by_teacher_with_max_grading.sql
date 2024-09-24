SELECT COUNT(grade) AS grade_A_count
FROM assignments
WHERE grade = 'A'
AND teacher_id = :teacher_id;
