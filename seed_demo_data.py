from datetime import date, datetime, time, timedelta

from backend.models import Chapter, Question, Quiz, Score, Subject, User, db


def get_or_create_user(username, full_name, qualification, dob, role, password):
    user = User.query.filter_by(username=username).first()
    if not user:
        user = User(
            username=username,
            full_name=full_name,
            qualification=qualification,
            dob=dob,
            role=role,
        )
        user.set_password(password)
        db.session.add(user)
        db.session.flush()
    return user


def get_or_create_subject(name, description):
    subject = Subject.query.filter_by(name=name).first()
    if not subject:
        subject = Subject(name=name, description=description)
        db.session.add(subject)
        db.session.flush()
    return subject


def get_or_create_chapter(subject_id, name, description):
    chapter = Chapter.query.filter_by(subject_id=subject_id, name=name).first()
    if not chapter:
        chapter = Chapter(subject_id=subject_id, name=name, description=description)
        db.session.add(chapter)
        db.session.flush()
    return chapter


def get_or_create_quiz(chapter_id, name, quiz_date, duration, remarks):
    quiz = Quiz.query.filter_by(chapter_id=chapter_id, name=name).first()
    if not quiz:
        quiz = Quiz(
            chapter_id=chapter_id,
            name=name,
            date_of_quiz=quiz_date,
            time_duration=duration,
            remarks=remarks,
        )
        db.session.add(quiz)
        db.session.flush()
    return quiz


def add_question_if_missing(quiz_id, statement, option1, option2, option3, option4, correct):
    exists = Question.query.filter_by(quiz_id=quiz_id, question_statement=statement).first()
    if not exists:
        db.session.add(
            Question(
                quiz_id=quiz_id,
                question_statement=statement,
                option1=option1,
                option2=option2,
                option3=option3,
                option4=option4,
                correct_answer=correct,
            )
        )


def seed_demo_data():
    admin = get_or_create_user(
        "admin@gmail.com", "Admin User", "Administrator", date(2000, 1, 1), 0, "Admin123"
    )
    student = get_or_create_user(
        "student@gmail.com", "Student User", "B.Tech", date(2002, 5, 15), 1, "Student123"
    )
    tester = get_or_create_user(
        "user1@gmail.com", "Test User One", "B.Sc Computer Science", date(2001, 9, 21), 1, "User12345"
    )

    math = get_or_create_subject("Mathematics", "Core quantitative aptitude and problem solving")
    science = get_or_create_subject("Science", "General science concepts and fundamentals")

    algebra = get_or_create_chapter(math.id, "Algebra", "Linear equations, identities, and simplification")
    geometry = get_or_create_chapter(math.id, "Geometry", "Shapes, areas, angles, and theorems")
    physics = get_or_create_chapter(science.id, "Physics Basics", "Motion, force, and units")

    today = date.today()
    quiz_1 = get_or_create_quiz(
        algebra.id,
        "Algebra Basics Quiz",
        today - timedelta(days=3),
        time(0, 20),
        "Beginner algebra assessment",
    )
    quiz_2 = get_or_create_quiz(
        geometry.id,
        "Geometry Quick Test",
        today,
        time(0, 15),
        "Basic geometry questions",
    )
    quiz_3 = get_or_create_quiz(
        physics.id,
        "Physics Fundamentals",
        today + timedelta(days=2),
        time(0, 25),
        "Intro physics concepts",
    )

    add_question_if_missing(quiz_1.id, "What is 2x + 3 when x = 4?", "8", "9", "10", "11", "11")
    add_question_if_missing(quiz_1.id, "Solve: 3x = 21", "5", "6", "7", "8", "7")
    add_question_if_missing(
        quiz_1.id,
        "Value of (a+b)^2 includes?",
        "a^2 + b^2",
        "a^2 + 2ab + b^2",
        "2a + 2b",
        "a^2 - b^2",
        "a^2 + 2ab + b^2",
    )

    add_question_if_missing(quiz_2.id, "Sum of angles in a triangle?", "90", "120", "180", "360", "180")
    add_question_if_missing(quiz_2.id, "A square has how many equal sides?", "2", "3", "4", "5", "4")

    add_question_if_missing(quiz_3.id, "SI unit of force?", "Joule", "Pascal", "Newton", "Watt", "Newton")
    add_question_if_missing(
        quiz_3.id,
        "Acceleration due to gravity on Earth (~)?",
        "9.8 m/s^2",
        "8.9 m/s^2",
        "10.8 m/s^2",
        "7.8 m/s^2",
        "9.8 m/s^2",
    )

    if Score.query.filter_by(user_id=student.id).count() == 0:
        db.session.add(
            Score(
                quiz_id=quiz_1.id,
                user_id=student.id,
                time_stamp_of_attempt=datetime.now() - timedelta(days=2),
                total_score=2,
            )
        )
        db.session.add(
            Score(
                quiz_id=quiz_2.id,
                user_id=student.id,
                time_stamp_of_attempt=datetime.now() - timedelta(days=1),
                total_score=2,
            )
        )

    if Score.query.filter_by(user_id=tester.id).count() == 0:
        db.session.add(
            Score(
                quiz_id=quiz_1.id,
                user_id=tester.id,
                time_stamp_of_attempt=datetime.now() - timedelta(days=4),
                total_score=3,
            )
        )

    db.session.commit()
    print("SEED_COMPLETE")
    print(
        "Users: "
        f"{User.query.count()} | Subjects: {Subject.query.count()} | Chapters: {Chapter.query.count()} | "
        f"Quizzes: {Quiz.query.count()} | Questions: {Question.query.count()} | Scores: {Score.query.count()}"
    )


if __name__ == "__main__":
    from app import app

    with app.app_context():
        seed_demo_data()