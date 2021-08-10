from application.extensions.dtoExtensions import questionResponsesToNextQuestionDto, questionResponsesOfUserDto, questionResponsesToQuestionWithAnswerDto
from domain.entities.sub_question import SubQuestion
from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from marshmallow.fields import Integer
from datetime import datetime
from Config import *
from flask_marshmallow import Marshmallow
from flask_jwt_extended import JWTManager, create_access_token, jwt_required
from flask_mail import Mail, Message
from flask_cors import CORS
from  application.extensions import *
from domain.entities.user import User
from domain.entities.planet import Planet
from domain.entities.question import Question
from domain.entities.exemple import Exemple
from domain.entities.field import Field
from domain.entities.chosen_answer import ChosenAnswer
# from domain.entities.question_field import QuestionField
from domain.entities.question_response_user import QuestionResponseUser
# from domain.entities.question_survey import QuestionSurvey
from domain.entities.report import Report
from domain.entities.response import Response
from domain.entities.survey import Survey
from domain.entities.sub_question import SubQuestion
app = Flask(__name__)
app.config.from_object(Config)
Context = app.config["CONTEXT_FACTORY"](app)
cors = CORS(app, resources={r"/*": {"origins": "*"}})

# initionaliser la base de donnee
ma = Marshmallow(app)
jwt = JWTManager(app)
mail = Mail(app)


# -----------------------------------------------------------------------------
# -----------------------------------------------------------------------------


################################################
#				endpoint user
################################################


############## search user
@app.route('/users', methods=['GET'])
##@jwt_required()
def users():
    name = request.args.get('name')
    id = request.args.get('id')
    email = request.args.get('email')
    if name:
        user = Context.user_repository.get_by_username(name)
        if user:
            return User_schema.dump(user)
        else:
            return jsonify(message='user not found'), 404

    if id:
        user = Context.user_repository.get_by_id(id)
        if user:
            return User_schema.dump(user)
        else:
            return jsonify(message='user not found'), 404
    if email:
        user = Context.user_repository.get_by_email(email)
        if user:
            return User_schema.dump(user)
        else:
            return jsonify(message='user not found'), 404

    users_list = Context.user_repository.get_all()
    result = Users_schema.dump(users_list)
    if result:
        return jsonify(result)
    return  jsonify(), 204

##############user by email
@app.route('/api/v1/users', methods=['GET'])
##@jwt_required()
def usersByEmail():
    email = request.args.get('email')
    if email:
        user = Context.user_repository.get_by_email(email)
        if user:
            return User_schema.dump(user)
        else:
            return jsonify(message='user not found'), 404

    users_list = Context.user_repository.get_all()
    result = Users_schema.dump(users_list)
    if result:
        return jsonify(result)
    return  jsonify(), 204    

############## Add user######### 
@app.route('/api/v1/users', methods=['POST'])
def adduser():
    body = request.json
    email_user = body['email_user']
    if email_user:
        user = Context.user_repository.get_by_email(email_user)
        if user:
            return jsonify(message='That email already exists.'), 409
        else:
             
            first_name_user = body['first_name_user']
            last_name_user = body['last_name_user']
            password_user= body['password_user']
            user = User( first_name_user=first_name_user, last_name_user=last_name_user, email_user=email_user, password_user=password_user)
            Context.user_repository.create(user)
            useradded = Context.user_repository.get_by_email(email_user)
            if useradded:
                return jsonify(message='User created sucessfuly.'), 201
            else:
                return jsonify(message='We could not creat user')
    return jsonify(message='email is required'), 400

    

# #############update
@app.route('/update_user', methods=['PUT'])
def update_user():
    id = int(request.form['id_user'])
    user = Context.user_repository.get_by_id(id)

    if user:
        user.id_user = request.form['id_user']
        user.first_name_user = request.form['first_name_user']
        user.last_name_user = request.form['last_name_user']
        user.email_user = request.form['email_user']
        user.password_user = request.form['password_user']
        Context.user_repository.Update(user)
        return jsonify(message="You updated a user"), 200
    else:
        return jsonify(message="That user does not exist"), 404

# ############delete User
@app.route('/removeuser', methods=['DELETE'])
def removeuser():
    id = request.args.get('id')
    user = Context.user_repository.get_by_id(id)

    if user:
        deleted = Context.user_repository.delete(id)
        return jsonify(message="You deleted a user"), 200
    else:
        return jsonify(message="That user does not exist"), 404

 #############login
@app.route('/login', methods=['POST'])
def login():
    body = request.json
    if body:
        email = body['email']
        password = body['password']
    else:
        email = request.form['email']
        password = request.form['password']
    user = Context.user_repository.get_by_email(email)
    if user:       
        access_token = create_access_token(identity=email)
        if (user.id_user):
           if (password == user.password_user):
               return jsonify(message='login succeded !' ,access_token=access_token,idUser=user.id_user)
           else:
               return jsonify(message='Bad email or password'), 401        
                
    else:
        return jsonify(message="this user doesn't exist" ), 401


