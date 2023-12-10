from sqlalchemy import func
from models import Student, Group, Teacher, Discipline, Grade
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine

engine = create_engine('postgresql://postgres:14021992@localhost:5432/migrations')
Session = sessionmaker(bind=engine)
session = Session()

# 1. Знайти 5 студентів із найбільшим середнім балом з усіх предметів
def select_1():
    students_avg = session.query(Student, func.avg(Grade.grade).label('avg_grade')) \
        .join(Grade).group_by(Student.id).order_by(func.avg(Grade.grade).desc()).limit(5).all()
    return students_avg

# 2. Знайти студента із найвищим середнім балом з певного предмета
def select_2(subject):
    student_highest_avg = session.query(Student, func.avg(Grade.grade).label('avg_grade')) \
        .join(Grade).join(Discipline).filter(Discipline.name == subject) \
        .group_by(Student.id).order_by(func.avg(Grade.grade).desc()).first()
    return student_highest_avg

# 3. Знайти середній бал у групах з певного предмета
def select_3(subject):
    groups_avg = session.query(Group.name, func.avg(Grade.grade).label('avg_grade')) \
        .join(Student).join(Grade).join(Discipline).filter(Discipline.name == subject) \
        .group_by(Group.name).all()
    return groups_avg

# 4. Знайти середній бал на потоці (по всій таблиці оцінок)
def select_4():
    overall_avg = session.query(func.avg(Grade.grade).label('overall_avg')).scalar()
    return overall_avg

# 5. Знайти які курси читає певний викладач
def select_5(teacher_id):
    teacher_courses = session.query(Discipline.name).join(Teacher).filter(Teacher.id == teacher_id).all()
    return teacher_courses

# 6. Знайти список студентів у певній групі
def select_6(group_name):
    group_students = session.query(Student).join(Group).filter(Group.name == group_name).all()
    return group_students

# 7. Знайти оцінки студентів у окремій групі з певного предмета
def select_7(group_name, subject):
    group_grades = session.query(Student, Grade) \
        .join(Grade).join(Discipline).join(Group) \
        .filter(Group.name == group_name, Discipline.name == subject).all()
    return group_grades

# 8. Знайти середній бал, який ставить певний викладач зі своїх предметів
def select_8(teacher_id):
    teacher_avg_grade = session.query(func.avg(Grade.grade).label('avg_grade')) \
        .join(Discipline).join(Teacher).filter(Teacher.id == teacher_id).scalar()
    return teacher_avg_grade

# 9. Знайти список курсів, які відвідує певний студент
def select_9(student_id):
    student_courses = session.query(Discipline.name).join(Grade).join(Student) \
        .filter(Student.id == student_id).distinct().all()
    return student_courses

# 10. Список курсів, які певному студенту читає певний викладач
def select_10(student_id, teacher_id):
    student_teacher_courses = session.query(Discipline.name).join(Grade).join(Student).join(Teacher) \
        .filter(Student.id == student_id, Teacher.id == teacher_id).distinct().all()
    return student_teacher_courses



if __name__ == "__main__":
    result_1 = select_1(session)
    print("Select 1 Result:", result_1)

    result_2 = select_2(session, 'Mathematics')
    print("Select 2 Result:", result_2)

    result_3 = select_3(session, 'Physics')
    print("Select 3 Result:", result_3)

    result_5 = select_5(session, teacher_id=1)
    print("Select 5 Result:", result_5)

    result_6 = select_6(session, 'GroupA')
    print("Select 6 Result:", result_6)

    result_7 = select_7(session, 'GroupB', 'Mathematics')
    print("Select 7 Result:", result_7)

    result_8 = select_8(session, teacher_id=2)
    print("Select 8 Result:", result_8)

    result_9 = select_9(session, student_id=3)
    print("Select 9 Result:", result_9)

    result_10 = select_10(session, student_id=4, teacher_id=1)
    print("Select 10 Result:", result_10)