from flask import request
from app import db
from sqlalchemy import delete
from app.models import Department, Unit, Process, Skill, Course, Employee


def get_departments():
    result = db.session.query(Department).all()
    data = []

    for department in result:

        units = db.session.query(Unit).filter_by(
            department_id=department._id).all()

        unit_names = [unit for unit in units]
        data_info = {
            'department': {'id': department._id, 'name': department.name},
            'units': unit_names
        }
        data.append(data_info)

    return data


def get_skills():
    result = db.session.query(Process).all()
    data = []

    for process in result:

        skills = db.session.query(Skill).filter_by(
            process_id=process._id).all()

        skill_names = [skill for skill in skills]
        data_info = {
            'process': {'id': process._id, 'name': process.name},
            'skills': skill_names
        }
        data.append(data_info)

    return data


def get_courses_by_skill(skill_id):
    courses = db.session.query(Course).filter_by(skill_id=skill_id).all()
    return courses


def get_employee():
    result = db.session.query(Employee).all()
    return result
