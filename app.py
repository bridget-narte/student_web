import os
import sys
import cloudinary
import cloudinary.uploader
from flask import Flask, render_template, request, redirect, flash, url_for

# Import database helpers
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'db'))
from db.dbhelper import init_db, getall, addrecord, updaterecord, deleterecord

# Flask app setup
app = Flask(__name__)
app.config['SECRET_KEY'] = 'd71068e934814ce781d1cfe5c3090684'

# ✅ Cloudinary configuration — make sure these are set in Render Environment Variables
cloudinary.config(
    cloud_name=os.getenv('CLOUDINARY_CLOUD_NAME'),
    api_key=os.getenv('CLOUDINARY_API_KEY'),
    api_secret=os.getenv('CLOUDINARY_API_SECRET')
)

# Initialize SQLite database
try:
    init_db()
except Exception as e:
    print("⚠️ Database initialization error:", e)

# ---------------------------
# Routes
# ---------------------------

@app.route("/")
def index():
    """Home page showing all students."""
    try:
        students = getall('students')
    except Exception:
        students = []
    return render_template("index.html", studentlist=students)


@app.route("/savestudent", methods=['POST'])
def savestudent():
    """Add a new student."""
    idno = request.form['idno'].strip()
    lastname = request.form['lastname'].strip()
    firstname = request.form['firstname'].strip()
    course = request.form['course'].strip()
    level = request.form['level'].strip()
    photo = request.files.get('photo')

    if not all([idno, lastname, firstname, course, level]):
        flash("All fields are required!", "error")
        return redirect(url_for('index'))

    photopath = 'https://res.cloudinary.com/demo/image/upload/v1698788888/default_user.png'  # Default image

    if photo:
        try:
            upload_result = cloudinary.uploader.upload(photo)
            photopath = upload_result.get('secure_url', photopath)
        except Exception as e:
            print("❌ Cloudinary upload error:", e)
            flash("Could not upload photo to Cloudinary.", "warning")

    ok = addrecord(
        'students',
        idno=idno,
        lastname=lastname,
        firstname=firstname,
        course=course,
        level=level,
        photo=photopath
    )

    flash("Student information saved successfully" if ok else "Error saving student information",
          "success" if ok else "error")
    return redirect(url_for('index'))


@app.route("/editstudent", methods=['POST'])
def editstudent():
    """Edit an existing student."""
    id = request.form['id']
    idno = request.form['idno'].strip()
    lastname = request.form['lastname'].strip()
    firstname = request.form['firstname'].strip()
    course = request.form['course'].strip()
    level = request.form['level'].strip()
    photo = request.files.get('photo')

    old_photo = request.form.get('old_photo', 'https://res.cloudinary.com/demo/image/upload/v1698788888/default_user.png')
    photopath = old_photo

    if photo:
        try:
            upload_result = cloudinary.uploader.upload(photo)
            photopath = upload_result.get('secure_url', photopath)
        except Exception as e:
            print("❌ Cloudinary upload error:", e)
            flash("Could not upload new photo to Cloudinary.", "warning")

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

    flash("Student updated successfully" if ok else "Error updating student",
          "success" if ok else "error")
    return redirect(url_for('index'))


@app.route("/deletestudent")
def deletestudent():
    """Delete a student by ID."""
    id = request.args.get('id')
    ok = deleterecord('students', id=id)

    flash("Student deleted successfully" if ok else "Error deleting student",
          "success" if ok else "error")
    return redirect(url_for('index'))


# ---------------------------
# Run the app
# ---------------------------
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)
