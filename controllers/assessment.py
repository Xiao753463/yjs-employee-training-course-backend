from sqlalchemy.orm import Session
from flask import request
from app.database import DB_ENGINE
from app.models import *
import app.services.assessment_service as AssessmentService
import app.services.employee_service as EmployeeService
import app.services.item_service as ItemService

def getAssessment():
    with Session(DB_ENGINE) as session:
        try:
            assessments = AssessmentService.getAssessments()
            result = { 'assessments' : [] }

            for assessment in assessments:
                employee = EmployeeService.getEmployee(assessment.emp_id)

                result['assessments'].append({
                    'assessment_id':assessment.assesment_id,
                    'emp_id':assessment.emp_id,
                    'emp_name':employee.emp_name,
                    'judge_id':assessment.judge_id,
                    'assessment_date':assessment.date.__str__(),
                    'assessment_startTime':assessment.time_start.__str__(),
                    'assessment_endTime':assessment.time_end.__str__(),
                    'assessment_type':assessment.type,
                    'item_3_id':assessment.item_3_id
                })

            return result
        except Exception as e:
            print(e)
            session.rollback()
            return {'status':'fail','message':'錯誤'}
        
def postAssessment():
    with Session(DB_ENGINE) as session:
        try:
            reqBody = request.json
            assessments = []
            for assessmentDict in reqBody['assessments']:
                assesment_id = assessmentDict['assessment_id'] if assessmentDict['assessment_id'] != -1 else None
                emp_id = assessmentDict['emp_id']
                judge_id = assessmentDict['judge_id']
                assessment_type = assessmentDict['assessment_type']
                item_3_id = assessmentDict['item_3_id']
                assessment_date = assessmentDict['assessment_date']
                assessment_startTime = assessmentDict['assessment_startTime']
                assessment_endTime = assessmentDict['assessment_endTime']

                assessments.append(Assesment(
                    assesment_id=assesment_id,
                    emp_id=emp_id,
                    judge_id=judge_id,
                    item_3_id=item_3_id,
                    date=assessment_date,
                    time_start=assessment_startTime,
                    time_end=assessment_endTime,
                    type=assessment_type
                ))
            
            AssessmentService.syncAssessmentsToDB(session,assessments)
            session.commit()

            return {'status':'success','message':'評量規劃儲存成功。'}
        except Exception as e:
            print(e)
            session.rollback()
            return {'status':'fail','message':'錯誤'}

def getAssessmentByTime(date,startTime,endTime):
    with Session(DB_ENGINE) as session:
        try:
            assessments = AssessmentService.getAssessmentByTime(date,startTime,endTime)
            result = { 'assessments' : [] }

            for assessment in assessments:
                employee = EmployeeService.getEmployee(assessment.emp_id)
                result['assessments'].append({
                    'assessment_id':assessment.assesment_id,
                    'emp_id':assessment.emp_id,
                    'emp_name':employee.emp_name,
                    'assessment_type':assessment.type,
                    'item_3_id':assessment.item_3_id
                })
            
            return result
        except Exception as e:
            print(e)
            session.rollback()
            return {'status':'fail','message':'錯誤'}

def getAssessmentResult(assessment_id):
    with Session(DB_ENGINE) as session:
        try:
            assessment_id = int(assessment_id)
            assessmentResults = AssessmentService.getAssessmentResultsByAssessmentId(assessment_id)

            result = { 'results' : [] }
            for assessmentResult in assessmentResults:
                result['results'].append({
                    'result_id':assessmentResult.result_id,
                    'assessment_id':assessmentResult.assesment_id,
                    'item_4_id':assessmentResult.item_4_id,
                    'mistake':assessmentResult.mistake,
                    'action_score':assessmentResult.action_score,
                    'quality_score':assessmentResult.quality_score
                })

            return result
        except Exception as e:
            print(e)
            session.rollback()
            return {'status':'fail','message':'錯誤'}

def postAssessmentResult():
    def mistakeArrToStr(mistakeArr : List[int]) -> str:
        mistakeStr = ''
        for i in range(len(mistakeArr)):
            mistakeStr += str(mistakeArr[i])
            if i != len(mistakeArr)-1:
                mistakeStr += ','

        return mistakeStr
        
    with Session(DB_ENGINE) as session:
        try:
            reqBody = request.json

            result_id = reqBody['result_id'] if reqBody['result_id'] != -1 else None
            assessment_id = reqBody['assessment_id']
            item_4_id = reqBody['item_4_id']
            mistake = mistakeArrToStr(reqBody['mistake'])
            action_score = reqBody['action_score']
            quality_score = reqBody['quality_score']

            assessmentResult = AssesmentResult(
                result_id=result_id,
                assesment_id=assessment_id,
                item_4_id=item_4_id,
                mistake=mistake,
                action_score=action_score,
                quality_score=quality_score
            )

            assessmentResult = AssessmentService.postAssessmentResult(session,assessmentResult)
            session.commit()

            return {'status':'success',
                    'message':'儲存成功。',
                    'result_id':assessmentResult.result_id}
        except Exception as e:
            print(e)
            session.rollback()
            return {'status':'fail','message':'錯誤'}
    
def getAssessmentItems():
    with Session(DB_ENGINE) as session:
        try:
            item2s = ItemService.getItem2s()

            result = { 'items' : [] }
            for item2 in item2s:
                item2Dict = {
                    'item_2_id':item2.item_2_id,
                    'item_2_name':item2.name,
                    'children':[]
                }

                item3s = ItemService.getItem3sByItem2Id(item2.item_2_id)
                for item3 in item3s:
                    item3Dict = {
                        'item_3_id':item3.item_3_id,
                        'item_3_name':item3.name
                    }
                    item2Dict['children'].append(item3Dict)
                
                result['items'].append(item2Dict)

            return result
        except Exception as e:
            print(e)
            session.rollback()
            return {'status':'fail','message':'錯誤'}
