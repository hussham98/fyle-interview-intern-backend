import random
from sqlalchemy import text

from core import db
from core.models.assignments import Assignment, AssignmentStateEnum, GradeEnum


def create_n_graded_assignments_for_teacher(number: int = 0, teacher_id: int = 1) -> int:
    """
    Creates 'n' graded assignments for a specified teacher and returns the count of assignments with grade 'A'.

    Parameters:
    - number (int): The number of assignments to be created.
    - teacher_id (int): The ID of the teacher for whom the assignments are created.

    Returns:
    - int: Count of assignments with grade 'A'.
    """
    # Count existing assignments with grade 'A' for the specified teacher
    initial_grade_a_count: int = Assignment.filter(
        Assignment.teacher_id == teacher_id,
        Assignment.grade == GradeEnum.A
    ).count()

    # Create 'n' graded assignments
    for _ in range(number):
        # Randomly select a grade from GradeEnum
        grade = random.choice(list(GradeEnum))

        # Create and add a new Assignment instance
        assignment = Assignment(
            teacher_id=teacher_id,
            student_id=1,  # You may want to make this parameterized in the future
            grade=grade,
            content='test content',
            state=AssignmentStateEnum.GRADED
        )
        db.session.add(assignment)

    # Commit changes to the database
    db.session.commit()

    # Count and return the updated number of assignments with grade 'A'
    final_grade_a_count = Assignment.filter(
        Assignment.teacher_id == teacher_id,
        Assignment.grade == GradeEnum.A
    ).count()
    return final_grade_a_count - initial_grade_a_count


def test_get_assignments_in_graded_state_for_each_student():
    """Test to get graded assignments for each student."""
    # Update the state of assignments for student 1 to 'GRADED'
    submitted_assignments = Assignment.filter(Assignment.student_id == 1)

    for assignment in submitted_assignments:
        assignment.state = AssignmentStateEnum.GRADED

    db.session.commit()  # Commit changes to the database

    # Execute the SQL query to fetch the count of graded assignments
    with open('tests/SQL/number_of_graded_assignments_for_each_student.sql', encoding='utf8') as fo:
        sql = fo.read()

    sql_result = db.session.execute(text(sql)).fetchall()
    expected_result = [(1, len(submitted_assignments))]  # Adjust this based on your test setup

    for result in expected_result:
        assert result[0] == sql_result[0][0]
        assert result[1] == sql_result[0][1]


def test_get_grade_A_assignments_for_teacher_with_max_grading():
    """Test to get count of grade A assignments for the teacher who has graded the most assignments."""
    # Read the SQL query from a file
    with open('tests/SQL/count_grade_A_assignments_by_teacher_with_max_grading.sql', encoding='utf8') as fo:
        sql = fo.read()

    # Create and grade assignments for teachers
    grade_a_count_1 = create_n_graded_assignments_for_teacher(5, 1)
    sql_result_1 = db.session.execute(text(sql), {'teacher_id': 1}).fetchall()
    assert grade_a_count_1 == sql_result_1[0][0]

    grade_a_count_2 = create_n_graded_assignments_for_teacher(10, 2)
    sql_result_2 = db.session.execute(text(sql), {'teacher_id': 2}).fetchall()
    assert grade_a_count_2 == sql_result_2[0][0]
