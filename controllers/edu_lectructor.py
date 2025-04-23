from flask import request
from app import db
from sqlalchemy import delete
from app.models import User_Role, Role_Permission, Lecturer_Assignment, Course

def get_lecturers():
    result = db.session.query(User_Role)\
         .join(Role_Permission, User_Role.role_permission_id == Role_Permission._id)\
         .filter(Role_Permission.role_name == "講師").all()
    r = []
    for row in result:
        lecturer={
            'code': row.emp_id,
            'name': row.emp.name
            }
        r.append(lecturer)
    return r

def get_lecturer_assignments():
    result = db.session.query(Lecturer_Assignment).all()
    r = []
    for row in result:
        course_info = {
            'id': row.course._id,
            'name': row.course.name,
            'skill': row.course.skill,
            'engaged_emp_num': row.course.engaged_emp_num,
            'start_date': row.course.course_start_date.strftime("%Y-%m-%d"),
            'end_date': row.course.course_end_date.strftime("%Y-%m-%d"),
            'start_time': row.course.course_start_time.strftime("%H:%M:%S"),
            'end_time': row.course.course_end_time.strftime("%H:%M:%S")
            }
        lecturer_info = {
            'code': row.emp.code,
            'name': row.emp.name,
            'rating':row.lecturer_rating
        }
        lecturer_data = {
            'id':row._id,
            'course': course_info,
            'lecturer': lecturer_info,
            }
        r.append(lecturer_data)
    return r
def update_lecturer(id):
    try:
        data = request.json
        emp_code = data.get('emp_code')
        lecturer_rating = data.get('rating')
        
        course_id = data.get('cid')
        engaged_emp_num = data.get('engaged_emp_num')
        course_start_date = data.get('course_start_date')
        course_end_date = data.get('course_end_date')
        course_start_time = data.get('course_start_time')
        course_end_time = data.get('course_end_time')

        lecturer = Lecturer_Assignment.query.get(id)
        lecturer.emp_code = emp_code
        lecturer.course_id = course_id
        lecturer.lecturer_rating = lecturer_rating
        db.session.commit()
        
        course = Course.query.get(course_id)
        course.engaged_emp_num = engaged_emp_num
        course.course_start_date = course_start_date
        course.course_end_date = course_end_date
        course.course_start_time = course_start_time
        course.course_end_time = course_end_time
        db.session.commit()
        
        return {'message': 'Assignment updated successfully!'}
    except Exception as e:
        db.session.rollback()
        return {'error': 'Assignment update failed!', 'details': str(e)}, 500
def assign_lecturer():
    try:
        data = request.json
        id = data.get('cid')
        emp_code = data.get('emp_code')
        engaged_emp_num = data.get('engaged_emp_num')
        course_start_date = data.get('course_start_date')
        course_end_date = data.get('course_end_date')
        course_start_time = data.get('course_start_time')
        course_end_time = data.get('course_end_time')
        rating = data.get('rating')
        course = Course.query.get(id)
        course.engaged_emp_num = engaged_emp_num
        course.course_start_date = course_start_date
        course.course_end_date = course_end_date
        course.course_start_time = course_start_time
        course.course_end_time = course_end_time
        assign = Lecturer_Assignment(
            emp_code = emp_code,
            course_id = id,
            lecturer_rating = rating
        )
        db.session.add(assign)
        db.session.commit()
        return {'message': 'Assignment create successfully!'}
    except Exception as e:
        db.session.rollback()
        return {'error': 'Assignment create error!', 'details': str(e)}, 500