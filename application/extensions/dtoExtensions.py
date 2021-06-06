
def questionResponsesToNextQuestionDto(questionResponseChoices):
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

