from flask import Flask, jsonify, request
from app import db
from app.models import Course, Item_1, Item_2, Item_3, Product, Department, Unit, Course_Assignment, Course_Document, Lecturer_Assignment, Role_Permission, User_Role
from sqlalchemy import *
from sqlalchemy.orm import *
from sqlalchemy.ext.declarative import declared_attr
import sys, json

class AlchemyEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, Row):
            data = {}
            for obj in o:
                data.update(self.parse_sqlalchemy_object(obj))
            return data
        if isinstance(o.__class__, DeclarativeMeta):
            return self.parse_sqlalchemy_object(o)
        return json.JSONEncoder.default(self, o)

    def parse_sqlalchemy_object(self, o):
        data = {}
        fields = o.__json__() if hasattr(o, '__json__') else dir(o)
        for field in [f for f in fields if not f.startswith('_') and f not in ['metadata', 'query', 'query_class', 'registry']]:
            value = o.__getattribute__(field)
            try:
                json.dumps(value)
                data[field] = value
            except TypeError:
                data[field] = None
        return data


        return json.JSONEncoder.default(self, obj)

ALLOWED_EXTENSIONS = set(['pdf', 'png', 'jpg', 'jpeg', 'gif'])
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def get_class(class_name):
    return getattr(sys.modules[__name__], class_name)
def cre_courses():
    try:
        data = request.json
        id = data.get('id')
        skill_id = data.get('skill_id')
        name = data.get('name')
        duration = data.get('duration')
        dept = data.get('department')
        unit = data.get('unit')
        desc = data.get('description')
        course = Course(
            _id = id,
            skill_id = skill_id,
            name = name,
            duration = duration,
            did = dept,
            uid = unit,
            desc = desc,
        )
        db.session.add(course)
        course = Course.query.get(id)
        course.name = name
        course.duration = duration
        course.skill_id = skill_id
        course.did = dept
        course.uid = unit
        course.desc = desc
        
        db.session.commit()
        
        return {'message': 'Course created successfully!'}
    except Exception as e:
        db.session.rollback()
        return {'error': 'Course created failed!', 'details': str(e)}, 500
def get_courses():
    # result = db.session.query(Course, Course_Assignment).join(Course_Assignment, full=True).filter(Course._id == Course_Assignment.cid).all()
    # json_object = json.dumps(result, cls=AlchemyEncoder, ensure_ascii=False).encode('utf8')
    # return json_object
    result = db.session.query(Course, func.count(Course_Assignment.emp_code).label('enrollment_count')) \
        .outerjoin(Course_Assignment, Course._id == Course_Assignment.cid) \
        .options(joinedload(Course.course_ca)).group_by(Course._id) \
        .all()

    r = []
    for row in result:
        course_details = {
            'id': row.Course._id,
            'name': row.Course.name,
            'skill': row.Course.skill,
            'duration': row.Course.duration,
            'department': row.Course.dept,
            'unit': row.Course.unit,
            # 'product': row.Course.prod.name,
            'description': row.Course.desc,
            'enrollment_count': row.enrollment_count,
            'engaged_emp_num': row.Course.engaged_emp_num,
            # 'course_start_date': row.Course.course_start_date.strftime("%Y-%m-%d"),
            # 'course_end_date': row.Course.course_end_date.strftime("%Y-%m-%d"),
            # 'course_start_time': row.Course.course_start_time.strftime("%H:%M:%S"),
            # 'course_end_time': row.Course.course_end_time.strftime("%H:%M:%S")
        }

        # Include the enrollment details if available
        if row.Course.course_ca:
            enrollment_list = [
                {'employee_id': enrollment.emp._id, 'employee_code': enrollment.emp.code, 'employee_name': enrollment.emp.name}
                for enrollment in row.Course.course_ca
            ]
            course_details['enrollment_list'] = enrollment_list

        r.append(course_details) 

    return r
def get_user_courses(id):
    result = db.session.query(Course_Assignment).filter(Course_Assignment.emp_code == id).all()
    courses = []
    for assignment in result:
        course = db.session.query(Course).filter_by(_id=assignment.cid).first()
        if course:
            courses.append({
                    "id":course._id,
                    "name": course.name,
                    "doc":course.course_doc,
                    })
    print(courses)
    print(id)
    return courses

def del_courses():
    id = request.json.get('id')
    sql = delete(Course).where(Course._id == id)
    db.session.execute(sql)
    try:
        db.session.commit()
        return ('Course deleted successfully!')
    # do something with the session
    except:                   # * see comment below
        db.session.rollback()
        return ('Course deleted error!')
        raise
    else:
        db.session.commit()
def upd_course():
    try:
        data = request.json
        id = data.get('id')
        skill_id = data.get('skill_id')
        name = data.get('name')
        duration = data.get('duration')
        dept = data.get('department')
        unit = data.get('unit')
        desc = data.get('description')
        
        course = Course.query.get(id)
        course.name = name
        course.duration = duration
        course.skill_id = skill_id
        course.did = dept
        course.uid = unit
        course.desc = desc
        
        db.session.commit()
        
        return {'message': 'Course updated successfully!'}
    except Exception as e:
        db.session.rollback()
        return {'error': 'Course update failed!', 'details': str(e)}, 500



def del_element(table, id):
    sql = delete(get_class(table)).where(get_class(table)._id == id)
    db.session.execute(sql)
    try:
        db.session.commit()
        return (table + ' deleted successfully!')
    # do something with the session
    except:                   # * see comment below
        db.session.rollback()
        return (table + ' deleted error!')
        raise
    else:
        db.session.commit()
def get_item_1():
    result = db.session.query(Item_1).all()
    r = {}
    for row in result:
        r[row._id] = row.name
    return r
def add_member():
    data = request.json
    if 'cid' not in data:
        return jsonify({'error': 'Missing parameters: cid'}), 400

    cid = data['cid']
    delete_codes = data.get('delete_codes', [])
    add_codes = data.get('add_codes', [])

    try:
        # 刪除操作
        if delete_codes:
            for emp_code in delete_codes:
                Course_Assignment.query.filter_by(emp_code=emp_code, cid=cid).delete()

        # 新增操作
        if add_codes:
            for emp_code in add_codes:
                assignment = Course_Assignment(emp_code=emp_code, cid=cid)
                db.session.add(assignment)

        db.session.commit()
        return jsonify({'message': 'Course assignments updated successfully'}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500
def remove_member(id):
    emp_code = request.json.get('emp_code')
    sql = delete(Course_Assignment).where(Course_Assignment.emp_code == emp_code).where(Course_Assignment.cid == id)
    db.session.execute(sql)
    try:
        db.session.commit()
        return ('Course_Assignment deleted successfully!')
    # do something with the session
    except:                   # * see comment below
        db.session.rollback()
        return ('Course_Assignment deleted error!')
        raise
    else:
        db.session.commit()
    

   