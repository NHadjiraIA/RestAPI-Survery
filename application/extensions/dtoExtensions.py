
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
    "responseChoices": responseChoices
  }
  return nextQuestionDto

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

