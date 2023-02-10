import os
import sqlite3

# poistaa tietokannan alussa (kätevä moduulin testailussa)
os.remove("courses.db")

db = sqlite3.connect("courses.db")
db.isolation_level = None

# luo tietokantaan tarvittavat taulut


def create_tables():
    db.execute("CREATE TABLE Teachers (\
        id INTEGER PRIMARY KEY, \
        name TEXT)")
    db.execute("CREATE TABLE Courses (\
        id INTEGER PRIMARY KEY, \
        name TEXT, \
        credits INTEGER )")
    db.execute("CREATE TABLE CourseTeachers (\
        id INTEGER PRIMARY KEY, \
        teacher_id INTEGER REFERENCES Teachers , \
        course_id INTEGER REFERENCES Courses)")
    db.execute("CREATE TABLE Students (\
        id INTEGER PRIMARY KEY, \
        name TEXT)")
    db.execute("CREATE TABLE Credits (\
        id INTEGER PRIMARY KEY,\
        student_id INTEGER REFERENCES Students,\
        course_id INTEGER REFERENCES Courses,\
        date DATE,\
        grade INTEGER)")
    db.execute("CREATE TABLE Groups (\
        id INTEGER PRIMARY KEY, \
        name TEXT)")
    db.execute("CREATE TABLE GroupStudents (\
        id INTEGER PRIMARY KEY, \
        student_id INTEGER REFERENCES Students , \
        group_id REFERENCES Groups)")
    db.execute("CREATE TABLE GroupTeachers (\
        id INTEGER PRIMARY KEY, \
        teacher_id INTEGER REFERENCES Teachers , \
        group_id INTEGER REFERENCES Groups)")


# lisää opettajan tietokantaan
def create_teacher(name):
    teacher = db.execute("INSERT INTO Teachers (name) VALUES (?)", [name])
    id = teacher.lastrowid
    return id


# lisää kurssin tietokantaan
def create_course(name, credits, teacher_ids):
    #print("create_course("+name+", ", credits, ", ", teacher_ids, ")")
    course = db.execute(
        "INSERT INTO Courses (name, credits) VALUES (?, ?)", [name, credits])
    course_id = course.lastrowid
    for teacher_id in teacher_ids:
        db.execute("INSERT INTO CourseTeachers (teacher_id, course_id) VALUES (?,?)", [
                   teacher_id, course_id])
    return course_id


# lisää opiskelijan tietokantaan
def create_student(name):
    student = db.execute("INSERT INTO Students (name) VALUES (?)", [name])
    id = student.lastrowid
    return id


# antaa opiskelijalle suorituksen kurssista
def add_credits(student_id, course_id, date, grade):
    #print("courses.add_credits(", student_id, ",",course_id, ",", date, ",", grade, ")")
    credit = db.execute("INSERT INTO Credits (student_id, course_id, date, grade)\
        VALUES (?,?,?,?)", [student_id, course_id, date, grade])


# lisää ryhmän tietokantaan
def create_group(name, teacher_ids, student_ids):
    #print("create_group(", name, ",", teacher_ids, ",", student_ids, ")")
    group = db.execute("INSERT INTO Groups (name) VALUES (?)", [name])
    group_id = group.lastrowid
    for teacher_id in teacher_ids:
        db.execute("INSERT INTO GroupTeachers (teacher_id, group_id) VALUES (?,?)", [
            teacher_id, group_id])
    for student_id in student_ids:
        db.execute("INSERT INTO GroupStudents (student_id, group_id) VALUES (?,?)", [
            student_id, group_id])


# hakee kurssit, joissa opettaja opettaa (aakkosjärjestyksessä)
def courses_by_teacher(teacher_name):
    #print("courses_by_teacher(", teacher_name, ")")
    courses = db.execute("SELECT c.name \
        FROM Courses c, CourseTeachers ct, Teachers t\
        WHERE t.name = ? AND t.id = ct.teacher_id AND ct.course_id = c.id\
        ORDER BY c.name ", [teacher_name]).fetchall()
    return [x[0] for x in courses]


# hakee opettajan antamien opintopisteiden määrän
def credits_by_teacher(teacher_name):
    #print("credits_by_teacher(", teacher_name, ")")
    op = db.execute("SELECT IFNULL(SUM(k.credits), 0) FROM Teachers t\
        LEFT JOIN CourseTeachers ct ON ct.teacher_id = t.id \
        LEFT JOIN Credits c ON ct.course_id = c.course_id\
        LEFT JOIN Courses k ON k.id = c.course_id\
        WHERE  t.name = ?\
        GROUP BY t.name;", [teacher_name]).fetchone();
    return op[0]


