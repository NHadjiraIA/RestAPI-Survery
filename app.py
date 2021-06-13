from application.extensions.dtoExtensions import questionResponsesToNextQuestionDto
from domain.entities.sub_question import SubQuestion
from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from marshmallow.fields import Integer
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
# from domain.entities.question_response_user import QuestionResponseUser
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

# À lire :

################################################
#				enpoint user
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

############## Add user#########
@app.route('/adduser', methods=['POST'])
def adduser():
    email = request.form['email']
    if email:
        user = Context.user_repository.get_by_email(email)
        if user:
            return jsonify(message='That email already exists.'), 409
        else:
            first_name = request.form['first_name']
            last_name = request.form['last_name']
            password = request.form['password']
            user = User(first_name=first_name, last_name=last_name, email=email, password=password)
            Context.user_repository.create(user)
            useradded = Context.user_repository.get_by_email(email)
            if useradded:
                return jsonify(message='User created sucessfuly.'), 201
            else:
                return jsonify(message='We could not creat user')
    return jsonify(message='email is required'), 400

# #############update
@app.route('/update_user', methods=['PUT'])
def update_user():
    id = int(request.form['id'])
    user = Context.user_repository.get_by_id(id)

    if user:
        user.id = request.form['id']
        user.first_name = request.form['first_name']
        user.last_name = request.form['last_name']
        user.email = request.form['email']
        user.password = request.form['password']
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
    if request.is_json:
        email = request.json['email']
        password = request.json['password']
    else:
        email = request.form['email']
        password = request.form['password']
    user = Context.user_repository.get_by_email(email)
    if user:
        access_token = create_access_token(identity=email)
        return jsonify(message='login succeded !', access_token=access_token)
    else:
        return jsonify(message='Bad email or password'), 401


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

################################################
#				endpoint planet
################################################


##################### add planet################
@app.route('/addplanet', methods=['POST'])
def addplanet():
    planet_name = request.form['planet_name']
    if planet_name:
        planet = Context.planet_repository.get_by_name(planet_name)
        if planet:
            return jsonify(message='That planet already exists.'), 409
        else:
            planet = Planet(planet_name=request.form['planet_name'],
                            planet_type=request.form['planet_type'],
                            home_star=request.form['home_star'],
                            mass=request.form['mass'],
                            radius=request.form['radius'],
                            distance=request.form['distance'])
            Context.planet_repository.create(planet)
            planetadded = Context.planet_repository.get_by_name(planet_name)
            if planetadded:
                return jsonify(message='Planet created sucessfuly.'), 201
            else:
                return jsonify(message='We could not creat planet')
    return jsonify(message='name is required'), 400





#################search planets

@app.route('/planets', methods=["GET"])
def planets():
    id = request.args.get('id')
    print(id)
    if id:
        planet = Context.planet_repository.get_by_id(id)
        if planet:
            return Planet_schema.dump(planet)
        else:
            return jsonify(message='planet not found'), 404
    else:
        Planet_list = Context.planet_repository.get_all()
        print(Planet_list)
        result = Planets_schema.dump(Planet_list)
        if result:
            return jsonify(result)
        return jsonify(), 204


#################Update planet############     #--Context.planet_repository.delete(planet_id)

@app.route('/update_planet', methods=['PUT'])
def update_planet():
    planet_id = int(request.form['planet_id'])
    planet = Context.planet_repository.get_by_id(planet_id)

    if planet:
        planet.planet_name = request.form['planet_name']
        planet.planet_type = request.form['planet_type']
        planet.home_star = request.form['home_star']
        planet.mass = float(request.form['mass'])
        planet.radius = float(request.form['radius'])
        planet.distance = float(request.form['distance'])
        Context.planet_repository.Update(planet)
        return jsonify(message="You updated a planet"), 200
    else:
        return jsonify(message="That planet does not exist"), 404

######### delete planet

@app.route('/remove_planet', methods=['DELETE'])
def remove_planet():
    planet_id = request.args.get('planet_id')
    planet = Context.planet_repository.get_by_id(planet_id)
    if planet:
        deleted = Context.planet_repository.delete(planet_id)
        return jsonify(message="You deleted a planet"), 200
    else:
        return jsonify(message="That planet does not exist"), 404

###############Question 
@app.route('/question', methods=["GET"])
def question():
    id = request.args.get('id_question')
    print(id)
    if id:
        print('helloooooooooo')
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
                  
# ###############Fields
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

if __name__ == '__main__':
    app.run()
