
from flask_mail import Message

def questionResponsesToNextQuestionDto(questionResponseChoices):
  if questionResponseChoices.count() == 0:
    return None
    
  responseChoices = []
  for responseChoice in questionResponseChoices:
    responseChoices.append({
      "idResponse": responseChoice.id_response,
      "idResponseChoice": responseChoice.id_chosen_answer,
      "title": responseChoice.content_chosen_answer
    })
  nextQuestionDto = {
    "id" : questionResponseChoices[0].id_question,
    "title" : questionResponseChoices[0].content_question,
    "level" : questionResponseChoices[0].level,
    "responseChoices": responseChoices
  }
  return nextQuestionDto
########
def questionResponsesToQuestionWithAnswerDto (responseQuestionsUserChosen):
  if responseQuestionsUserChosen.count() == 0:
    return None
  questionWithAnswerDto = {
    "id" : responseQuestionsUserChosen[0].id_chosen_answer,
    "fieldId":responseQuestionsUserChosen[0].id_field
  }

  return questionWithAnswerDto  

def questionResponsesOfUserDto(questionResponseChoicesReport):
  if questionResponseChoicesReport.count() == 0:
    return None
    
  responseChoicesReport = []
  for responseChoiceReport in questionResponseChoicesReport:
    responseChoicesReport.append({ 
      "idResponseChoice": responseChoiceReport.id_chosen_answer,
      "message": responseChoiceReport.message
    })
  messageReportUserDto = {
    "firstName" : questionResponseChoicesReport[0].first_name_user,
    "lastName" : questionResponseChoicesReport[0].last_name_user,
    "date" : questionResponseChoicesReport[0].datetime_response,
    "messageReport": responseChoicesReport
  }
  return messageReportUserDto  

def questionResponsesToFirstQuestionOfFieldDto(firstQuestionResponseField):
  responseFirstQuestionField = []
  for firstQuestionField in firstQuestionResponseField:
    responseFirstQuestionField.append({
      "idResponse": firstQuestionField.id_response,
      "idResponseChoice": firstQuestionField.id_chosen_answer,
      "title": firstQuestionField.content_chosen_answer
    })
  firstQuestionFieldDto = {
    "id" : firstQuestionResponseField[0].id_field,
    "title" : firstQuestionResponseField[0].name_field,
    "responseChoicesFirstQuestion": responseFirstQuestionField
  }
  return firstQuestionFieldDto

