from app import app
from flask import jsonify, render_template
from app.controllers.edu_course import del_element, cre_courses, get_courses, get_user_courses, upd_course, get_item_1, \
    remove_member, add_member
from app.controllers.edu_lectructor import get_lecturers, get_lecturer_assignments, assign_lecturer, update_lecturer
from app.controllers.edu_document import get_file, upl_file, del_file, download_file
from app.controllers.edu_common import get_departments, get_skills, get_courses_by_skill, get_employee
from app.controllers.edu_login import member_login
from model.employeeControl.employee_control import member_app
from model.employeeControl.get_data import get_data_app
from model.employeeControl.role_control import role_app

from Competency.controllers.exam import exam_bp
from Competency.controllers.exam_items import exam_items_bp
from Competency.controllers.exam_sop import exam_sop_bp
from Competency.controllers.assessment import assessment_bp

app.register_blueprint(member_app)
app.register_blueprint(get_data_app)
app.register_blueprint(role_app)
app.register_blueprint(exam_bp)
app.register_blueprint(exam_items_bp)
app.register_blueprint(exam_sop_bp)
app.register_blueprint(assessment_bp)


@app.route('/login')
def login():
    return render_template('login.html')


@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html')

# @app.route('/test')
# def test():
#     return render_template('test.html')


@app.route('/topbar')
def topbar():
    return render_template('topbar.html')


@app.route('/sidebar')
def sidebar():
    return render_template('sidebar.html')


# 人員與權限管理
@app.route('/emp_auth_index')
def emp_auth_index():
    return render_template('emp_auth_index.html')


# 人員管理
@app.route('/emp_index')
def emp_index():
    return render_template('emp_index.html')


# 員工列表
@app.route('/emp_list')
def emp_list():
    return render_template('emp_list.html')


# 新增員工
@app.route('/emp_static_add')
def emp_static_add():
    return render_template('emp_static_add.html')


# 員工詳細資料
@app.route('/emp_static_update')
def emp_static_update():
    return render_template('emp_static_update.html')


# 帳號與權限管理
@app.route('/auth_index')
def auth_index():
    return render_template('auth_index.html')


# 身份權限管理
@app.route('/auth_list')
def auth_list():
    return render_template('auth_list.html')


# 使用者身份管理
@app.route('/role_list')
def role_list():
    return render_template('role_list.html')


# 教育訓練管理
@app.route('/edu_plan_index')
def edu_plan_index():
    return render_template('edu_plan_index.html')


# 課程管理
@app.route('/edu_index')
def edu_index():
    return render_template('edu_index.html')


# 課程管理
@app.route('/edu_course_list')
def edu_course_list():
    return render_template('edu_course_list.html')


# 講師管理
@app.route('/edu_instructor_list')
def edu_instructor_list():
    return render_template('edu_instructor_list.html')


# 指導員管理
@app.route('/edu_mentor_list')
def edu_mentor_list():
    return render_template('edu_mentor_list.html')


# 培訓計畫管理
@app.route('/plan_index')
def plan_index():
    return render_template('plan_index.html')


# 課程指派
@app.route('/plan_assignment_list')
def plan_assignment_list():
    return render_template('plan_assignment_list.html')


# 職能管理
@app.route('/competency_index')
def competency_index():
    return render_template('competency_index.html')


# 實作評量
@app.route('/competency_assess')
def competency_assess():
    return render_template('competency_assess.html')


# 受訓人員評量規劃
@app.route('/competency_assessment')
def competency_assessment():
    return render_template('competency_assessment.html')


# 教育訓練評量表準備
@app.route('/competency_pre')
def competency_pre():
    return render_template('competency_pre.html')


# 教育訓練之生產技術評量
@app.route('/competency_skills')
def competency_skills():
    return render_template('competency_skills.html')


# 使用者人員與權限管理
@app.route('/user_emp_auth_index')
def user_emp_auth_index():
    return render_template('user_emp_auth_index.html')


# 使用者員工基本資料
@app.route('/user_emp_static')
def user_emp_static():
    return render_template('user_emp_static.html')


# 使用者教育訓練管理
@app.route('/user_edu_index')
def user_edu_index():
    return render_template('user_edu_index.html')


# 使用者個人課程列表
@app.route('/user_course_list')
def user_course_list():
    return render_template('user_course_list.html')


# 使用者職能管理
@app.route('/user_competency_index')
def user_competency_index():
    return render_template('user_competency_index.html')


# 評量成績統計與檢視
@app.route('/assessment_review')
def assessment_review():
    return render_template('assessment_review.html')


@app.route('/api/courses', methods=['GET'])
def getCourse():
    courses = get_courses()
    return courses


@app.route('/api/courses/<id>', methods=['GET'])
def get_user_courses_api(id):
    courses = get_user_courses(id)
    return courses


@app.route('/api/courses', methods=['PUT'])
def updateCourse():
    courses = upd_course()
    return jsonify(courses)


@app.route('/api/courses', methods=['POST'])
def createCourse():
    return cre_courses()


@app.route('/api/courses/<id>', methods=['DELETE'])
def deleteCourse(id):
    return del_element("Course", id)


@app.route('/api/courses/<cid>/files', methods=['GET'])
def getFile(cid):
    return get_file(cid)


@app.route('/api/files', methods=['POST'])
def uploadFile():
    return jsonify(upl_file())


@app.route('/api/files/<id>', methods=['DELETE'])
def removeFile(id):
    return jsonify(del_file(id))


@app.route('/api/lecturer-assignments', methods=['GET'])
def gotLecturerAssignments():
    return jsonify(get_lecturer_assignments())


@app.route('/api/lecturer-assignments', methods=['POST'])
def assignLecturer():
    return jsonify(assign_lecturer())


@app.route('/api/lecturer-assignments/<id>', methods=['PUT'])
def update_lecturer_api(id):
    return jsonify(update_lecturer(id))


@app.route('/api/lecturer-assignments/<id>', methods=['DELETE'])
def delLecturerAssignment(id):
    return jsonify(del_element("Lecturer_Assignment", id))


@app.route('/api/lecturers', methods=['GET'])
def gotLecturers():
    return get_lecturers()


@app.route('/api/plans', methods=['POST'])
def addMember():
    return add_member()


@app.route('/api/plans/<id>', methods=['DELETE'])
def removeMember(id):
    return jsonify(remove_member(id))


@app.route('/api/departments', methods=['GET'])
def getDepartments():
    return jsonify(get_departments())


@app.route('/api/skills', methods=['GET'])
def getSkills():
    return jsonify(get_skills())


@app.route('/api/skills/<int:skill_id>', methods=['GET'])
def get_courses_by_skill_api(skill_id):
    courses = get_courses_by_skill(skill_id)
    courses_data = []
    for course in courses:
        course_data = {
            'id': course._id,
            'engaged_emp_num': course.engaged_emp_num,
            'course_start_date': course.course_start_date.strftime("%Y-%m-%d"),
            'course_end_date': course.course_end_date.strftime("%Y-%m-%d"),
            'course_start_time': course.course_start_time.strftime("%H:%M:%S"),
            'course_end_time': course.course_end_time.strftime("%H:%M:%S"),
        }
        courses_data.append(course_data)

    return jsonify(courses_data)


@app.route('/api/employees', methods=['GET'])
def get_employee_api():
    return jsonify(get_employee())


@app.route('/api/courses/<cid>/files/download', methods=['GET'])
def download_file_api(cid):
    return download_file(cid)


@app.route('/api/auth/session', methods=['POST'])
def memberLogin():
    return member_login()