########
@app.route('/retrieve_password', methods=['GET'])
def retrieve_password():
    email = request.args.get('email')
    user = Context.user_repository.get_by_email(email)
    if user:
        msg = Message("your planetary API password is " + user.password,
                      sender="admin@planetary-api.com",
                      recipients=[email])
        mail.send(msg)
        return jsonify(message="password sent to " + email)
    else:
        return jsonify(message="That email doesn't exist"), 401

# -----------------------------------------------------------------------------
# -----------------------------------------------------------------------------

#

##############################################################
#				endpoint Question
##############################################################
@app.route('/question', methods=["GET"])
def question():
    id = request.args.get('id_question')
    print(id)
    if id:
        question = Context.question_repository.get_by_id(id)
        if question:
             
            result = QuestionDtos_Schema.dump(question)
            return jsonify(result)
        else:
            return jsonify(message='question not found'), 404
    else:
        Question_list = Context.question_repository.get_all()
        print(Question_list)
        result = Questions_schema.dump(Question_list)
        if result:
            return jsonify(result)
        return jsonify(), 204
        

 ###### response of question 
@app.route('/api/v1/questions/next', methods=['GET'])
def next_question():
    id_question = request.args.get('id_question')
    id_chosen_answer = request.args.get('id_chosen_answer')
    id_field = request.args.get('id_field')
    

    if id_question and id_chosen_answer and id_field:
        response = Context.sub_question_repository.get_by_question_response_chosed(id_question,id_chosen_answer,id_field)
        
        if response:
            nextQuestionDto  = questionResponsesToNextQuestionDto(response)
            return jsonify(nextQuestionDto)
        else:
            return jsonify(message="This is the last question"), 404
    else:
        Response_list = Context.sub_question_repository.get_all() 
        print(Response_list)
        result = Responses_Schema.dump(Response_list)
        if result:
            return jsonify(result)
        return jsonify(), 204    

###### response of question 
@app.route('/api/v1/questions/<id>', methods=['GET'])
def get_question(id):
    if id:
        response = Context.question_repository.get_by_id(id)
        if response:
            questionDto  = questionResponsesToNextQuestionDto(response)
            return jsonify(questionDto)
        else:
            return jsonify(message="That question doesn't exist"), 404  
    else:
        return jsonify(message="id of the question is required !")
                  

 ###### previous  question 
@app.route('/api/v1/questions/previous', methods=['GET'])
def previous_question():
    id_question = request.args.get('id_question')    
    id_field = request.args.get('id_field')
    

    if id_question and id_field:
        response = Context.sub_question_repository.get_previous_question_by_response_chosed(id_question,id_field)
        
        if response:
            previousQuestionDto  = questionResponsesToNextQuestionDto(response)
            return jsonify(previousQuestionDto)
        else:
            return jsonify(message="This is the last question"), 404
    else:
        Response_list = Context.sub_question_repository.get_all() 
        print(Response_list)
        result = Responses_Schema.dump(Response_list)
        if result:
            return jsonify(result)
        return jsonify(), 204    

##############################################################
#				endpoint Field
##############################################################
@app.route('/fields', methods=["GET"])
def field():
    id = request.args.get('id')
     
    if id:
        field = Context.field_repository.get_by_id(id)
        if field:
            return Field_schema.dump(field)
        else:
            return jsonify(message='field not found'), 404
    else:
        Field_list = Context.field_repository.get_all()    
        print(Field_list)
        result = Fields_schema.dump(Field_list)
        if result:
            return jsonify(result)
        return jsonify(), 204

# ##############################################################
#				endpoint Response
##############################################################
#  ################ add response of user         
@app.route('/api/v1/response/user', methods=['POST'])
def responseuser():
    body = request.json
    fieldId = body['id_field']
    userId = body['id_user']
    questionId = body['id_question']
    answerChosenId = body['id_chosen_answer']
    codeUserResponse = body['code_user_response']
    field = Context.field_repository.get_by_id(fieldId)
    user = Context.user_repository.get_by_id(userId)
    if user:
        if field:
            questionField = Context.sub_question_repository.get_question_by_field(fieldId,questionId)
            if questionField:
                answerChosen = Context.question_response_repository.get_answerChosen_by_question(questionId,answerChosenId)
                if answerChosen and codeUserResponse:
                    print(codeUserResponse)
                    responseuser = Context.question_response_user_repository.get_response_by_user_question_answer_chosen(userId,questionId,answerChosenId,codeUserResponse)
                    if responseuser:
                        return jsonify(message='That response  already exists.'), 409
                    else:
                                              
                        currentDateTime = datetime.now()                         
                        responseuser = QuestionResponseUser(code_user_response=codeUserResponse,id_user=userId,id_question=questionId,id_field= fieldId,id_chosen_answer=answerChosenId,datetime_response=currentDateTime)
                        print('responseuser is')
                        print(responseuser)
                        Context.question_response_user_repository.create(responseuser)
                        responseuseradded = Context.question_response_user_repository.get_response_by_user_question_answer_chosen(userId,questionId,answerChosenId,codeUserResponse)
                        if responseuseradded:
                            return jsonify(message='response user created sucessfuly.'), 201
                        else:
                            return jsonify(message='We could not creat user')
                return jsonify(message="this response is not a answer of this question"), 400         
            return jsonify(message="this question didn't exist in this field"), 400            
        return jsonify(message="field didn't exist"), 400
    return jsonify(message="user didn't exist"), 400
