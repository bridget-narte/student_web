import os
import sys
from flask import Flask, render_template, request, redirect, flash, url_for
from werkzeug.utils import secure_filename

sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'db'))
from db.dbhelper import init_db, getall, addrecord, updaterecord, deleterecord

app = Flask(__name__)
app.config['SECRET_KEY'] = 'd71068e934814ce781d1cfe5c3090684'

app.config['UPLOAD_FOLDER'] = os.path.join('static', 'uploads')
app.config['ALLOWED_EXTENSIONS'] = {'png', 'jpg', 'jpeg', 'gif'}

os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

try:
    init_db()
except Exception as e:
    print("⚠️ Database initialization skipped:", e)

def allowed_file(filename):
    """Check if uploaded file is an allowed image type."""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

@app.route("/")
def index():
    """Home route — displays the student list."""
    try:
        students = getall('students')
    except Exception:
        students = [] 
    return render_template("index.html", studentlist=students)

@app.route("/main")
def main():
    return redirect(url_for('index'))

@app.route("/savestudent", methods=['POST'])
def savestudent():
    """Save a new student record to the database."""
    idno = request.form['idno'].strip()
    lastname = request.form['lastname'].strip()
    firstname = request.form['firstname'].strip()
    course = request.form['course'].strip()
    level = request.form['level'].strip()
    photo = request.files.get('photo')

    if not all([idno, lastname, firstname, course, level]):
        flash("All fields are required!", "error")
        return redirect(url_for('index'))

    photopath = 'images/account.png'

    if photo and allowed_file(photo.filename):
        filename = secure_filename(photo.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        try:
            photo.save(filepath)
            photopath = f'uploads/{filename}'
        except Exception:
            flash(" Uploads not supported on this server (use Render or Railway for full support)", "warning")

    ok = addrecord(
        'students',
        idno=idno,
        lastname=lastname,
        firstname=firstname,
        course=course,
        level=level,
        photo=photopath
    )

    if ok:
        flash("Student information saved successfully", "success")
    else:
        flash("Error saving student information", "error")

    return redirect(url_for('index'))

@app.route("/editstudent", methods=['POST'])
def editstudent():
    id = request.form['id']
    idno = request.form['idno'].strip()
    lastname = request.form['lastname'].strip()
    firstname = request.form['firstname'].strip()
    course = request.form['course'].strip()
    level = request.form['level'].strip()
    photo = request.files.get('photo')

    old_photo = request.form.get('old_photo', 'images/account.png')
    photopath = old_photo

    if photo and allowed_file(photo.filename):
        filename = secure_filename(photo.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        try:
            photo.save(filepath)
            photopath = f'uploads/{filename}'
        except Exception:
            flash("⚠️ Uploads not supported on this server (use Render or Railway for full support)", "warning")

    ok = updaterecord(
        'students',
        id=id,
        idno=idno,
        lastname=lastname,
        firstname=firstname,
        course=course,
        level=level,
        photo=photopath
    )

    if ok:
        flash("Student updated successfully", "success")
    else:
        flash("Error updating student", "error")

    return redirect(url_for('index'))

@app.route("/deletestudent")
def deletestudent():
    """Delete a student record."""
    id = request.args.get('id')
    ok = deleterecord('students', id=id)

    if ok:
        flash("Student deleted successfully", "success")
    else:
        flash("Error deleting student", "error")

    return redirect(url_for('index'))


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)

