from app import app, db
from dataclasses import dataclass
from datetime import datetime
# Creating the Inserttable for inserting data into the database
@dataclass
class Product(db.Model):
    __tablename__ = 'product'
    _id:int = db.Column('product_id', db.Integer, primary_key=True)
    name:str = db.Column('product_name', db.String(30))
    # prod_c = db.relationship("Course", backref="prod", cascade="all, delete", passive_deletes=True,)
    
    def __init__(self, name):
        self.name = name

@dataclass
class Department(db.Model):
    __tablename__ = 'department'
    _id:int = db.Column('department_id', db.Integer, primary_key=True)
    name:str = db.Column('department_name', db.String(30))
    department_code:str = db.Column('department_code', db.String(30), nullable=True)
    dept_c = db.relationship("Course", backref="dept", cascade="all, delete", passive_deletes=True,)
    dept_u = db.relationship("Unit", backref="dept", cascade="all, delete", passive_deletes=True,)
    
    def __init__(self, name, department_code):
        self.name = name
        self.department_code = department_code

@dataclass
class Unit(db.Model):
    __tablename__ = 'unit'
    _id:int = db.Column('unit_id', db.Integer, primary_key=True)
    name:str = db.Column('unit_name', db.String(30))
    unit_code:str = db.Column(db.String(30))
    department_id:int = db.Column(db.Integer, db.ForeignKey('department.department_id', ondelete="CASCADE"))
    unit_c = db.relationship("Course", backref="unit", cascade="all, delete", passive_deletes=True,)
    
    def __init__(self, name, unit_code, department_id):
        self.name = name
        self.unit_code = unit_code
        self.department_id = department_id


@dataclass
class Item_1(db.Model):
    __tablename__ = 'item_1'
    _id:int = db.Column('item_1_id', db.Integer, primary_key=True)
    name:str = db.Column('name', db.String(10))
    Item_1 = db.relationship("Item_2", backref="item_1", cascade="all, delete", passive_deletes=True,)
    def __init__(self, name):
        self.name = name
    def get_item_3_list(self):
        # Retrieve all associated Item_3 instances through Item_2
        item_3_list = [item_2.Item_2 for item_2 in self.Item_1]
        return item_3_list
@dataclass
class Item_2(db.Model):
    __tablename__ = 'item_2'
    _id:int = db.Column('item_2_id', db.Integer, primary_key=True)
    item_1_id:int = db.Column('item_1_id', db.Integer, db.ForeignKey('item_1.item_1_id', ondelete="CASCADE"))
    name:str = db.Column('name', db.String(10))

    Item_2 = db.relationship("Item_3", backref="item_2", cascade="all, delete", passive_deletes=True,)
    
    def __init__(self, name, item_1_id):
        self.name = name
        self.item_1_id = item_1_id
@dataclass
class Item_3(db.Model):
    __tablename__ = 'item_3'
    _id:int = db.Column('item_3_id', db.Integer, primary_key=True)
    item_2_id:int = db.Column('item_2_id', db.Integer, db.ForeignKey('item_2.item_2_id', ondelete="CASCADE"))
    name:str = db.Column('name', db.String(10))

    
    def __init__(self, name, item_2_id):
        self.name = name
        self.item_2_id = item_2_id

@dataclass
class Skill(db.Model):
    __tablename__ = 'skill'
    _id:int = db.Column('skill_id', db.Integer, primary_key=True)
    name:str = db.Column('skill_name', db.String(10))
    process_id:str = db.Column(db.Integer, db.ForeignKey('department.department_id', ondelete="CASCADE"))
    skill_c = db.relationship("Course", backref="skill", cascade="all, delete", passive_deletes=True,)
    
    def __init__(self, name, process_id):
        self.name = name
        self.process_id = process_id
@dataclass
class Process(db.Model):
    __tablename__ = 'process'
    _id:int = db.Column('process_id', db.Integer, primary_key=True)
    name:str = db.Column('process_name', db.String(10))
    def __init__(self, name):
        self.name = name
        
@dataclass
class Course(db.Model):
    __tablename__ = 'course'
    _id:str = db.Column('course_id', db.String(10), primary_key=True)
    skill_id:int = db.Column('skill_id', db.Integer, db.ForeignKey('skill.skill_id', ondelete="CASCADE"))
    name:str = db.Column('course_name', db.String(30))
    duration:int = db.Column('course_duration', db.Integer)
    did:int = db.Column('department_id', db.Integer, db.ForeignKey('department.department_id', ondelete="CASCADE"))
    uid:int = db.Column('unit_id', db.Integer, db.ForeignKey('unit.unit_id', ondelete="CASCADE"))
    desc:str = db.Column('course_description', db.String(900), nullable=True)
    engaged_emp_num:int = db.Column(db.Integer)
    course_start_date:str = db.Column(db.Date)
    course_end_date:str = db.Column(db.Date)
    course_start_time:str = db.Column(db.Time)
    course_end_time:str = db.Column(db.Time)
    course_ca = db.relationship("Course_Assignment", backref="course", cascade="all, delete", passive_deletes=True,)
    course_la = db.relationship("Lecturer_Assignment", backref="course", cascade="all, delete", passive_deletes=True,)
    course_doc = db.relationship("Course_Document", backref="course", cascade="all, delete", passive_deletes=True,)
    
    def __init__(self, _id, skill_id, name, duration, did, uid,  desc, engaged_emp_num=None, 
                 course_start_date=None, course_end_date=None, 
                 course_start_time=None, course_end_time=None):
        self._id = _id
        self.skill_id = skill_id
        self.name = name
        self.duration = duration
        self.did = did
        self.uid = uid
        self.desc = desc
        self.engaged_emp_num = engaged_emp_num
        self.course_start_date = course_start_date
        self.course_end_date = course_end_date
        self.course_start_time = course_start_time
        self.course_end_time = course_end_time