# hakee opiskelijan suorittamat kurssit arvosanoineen (aakkosjärjestyksessä)
def courses_by_student(student_name):
    # print("courses_by_student(",student_name,")");
    courses = db.execute("SELECT k.name, c.grade \
        FROM Courses k, Credits c, Students s\
        WHERE s.name = ? AND s.id = c.student_id AND c.course_id = k.id\
        ORDER BY k.name;", [student_name]).fetchall()
    return courses


# hakee tiettynä vuonna saatujen opintopisteiden määrän
def credits_by_year(year):
    # print("credits_by_year(",year,")");
    op = db.execute("SELECT SUM(k.credits) FROM Courses k, Credits c \
        WHERE c.course_id = k.id AND strftime('%Y', c.date) = ?", [str(year)]).fetchone()
    return op[0]


# hakee kurssin arvosanojen jakauman (järjestyksessä arvosanat 1-5)
def grade_distribution(course_name):
    # print("grade_distribution(",course_name,")")
    distr = db.execute("SELECT DISTINCT c.grade, count(c.id) \
        FROM Credits c, Courses k \
        WHERE k.name = ? AND k.id = c.course_id\
        GROUP BY c.grade ORDER BY c.grade", [course_name]).fetchall()
    res = {1: 0, 2: 0, 3: 0, 4: 0, 5: 0}
    for d in distr:
        key, value = d
        res[key] = value
    return res


# hakee listan kursseista (nimi, opettajien määrä, suorittajien määrä) (aakkosjärjestyksessä)
def course_list():
    # print("course_list()")
    courses = db.execute("SELECT DISTINCT c.name, COUNT(DISTINCT ct.id), COUNT(DISTINCT cr.id)\
        FROM Courses c \
        LEFT JOIN CourseTeachers ct ON ct.course_id = c.id\
        LEFT JOIN Credits cr ON cr.course_id=c.id\
        GROUP BY c.name ORDER BY c.name").fetchall()
    return courses


# hakee listan opettajista kursseineen (aakkosjärjestyksessä opettajat ja kurssit)
def teacher_list():
    # print("teacher_list()")
    teachers = db.execute("SELECT DISTINCT t.name, k.name \
        FROM Teachers t\
        LEFT JOIN CourseTeachers ct ON t.id = ct.teacher_id\
        LEFT JOIN Courses k ON ct.course_id = k.id\
        GROUP BY t.name, k.name ORDER BY t.name, k.name;").fetchall()
    res = []
    ope = ""
    kurssit = []
    for teacher in teachers:
        t, c = teacher
        if ope == t:
            kurssit.append(c)
        else:
            if ope != "":
                res.append(((ope, kurssit)))
            ope = t
            kurssit = [c]
    res.append(((ope, kurssit)))
    return res
# lopusta puuttuu ('Matti Luukkainen', ['Tietokantojen perusteet'])

# hakee ryhmässä olevat henkilöt (aakkosjärjestyksessä)
def group_people(group_name):
    #print("group_people(", group_name, ")")
    students = db.execute("SELECT s.name\
        FROM Students s, GroupStudents gs, Groups g\
        WHERE s.id=gs.student_id AND g.id=gs.group_id AND g.name= ?\
        ORDER BY s.name", [group_name]).fetchall()

    teachers = db.execute("SELECT t.name\
        FROM Teachers t, GroupTeachers gt, Groups g\
        WHERE t.id=gt.teacher_id AND g.id=gt.group_id AND g.name= ?\
        ORDER BY t.name", [group_name]).fetchall()

    students = [x[0] for x in students]
    teachers = [x[0] for x in teachers]
    return(sorted(students+teachers))


# hakee ryhmissä saatujen opintopisteiden määrät (aakkosjärjestyksessä)
def credits_in_groups():
    #print("credits_in_groups()")
    groups = db.execute("SELECT g.name, IFNULL(SUM(c.credits), 0)\
        FROM Groups g\
        LEFT JOIN GroupStudents gs ON g.id = gs.group_id \
        LEFT JOIN Credits cr ON gs.student_id = cr.student_id\
        LEFT JOIN Courses c ON c.id = cr.course_id\
        GROUP BY g.name ORDER BY g.name;").fetchall()
    return groups

# hakee ryhmät, joissa on tietty opettaja ja opiskelija (aakkosjärjestyksessä)
def common_groups(teacher_name, student_name):
    #print("common_groups(",teacher_name,",",student_name,")")
    groups = db.execute("SELECT DISTINCT g.name\
        FROM Groups g, Students s, Teachers t, GroupTeachers gt, GroupStudents gs\
        WHERE t.name = ? AND s.name = ? \
        AND gt.teacher_id = t.id AND gs.student_id = s.id AND gt.group_id = gs.group_id AND g.id = gt.group_id\
        ",[teacher_name, student_name]).fetchall()
    return [x[0] for x in groups]
