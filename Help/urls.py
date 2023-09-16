from django.urls import path
from .views import HelpTopics, HelpSingleTopic, HelpSubmitRequest, centre_aide_question

urlpatterns = [
    path('helpTopics/',HelpTopics, name='helpTopics'),
    path('helpSingleTopic/', HelpSingleTopic, name='helSingleTopic'),
    path('helpSubmitRequest/', HelpSubmitRequest.as_view(), name='helpSubmitRequest'),

    # Help topics question
    path("centre-aide-question/", centre_aide_question, name="centre_aide_question")
]