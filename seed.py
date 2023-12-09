from faker import Faker
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Student, Group, Teacher, Discipline, Grade
from sqlalchemy.exc import IntegrityError
import random

# Підключення до бази даних
engine = create_engine('postgresql://postgres:14021992@localhost:5432/postgres')
Session = sessionmaker(bind=engine)
session = Session()


fake = Faker('uk_UA')

# Створення студентів
def create_students(num_students):
    for _ in range(num_students):
        student = Student(fullname=fake.name())
        session.add(student)

# Створення груп
def create_groups(num_groups):
    for i in range(1, num_groups + 1):
        group = Group(name=f'Group {i}')
        session.add(group)

# Створення викладачів
def create_teachers(num_teachers):
    for _ in range(num_teachers):
        teacher = Teacher(fullname=fake.name())
        session.add(teacher)

# Створення предметів
def create_disciplines(num_disciplines):
    disciplines = ['Mathematics', 'Physics', 'Biology', 'Chemistry', 'History', 'Literature', 'Programming']
    for _ in range(num_disciplines):
        discipline = Discipline(name=random.choice(disciplines))
        session.add(discipline)

# Створення оцінок
def create_grades(num_grades):
    students = session.query(Student).all()
    disciplines = session.query(Discipline).all()
    for _ in range(num_grades):
        student = random.choice(students)
        discipline = random.choice(disciplines)
        grade = Grade(grade=random.randint(1, 10),
                      date_received=fake.date_between(start_date='-1y'),
                      student=student,
                      discipline=discipline)
        session.add(grade)

# Генерація
create_students(50)
create_groups(3)
create_teachers(5)
create_disciplines(8)
create_grades(20)

# Збереження у базі
try:
    session.commit()
except IntegrityError as e:
    print(f"IntegrityError: {e}")
    session.rollback()
finally:
    session.close()
