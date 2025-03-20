from flask import Flask, render_template, request, redirect, url_for
import db  # Archivo que maneja las conexiones y consultas SQL

app = Flask(__name__)

@app.route('/')
def home():
    # Consultar asignaturas desde la base de datos
    subjects = db.query("SELECT * FROM subjects ORDER BY name")
    return render_template('home.html', subjects=subjects)

@app.route('/students')
def students():
    # Consultar estudiantes junto con sus asignaturas y calificaciones
    students = db.query("""
        SELECT s.student_id, s.name, s.email, 
               GROUP_CONCAT(CONCAT(sb.name, ': ', IFNULL(ps.calification, 'Sin nota')) SEPARATOR ', ') AS subjects_grades
        FROM students s
        LEFT JOIN person_subjects ps ON s.student_id = ps.person_id
        LEFT JOIN subjects sb ON ps.subject_id = sb.subject_id
        GROUP BY s.student_id
        ORDER BY s.name
    """)
    return render_template('students.html', students=students)

@app.route('/add_student', methods=['GET', 'POST'])
def add_student():
    if request.method == 'POST':
        # Recoger datos del formulario
        name = request.form['name']
        dni = request.form['dni']
        phone = request.form['phone']
        email = request.form['email']
        address = request.form['address']
        # Insertar estudiante en la base de datos
        db.execute(
            "INSERT INTO students (name, dni, phone, email, address) VALUES (%s, %s, %s, %s, %s)",
            (name, dni, phone, email, address)
        )
        return redirect(url_for('students'))
    return render_template('add_student.html')

@app.route('/subject/<int:subject_id>')
def subject_detail(subject_id):
    # Consultar detalles de la asignatura y los estudiantes
    subject = db.query_one("SELECT * FROM subjects WHERE subject_id = %s", (subject_id,))
    students = db.query("""
        SELECT s.student_id, s.name, ps.calification
        FROM students s
        LEFT JOIN person_subjects ps ON s.student_id = ps.person_id AND ps.subject_id = %s
        ORDER BY s.name
    """, (subject_id,))
    return render_template('subject.html', subject=subject, students=students)

@app.route('/update_grade', methods=['POST'])
def update_grade():
    # Recoger datos del formulario
    student_id = request.form['student_id']
    subject_id = request.form['subject_id']
    grade = request.form['grade']
    
    # Insertar o actualizar calificación en la base de datos
    db.execute("""
        INSERT INTO person_subjects (person_id, subject_id, calification)
        VALUES (%s, %s, %s)
        ON DUPLICATE KEY UPDATE calification = %s
    """, (student_id, subject_id, grade, grade))

    return redirect(url_for('subject_detail', subject_id=subject_id))

@app.route('/delete_grade', methods=['POST'])
def delete_grade():
    # Recoger datos del formulario
    student_id = request.form['student_id']
    subject_id = request.form['subject_id']

    # Eliminar calificación de la base de datos
    db.execute("""
        DELETE FROM person_subjects
        WHERE person_id = %s AND subject_id = %s
    """, (student_id, subject_id))

    return redirect(url_for('subject_detail', subject_id=subject_id))

@app.route('/delete_student', methods=['POST'])
def delete_student():
    # Recoger el ID del alumno desde el formulario
    student_id = request.form['student_id']
    
    # Eliminar al alumno de la base de datos
    db.execute("""
        DELETE FROM students
        WHERE student_id = %s
    """, (student_id,))

    # Redirigir a la lista de alumnos después de eliminar
    return redirect(url_for('students'))

if __name__ == '__main__':
    app.run(debug=True)
