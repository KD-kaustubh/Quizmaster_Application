from app import app, db
from backend.models import User, Subject, Chapter, Quiz, Question
from datetime import datetime, date, time

def seed_data():
    with app.app_context():
        print("Starting seed...")

        # ─── USERS ──────────────────────────────────────────────────
        if User.query.count() == 0:
            admin = User(
                username='admin@gmail.com',
                full_name='Admin User',
                qualification='Administrator',
                dob=date(2000, 1, 1),
                role=0
            )
            admin.set_password('Admin123')

            student = User(
                username='student@gmail.com',
                full_name='Student User',
                qualification='B.Tech',
                dob=date(2002, 5, 15),
                role=1
            )
            student.set_password('Student123')

            db.session.add_all([admin, student])
            db.session.commit()
            print("  Added: admin and student users")
        else:
            print("  Users already exist, skipping.")

        # ─── SUBJECTS ───────────────────────────────────────────────
        subjects_data = [
            {"name": "Mathematics",  "description": "Algebra, calculus, and number theory"},
            {"name": "Science",      "description": "Physics, chemistry, and biology basics"},
            {"name": "Programming",  "description": "Python, data structures, and algorithms"},
        ]

        for s in subjects_data:
            if not Subject.query.filter_by(name=s["name"]).first():
                db.session.add(Subject(name=s["name"], description=s["description"]))
                print(f"  Added subject: {s['name']}")
        db.session.commit()

        # ─── CHAPTERS ───────────────────────────────────────────────
        chapters_data = [
            {"name": "Algebra",          "description": "Linear equations and polynomials",     "subject": "Mathematics"},
            {"name": "Calculus",         "description": "Differentiation and integration",       "subject": "Mathematics"},
            {"name": "Physics",          "description": "Motion, forces, and energy",            "subject": "Science"},
            {"name": "Chemistry",        "description": "Elements, compounds, and reactions",    "subject": "Science"},
            {"name": "Python Basics",    "description": "Variables, loops, and functions",       "subject": "Programming"},
            {"name": "Data Structures",  "description": "Lists, stacks, queues, and trees",      "subject": "Programming"},
        ]

        for c in chapters_data:
            subj = Subject.query.filter_by(name=c["subject"]).first()
            if not Chapter.query.filter_by(name=c["name"], subject_id=subj.id).first():
                db.session.add(Chapter(name=c["name"], description=c["description"], subject_id=subj.id))
                print(f"  Added chapter: {c['name']}")
        db.session.commit()

        # ─── QUIZZES ────────────────────────────────────────────────
        quizzes_data = [
            {"name": "Algebra Basics Quiz",      "chapter": "Algebra",         "date": date(2026, 4, 1),  "duration": time(0, 15), "remarks": "Basic algebra quiz covering equations"},
            {"name": "Algebra Advanced Quiz",    "chapter": "Algebra",         "date": date(2026, 4, 10), "duration": time(0, 20), "remarks": "Advanced algebra with polynomials"},
            {"name": "Differentiation Quiz",     "chapter": "Calculus",        "date": date(2026, 4, 5),  "duration": time(0, 20), "remarks": "Quiz on basic differentiation rules"},
            {"name": "Integration Quiz",         "chapter": "Calculus",        "date": date(2026, 4, 15), "duration": time(0, 25), "remarks": "Quiz on integration techniques"},
            {"name": "Motion and Forces Quiz",   "chapter": "Physics",         "date": date(2026, 4, 3),  "duration": time(0, 15), "remarks": "Newton laws and motion"},
            {"name": "Energy and Work Quiz",     "chapter": "Physics",         "date": date(2026, 4, 12), "duration": time(0, 20), "remarks": "Work, energy and power"},
            {"name": "Periodic Table Quiz",      "chapter": "Chemistry",       "date": date(2026, 4, 6),  "duration": time(0, 15), "remarks": "Elements and periodic table"},
            {"name": "Chemical Reactions Quiz",  "chapter": "Chemistry",       "date": date(2026, 4, 18), "duration": time(0, 20), "remarks": "Types of chemical reactions"},
            {"name": "Python Variables Quiz",    "chapter": "Python Basics",   "date": date(2026, 4, 2),  "duration": time(0, 15), "remarks": "Variables, data types and operators"},
            {"name": "Python Loops Quiz",        "chapter": "Python Basics",   "date": date(2026, 4, 11), "duration": time(0, 20), "remarks": "For loops, while loops and functions"},
            {"name": "Lists and Stacks Quiz",    "chapter": "Data Structures", "date": date(2026, 4, 7),  "duration": time(0, 20), "remarks": "Arrays, lists and stack operations"},
            {"name": "Trees and Graphs Quiz",    "chapter": "Data Structures", "date": date(2026, 4, 20), "duration": time(0, 25), "remarks": "Binary trees and graph traversal"},
        ]

        for q in quizzes_data:
            chap = Chapter.query.filter_by(name=q["chapter"]).first()
            if not Quiz.query.filter_by(name=q["name"], chapter_id=chap.id).first():
                db.session.add(Quiz(
                    name=q["name"],
                    chapter_id=chap.id,
                    date_of_quiz=q["date"],
                    time_duration=q["duration"],
                    remarks=q["remarks"]
                ))
                print(f"  Added quiz: {q['name']}")
        db.session.commit()

        # ─── QUESTIONS ──────────────────────────────────────────────
        questions_data = [
            # Algebra Basics Quiz
            {"quiz": "Algebra Basics Quiz", "statement": "What is the value of x in 2x + 4 = 10?",     "o1": "2",           "o2": "3",              "o3": "4",          "o4": "5",            "answer": "3"},
            {"quiz": "Algebra Basics Quiz", "statement": "Simplify: 3x + 2x",                           "o1": "5x",          "o2": "6x",             "o3": "x",          "o4": "5x2",          "answer": "5x"},
            {"quiz": "Algebra Basics Quiz", "statement": "What is the slope of y = 3x + 2?",            "o1": "2",           "o2": "3",              "o3": "1",          "o4": "0",            "answer": "3"},
            {"quiz": "Algebra Basics Quiz", "statement": "Solve: x squared = 16",                       "o1": "2",           "o2": "4",              "o3": "8",          "o4": "16",           "answer": "4"},
            # Algebra Advanced Quiz
            {"quiz": "Algebra Advanced Quiz", "statement": "Factor: x2 - 5x + 6",                       "o1": "(x-2)(x-3)",  "o2": "(x+2)(x+3)",     "o3": "(x-1)(x-6)", "o4": "(x-2)(x+3)",   "answer": "(x-2)(x-3)"},
            {"quiz": "Algebra Advanced Quiz", "statement": "What are the roots of x2 - 4 = 0?",         "o1": "2 and -2",    "o2": "4 and -4",       "o3": "1 and -1",   "o4": "2 and 0",      "answer": "2 and -2"},
            {"quiz": "Algebra Advanced Quiz", "statement": "Expand: (x + 3) squared",                   "o1": "x2+6x+9",     "o2": "x2+3x+9",        "o3": "x2+9",       "o4": "x2+6x+6",      "answer": "x2+6x+9"},
            {"quiz": "Algebra Advanced Quiz", "statement": "If f(x) = 2x + 1, find f(3)",               "o1": "5",           "o2": "6",              "o3": "7",          "o4": "8",            "answer": "7"},
            # Differentiation Quiz
            {"quiz": "Differentiation Quiz", "statement": "What is the derivative of x squared?",       "o1": "x",           "o2": "2x",             "o3": "2",          "o4": "x2",           "answer": "2x"},
            {"quiz": "Differentiation Quiz", "statement": "Differentiate: 3x cubed",                    "o1": "3x2",         "o2": "9x2",            "o3": "6x",         "o4": "9x",           "answer": "9x2"},
            {"quiz": "Differentiation Quiz", "statement": "What is d/dx of a constant?",                "o1": "1",           "o2": "the constant",   "o3": "0",          "o4": "undefined",    "answer": "0"},
            {"quiz": "Differentiation Quiz", "statement": "Derivative of sin(x) is?",                   "o1": "-cos(x)",     "o2": "cos(x)",         "o3": "tan(x)",     "o4": "-sin(x)",      "answer": "cos(x)"},
            # Integration Quiz
            {"quiz": "Integration Quiz", "statement": "Integrate: 2x dx",                               "o1": "x + C",       "o2": "2x2 + C",        "o3": "x2 + C",     "o4": "2 + C",        "answer": "x2 + C"},
            {"quiz": "Integration Quiz", "statement": "What is the integral of 1 dx?",                  "o1": "0",           "o2": "x + C",          "o3": "1 + C",      "o4": "x",            "answer": "x + C"},
            {"quiz": "Integration Quiz", "statement": "Integrate: cos(x) dx",                           "o1": "-sin(x)+C",   "o2": "sin(x)+C",       "o3": "tan(x)+C",   "o4": "-cos(x)+C",    "answer": "sin(x)+C"},
            {"quiz": "Integration Quiz", "statement": "Evaluate integral from 0 to 1 of x dx",         "o1": "0",           "o2": "1",              "o3": "0.5",        "o4": "2",            "answer": "0.5"},
            # Motion and Forces Quiz
            {"quiz": "Motion and Forces Quiz", "statement": "Newton's first law is also called?",       "o1": "Law of acceleration", "o2": "Law of inertia", "o3": "Law of action", "o4": "Law of gravity", "answer": "Law of inertia"},
            {"quiz": "Motion and Forces Quiz", "statement": "Unit of force is?",                        "o1": "Joule",       "o2": "Watt",           "o3": "Newton",     "o4": "Pascal",       "answer": "Newton"},
            {"quiz": "Motion and Forces Quiz", "statement": "F=ma. If m=5kg, a=3m/s2, F=?",            "o1": "8 N",         "o2": "15 N",           "o3": "2 N",        "o4": "10 N",         "answer": "15 N"},
            {"quiz": "Motion and Forces Quiz", "statement": "Speed is a ___ quantity.",                 "o1": "vector",      "o2": "scalar",         "o3": "tensor",     "o4": "none",         "answer": "scalar"},
            # Energy and Work Quiz
            {"quiz": "Energy and Work Quiz", "statement": "Unit of energy is?",                         "o1": "Newton",      "o2": "Watt",           "o3": "Joule",      "o4": "Pascal",       "answer": "Joule"},
            {"quiz": "Energy and Work Quiz", "statement": "Work = Force x ?",                           "o1": "Mass",        "o2": "Time",           "o3": "Displacement","o4": "Velocity",    "answer": "Displacement"},
            {"quiz": "Energy and Work Quiz", "statement": "Kinetic energy formula is?",                 "o1": "mgh",         "o2": "half mv2",       "o3": "mv",         "o4": "Fxd",          "answer": "half mv2"},
            {"quiz": "Energy and Work Quiz", "statement": "Power is defined as?",                       "o1": "Work x Time", "o2": "Work / Time",    "o3": "Force x Time","o4": "Energy x Mass","answer": "Work / Time"},
            # Periodic Table Quiz
            {"quiz": "Periodic Table Quiz", "statement": "What is the symbol for Gold?",                "o1": "Go",          "o2": "Gd",             "o3": "Au",         "o4": "Ag",           "answer": "Au"},
            {"quiz": "Periodic Table Quiz", "statement": "Atomic number of Carbon is?",                 "o1": "6",           "o2": "12",             "o3": "8",          "o4": "4",            "answer": "6"},
            {"quiz": "Periodic Table Quiz", "statement": "Which is the lightest element?",              "o1": "Helium",      "o2": "Oxygen",         "o3": "Hydrogen",   "o4": "Lithium",      "answer": "Hydrogen"},
            {"quiz": "Periodic Table Quiz", "statement": "Noble gases are in group?",                   "o1": "1",           "o2": "7",              "o3": "18",         "o4": "2",            "answer": "18"},
            # Chemical Reactions Quiz
            {"quiz": "Chemical Reactions Quiz", "statement": "H2 + O2 produces?",                       "o1": "HO",          "o2": "H2O",            "o3": "H2O2",       "o4": "HO2",          "answer": "H2O"},
            {"quiz": "Chemical Reactions Quiz", "statement": "Acid + Base produces?",                   "o1": "Acid",        "o2": "Base",           "o3": "Salt + Water","o4": "Gas",         "answer": "Salt + Water"},
            {"quiz": "Chemical Reactions Quiz", "statement": "What type of reaction is burning?",       "o1": "Endothermic", "o2": "Exothermic",     "o3": "Neutralization","o4": "Decomposition","answer": "Exothermic"},
            {"quiz": "Chemical Reactions Quiz", "statement": "pH of pure water is?",                    "o1": "0",           "o2": "14",             "o3": "7",          "o4": "1",            "answer": "7"},
            # Python Variables Quiz
            {"quiz": "Python Variables Quiz", "statement": "What is the output of type(10)?",           "o1": "float",       "o2": "str",            "o3": "int",        "o4": "bool",         "answer": "int"},
            {"quiz": "Python Variables Quiz", "statement": "Which is a valid variable name?",           "o1": "2name",       "o2": "my-var",         "o3": "my_var",     "o4": "my var",       "answer": "my_var"},
            {"quiz": "Python Variables Quiz", "statement": "What does len('hello') return?",            "o1": "4",           "o2": "5",              "o3": "6",          "o4": "0",            "answer": "5"},
            {"quiz": "Python Variables Quiz", "statement": "Which operator is used for exponentiation?","o1": "^",           "o2": "**",             "o3": "//",         "o4": "%",            "answer": "**"},
            # Python Loops Quiz
            {"quiz": "Python Loops Quiz", "statement": "What does range(3) produce?",                   "o1": "1,2,3",       "o2": "0,1,2,3",        "o3": "0,1,2",      "o4": "1,2",          "answer": "0,1,2"},
            {"quiz": "Python Loops Quiz", "statement": "Which keyword exits a loop?",                   "o1": "exit",        "o2": "stop",           "o3": "break",      "o4": "end",          "answer": "break"},
            {"quiz": "Python Loops Quiz", "statement": "What is the output of print(2**3)?",            "o1": "6",           "o2": "9",              "o3": "8",          "o4": "5",            "answer": "8"},
            {"quiz": "Python Loops Quiz", "statement": "def keyword is used to?",                       "o1": "define a variable","o2": "define a function","o3": "define a class","o4": "delete a variable","answer": "define a function"},
            # Lists and Stacks Quiz
            {"quiz": "Lists and Stacks Quiz", "statement": "Which method adds an element to a list?",   "o1": "add()",       "o2": "insert()",       "o3": "append()",   "o4": "push()",       "answer": "append()"},
            {"quiz": "Lists and Stacks Quiz", "statement": "Stack follows which principle?",            "o1": "FIFO",        "o2": "LIFO",           "o3": "LILO",       "o4": "FILO",         "answer": "LIFO"},
            {"quiz": "Lists and Stacks Quiz", "statement": "Index of first element in a list is?",      "o1": "1",           "o2": "-1",             "o3": "0",          "o4": "None",         "answer": "0"},
            {"quiz": "Lists and Stacks Quiz", "statement": "Which removes last element from a list?",   "o1": "remove()",    "o2": "delete()",       "o3": "pop()",      "o4": "clear()",      "answer": "pop()"},
            # Trees and Graphs Quiz
            {"quiz": "Trees and Graphs Quiz", "statement": "Root node has how many parents?",           "o1": "1",           "o2": "2",              "o3": "0",          "o4": "depends",      "answer": "0"},
            {"quiz": "Trees and Graphs Quiz", "statement": "BFS uses which data structure?",            "o1": "Stack",       "o2": "Queue",          "o3": "Array",      "o4": "Tree",         "answer": "Queue"},
            {"quiz": "Trees and Graphs Quiz", "statement": "DFS uses which data structure?",            "o1": "Queue",       "o2": "Heap",           "o3": "Stack",      "o4": "Array",        "answer": "Stack"},
            {"quiz": "Trees and Graphs Quiz", "statement": "A binary tree node has at most how many children?", "o1": "1", "o2": "2",              "o3": "3",          "o4": "unlimited",    "answer": "2"},
        ]

        for q in questions_data:
            quiz = Quiz.query.filter_by(name=q["quiz"]).first()
            if quiz and not Question.query.filter_by(question_statement=q["statement"], quiz_id=quiz.id).first():
                db.session.add(Question(
                    quiz_id=quiz.id,
                    question_statement=q["statement"],
                    option1=q["o1"],
                    option2=q["o2"],
                    option3=q["o3"],
                    option4=q["o4"],
                    correct_answer=q["answer"]
                ))
        db.session.commit()
        print("  Added all questions.")

        print("\n Seed complete!")
        print("   Subjects : 3")
        print("   Chapters : 6")
        print("   Quizzes  : 12")
        print("   Questions: 48")
        print("\n   Login credentials:")
        print("   Admin   -> admin@gmail.com   / Admin123")
        print("   Student -> student@gmail.com / Student123")


if __name__ == '__main__':
    seed_data()