######################delete response of user 
@app.route('/api/v1/responses', methods=['DELETE'])
def responseuserdelete():
    userId = request.args.get('id_user')
    questionId = request.args.get('id_question')
    userAnswerCode = request.args.get('survery_answer_code')
    currentresponseuser = Context.question_response_user_repository.get_response_by_user_survery(userId, questionId, userAnswerCode)
    if currentresponseuser:
        deleted = Context.question_response_user_repository.delete(userId, questionId, userAnswerCode)
        if(deleted):
            return jsonify(message="You deleted a response of user "), 200
        return jsonify(message="Could not delete the response of the user"), 500
    else:
        return jsonify(message="That response does not exist"), 404

######################delete response of user 
@app.route('/api/v1/answers', methods=['DELETE'])
def delete_answers_following_questionid():
    questionId = request.args.get('questionId')
    surveryCode = request.args.get('codeSurvery')
    userId = request.args.get('userId')

    questions = []
    next_question_id = questionId
    # create the list of questions to delete
    while(True):
        # get the answer from the user's answers
        answer_dto = questionResponsesToQuestionWithAnswerDto(
                                                              Context
                                                              .question_response_user_repository
                                                              .get_response_by_user_survery(userId, next_question_id, surveryCode)
                                                              )
        print('this is the result***************************************',answer_dto['id'])                                                      
        # get the next question from the survery
        next_question_dto = questionResponsesToNextQuestionDto(Context
                                                               .sub_question_repository
                                                               .get_by_question_response_chosed(next_question_id, answer_dto['id'], answer_dto['fieldId'])
                                                              )
        print('#########################################',next_question_dto)                                                      
        if next_question_dto:
            next_question_id = next_question_dto['id']
            questions.append(next_question_dto['id'])
        else:
            break
    # delete the list of questions    
    if len(questions) > 0:
        deleted = (Context
                   .question_response_user_repository
                   .delete_answers(questions, userId, surveryCode)
                  )
        if(deleted):
            return jsonify(message=(f"All questions following the question : {questionId},"
                                    f" for the surveryCode = {surveryCode} have been deleted")), 200
        return jsonify(message="Could not delete the response of the user"), 500
    else:
        return jsonify(message="That response does not exist"), 404

##       
###### question of user with response chosen before 
@app.route('/api/v1/questions/answered', methods=['GET'])
def question_answered_already():
    code_user_response = request.args.get('code_user_response')
    userId = request.args.get('id_user')
    questionId = request.args.get('id_question')

    if code_user_response:
        currentresponseuser = Context.question_response_user_repository.get_response_by_user_survery(userId, questionId, code_user_response)
        print('this is the response of user in answered',currentresponseuser)
        if currentresponseuser:
            dto = questionResponsesToQuestionWithAnswerDto(currentresponseuser)
            return jsonify(dto)
        else:
            return jsonify(message="the user didn't select a response for this question"), 404
    else:
        return jsonify(message="code_user_response is required !")    
        
# ##################display message report
@app.route('/api/v1/raport/messages', methods=['GET'])
def report_message():
    # id_user = request.args.get('id_user')
    # id_field = request.args.get('id_field')
    code_user_response   = request.args.get('code_user_response')
    

    if code_user_response:
        response = Context.question_response_user_repository.get_message_by_response_user(code_user_response)
        print(response)
        if response:
            messageReportUserDto  = questionResponsesOfUserDto(response)
            return jsonify(messageReportUserDto)
        else:
            return jsonify(message="This is not a response for this user on this field"), 404
    else:
        Response_list = Context.question_response_user_repository.get_all() 
        print(Response_list)
        result = Responses_Schema.dump(Response_list)
        if result:
            return jsonify(result)
        return jsonify(), 204    
