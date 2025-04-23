from flask import flash, redirect, request, send_from_directory
from app import app, db
from sqlalchemy import delete
from app.models import Course_Document
import os
from werkzeug.utils import secure_filename
ALLOWED_EXTENSIONS = set(['pdf', 'doc', 'png', 'jpg', 'jpeg', 'gif'])
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def get_file(cid):
    result = db.session.query(Course_Document).where(Course_Document.cid == cid).all()
    return result
def upl_file():
    cid = request.form.get('cid')
    time = request.form.get('time')
    editor = request.form.get('editor')
    desc = request.form.get('desc')
    file = request.files['file']
    course_folder = os.path.join(app.root_path, 'static', cid)
    name = ''
    if not os.path.exists(course_folder):
        os.makedirs(course_folder)
    if file and allowed_file(file.filename):
        counter = 1
        print("file.filename: "+file.filename)
        filename = file.filename
        path = course_folder + "/" + filename
        temp_filename, extension = os.path.splitext(filename)
        while os.path.exists(path):
            filename = temp_filename + " (" + str(counter) + ")" + extension
            path = course_folder + "/" + filename
            counter += 1
        file.save(os.path.join(course_folder, filename))
        name = filename
        pass
    else:
        return ('File uploaded error!')
    
    doc = Course_Document(
        cid = cid,
        name = name,
        time = time,
        editor = editor,
        desc = desc
    )
    db.session.add(doc)
    try:
        db.session.commit()
        return ('Course create successfully!')
    # do something with the session
    except Exception as e:
        db.session.rollback()
        error_message = str(e)
        print("Error:", error_message)
        return ('Course create error: ' + error_message)
    else:
        db.session.commit()
    
def del_file(id):
    result = db.session.query(Course_Document).first()
    cid = result.cid
    name = result.name
    course_folder = os.path.join(app.root_path, 'static', cid)
    try:
        os.remove(os.path.join(course_folder, name))
        pass
    except:
        return ('Cannot find the file you want delete')
    sql = delete(Course_Document).where(Course_Document.cid == cid).where(Course_Document.name == name)
    db.session.execute(sql)
    try:
        db.session.commit()
        return ('Course document deleted successfully!')
    # do something with the session
    except:                   # * see comment below
        db.session.rollback()
        return ('Course deleted error!')
        raise
    else:
        db.session.commit()

def download_file(cid):
    try:
        name = request.args.get('name')  # Get parameter from the URL query string
        if not name:
            raise ValueError("No file name provided in the request")

        course_folder = os.path.join(app.static_folder, cid)
        print("course_folder: " + course_folder)
        print("name: " + name)
        # Check if the file exists
        if not os.path.exists(os.path.join(course_folder, name)):
            raise FileNotFoundError("File not found")
        return send_from_directory(course_folder, name, as_attachment=True)  # Explicitly set attachment filename
    
    except ValueError as ve:
        return str(ve), 400  # Return error message and 400 error code
    
    except FileNotFoundError:
        return "File not found", 404  # Return file not found error message and 404 error code

    except Exception as e:
        return str(e), 500  # Return other exceptions' error message and 500 error code