@dataclass
class Course_Document(db.Model):
    __tablename__ = 'course_document'
    _id:int = db.Column('course_document_id', db.Integer, primary_key=True)
    cid:str = db.Column('course_id', db.String(10), db.ForeignKey('course.course_id', ondelete="CASCADE"))
    name:str = db.Column('course_document_name', db.String(30))
    time:str = db.Column('update_time', db.DateTime)
    editor:str = db.Column('editor', db.String(10), db.ForeignKey('employee_static_info.emp_id', ondelete="CASCADE"))
    desc:str = db.Column('document_description', db.String(900))

    def __init__(self, cid, name, time, editor, desc):
        self.cid = cid
        self.name = name
        self.time = time
        self.editor = editor
        self.desc = desc

@dataclass
class Position(db.Model):
    __tablename__ = 'position'
    _id:int = db.Column('position_id', db.Integer, primary_key=True)
    name:str = db.Column('position_name', db.String(30), primary_key=True)
    pos_emp = db.relationship("Employee", backref="position", cascade="all, delete", passive_deletes=True)
@dataclass
class Employee(db.Model):
    __tablename__ = 'employee_static_info'
    _id:int = db.Column('id', db.Integer, primary_key=True)
    code:str = db.Column('emp_id', db.String(10), unique=True)
    name:str = db.Column('emp_name', db.String(30))
    dept:int = db.Column('department_id', db.Integer, db.ForeignKey('department.department_id', ondelete="CASCADE"))
    pos:str = db.Column('position_id', db.Integer, db.ForeignKey('position.position_id', ondelete="CASCADE"))
    gender:str = db.Column('gender', db.String(10))
    birth:str = db.Column('birth', db.Date)
    address:str = db.Column('address', db.String(50))
    phone:str = db.Column('phone', db.String(10))
    mobilephone:str = db.Column('mobilephone', db.String(10))
    email:str = db.Column('email', db.String(30))
    account_enabled:str = db.Column('account_enabled', db.String(10))
    emp_password:str = db.Column('password', db.String(30))
    emp_ca = db.relationship("Course_Assignment", backref="emp", cascade="all, delete", passive_deletes=True)
    emp_ur = db.relationship("User_Role", backref="emp", cascade="all, delete", passive_deletes=True)
    emp_la = db.relationship("Lecturer_Assignment", backref="emp", cascade="all, delete", passive_deletes=True)

    def __init__(self, code, name, dept, pos, gender, birth):
        self.code = code
        self.name = name
        self.dept = dept
        self.pos = pos
        self.gender = gender
        self.birth = birth
@dataclass
class Role_Permission(db.Model):
    __tablename__ = 'role_permission'
    _id = db.Column('role_permission_id', db.Integer, primary_key=True)
    role_name = db.Column(db.String(30))
    role_description = db.Column(db.String(900))
    permission_name = db.Column(db.String(30))
    permission = db.Column(db.String(30))

    def __init__(self, role_name, role_description, permission_name, permission):
        self.role_name = role_name
        self.role_description = role_description
        self.permission_name = permission_name
        self.permission = permission

@dataclass
class User_Role(db.Model):
    __tablename__ = 'user_role'
    _id:int = db.Column('relation_id', db.Integer, primary_key=True)
    role_permission_id:int = db.Column(db.Integer, db.ForeignKey('role_permission.role_permission_id'))
    emp_id:str = db.Column(db.String(10), db.ForeignKey('employee_static_info.emp_id', ondelete="CASCADE"))
    emp_role_start:str = db.Column(db.Date, nullable=True)
    emp_role_end:str = db.Column(db.Date, nullable=True)

    def __init__(self, role_permission_id, emp_id, emp_role_start = None, emp_role_end = None):
        self.role_permission_id = role_permission_id
        self.emp_id = emp_id
        self.emp_role_start = emp_role_start
        self.emp_role_end = emp_role_end

@dataclass
class Lecturer_Assignment(db.Model):
    __tablename__ = 'lecturer_assignment'
    _id:int = db.Column('lecturer_assignment_id', db.Integer, primary_key=True)
    emp_code:str = db.Column(db.String(10), db.ForeignKey('employee_static_info.emp_id', ondelete="CASCADE"))
    course_id:str = db.Column(db.String(10), db.ForeignKey('course.course_id', ondelete="CASCADE"))
    lecturer_rating:int = db.Column(db.Integer, nullable=True)
    
    def __init__(self, emp_code, course_id, lecturer_rating=None):
        self.emp_code = emp_code
        self.course_id = course_id
        self.lecturer_rating = lecturer_rating
@dataclass  
class Course_Assignment(db.Model):
    __tablename__ = 'course_assignment'
    _id:int = db.Column('assignment_id', db.Integer, primary_key=True)
    emp_code:str = db.Column(db.String(10), db.ForeignKey('employee_static_info.emp_id', ondelete="CASCADE"))
    cid:str = db.Column('course_id', db.String(10), db.ForeignKey('course.course_id', ondelete="CASCADE"))
    def __init__(self, emp_code, cid):
        self.emp_code = emp_code
        self.cid = cid
# 新增產品
app.app_context().push()