################update response
@app.route('/api/v1/responses', methods=['PUT'])
def update_response():
    body = request.json
    code_user_response = body['code_user_response']
    userId = body['id_user']
    questionId = body['id_question']
    currentresponseuser = Context.question_response_user_repository.get_response_by_user_survery(userId, questionId, code_user_response)
    print('this is response************************',currentresponseuser)
    if currentresponseuser:
        currentresponseuser[0].id_question = body['id_question']
        currentresponseuser[0].id_user = body['id_user']
        currentresponseuser[0].id_field = body['id_field']
        currentresponseuser[0].id_chosen_answer = body['id_chosen_answer']
        currentresponseuser[0].datetime_response = datetime.now()
        currentresponseuser[0].code_user_response = body['code_user_response']
        Context.question_response_user_repository.Update(currentresponseuser[0])
        return jsonify(message="You updated a response"), 200
    else:
        return jsonify(message="That response does not exist"), 404        


# batabase models
class UserSchema(ma.Schema):
    class Meta:
        fields = ('id_user', 'first_name_user', 'last_name_user', 'email_user', 'password_user')

class PlanetSchema(ma.Schema):
    class Meta:
        fields = ('planet_id', 'planet_name', 'planet_type', 'home_star', 'mass', 'radius', 'distance', "exemple_id")

class QuestionSchema(ma.Schema):
    class Meta:
         fields = ('id_question', 'content_question','id_response')
class ExempleSchema(ma.Schema):
    class Meta:
        fields = ('exemple_id', 'exemple_name','date_report','planets' )

class FieldSchema(ma.Schema):
    class Meta:
        fields = ('id_field', 'name_field','id_question')   
class ResponseSelectedSchema(ma.Schema):
    class Meta:
        fields = ('id_chosen_answer','id_question')               
 
# class QuestionFieldSchema(ma.Schema):
#     class Meta:
#         fields = ('id_question', 'id_field') 

class ChosenAnswerSchema(ma.Schema):
    class Meta:
        fields = ('id_chosen_answer', 'content_chosen_answer', 'title_chosen_answer','id_response')     

class SubQuestionSchema(ma.Schema):
    class Meta:
        fields = ('id','id_question','id_sub_question','level','id_chosen_answer','id_field','id_response')    

# class QuestionResponseUserSchema(ma.Schema):
#     class Meta:
#         fields = ( 'id_question', 'id_response', 'id_user', 'date_reponse','hour_response')

# class QuestionSurveySchema(ma.Schema):
#     class Meta:
#         fields = ( 'id_question', 'id_survey')  

class ReportSchema(ma.Schema):
    class Meta:
        fields = ( 'id_report','title_report', 'content_report', 'date_report','id_user')           

class Responsechema(ma.Schema):
    class Meta:
        fields = ( 'id_response','id_field', 'content_question','id_question','level') 

class SurveySechema(ma.Schema):
    class Meta:
        fields = ( 'id_survey', 'number_questions', 'title_suvery', 'id_field')

class QuestionResponsesDtoSchema(ma.Schema):
    class Meta:
        #'content_chosen_answer','id_question',
        fields = ('id_question','id_field','id_chosen_answer','content_chosen_answer','id_response','content_question')


class QuestionDtoSchema(ma.Schema):
    class Meta:
        #'content_chosen_answer','id_question',
        fields = ('id_question','content_question')
# instantiate UserSchema (deserialize a single object)
User_schema = UserSchema()
Users_schema = UserSchema(many=True)
Planet_schema = PlanetSchema()
Planets_schema = PlanetSchema(many=True)
Question_schema = QuestionSchema()
Questions_schema = QuestionSchema(many=True)
Exemples_schema = ExempleSchema(many=True)
Exemple_schema = ExempleSchema()
Field_schema = FieldSchema()
Fields_schema = FieldSchema(many=True)
# QuestionField_Schema = QuestionFieldSchema(many=True)
ChosenAnswers_Schema = ChosenAnswerSchema(many=True)
ChosenAnswer_Schema = ChosenAnswerSchema()
# QuestionResponseUser_Schema = QuestionResponseUserSchema(many=True)
# QuestionSurvey_Schema = QuestionSurveySchema(many=True)
Report_Schema = ReportSchema(many=True)
Responses_Schema = Responsechema(many=True)
Response_Schema = Responsechema()
QuestionResponseDtos_Schema =QuestionResponsesDtoSchema(many=True)
QuestionResponseDto_Schema =QuestionResponsesDtoSchema()
QuestionDtos_Schema =QuestionResponsesDtoSchema(many=True)
QuestionDto_Schema =QuestionResponsesDtoSchema()
SubQuestion_Schema = SubQuestionSchema()
SubQuestions_Schema = SubQuestionSchema(many=True)
Survey_Schema = SurveySechema(many=True)
Responses_Selected_Schema = ResponseSelectedSchema(many=True)
Response_Selected_Schema = ResponseSelectedSchema()

if __name__ == '__main__':
    app.run()
