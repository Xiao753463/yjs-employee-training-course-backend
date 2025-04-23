from app import db
from app.models import Employee
from sqlalchemy import *
from sqlalchemy.orm import *
from flask import request, jsonify, session

def member_login():
    data = request.get_json()
    emp_id = data.get('emp_id')
    password = data.get('emp_password')

    employee = db.session.query(Employee).filter(Employee.code == emp_id, Employee.emp_password == password).first()
    print(db.session.query(Employee).filter(Employee.code == emp_id).first())
    if employee:
        session['username'] = emp_id
        return jsonify({
            'status': 'success',
            'data': {
                'user_id': emp_id,
                'user_name': employee.name
            }
        })
    else:
        return jsonify({
            'status': 'error',
            'message': 'Invalid username or password'
        })