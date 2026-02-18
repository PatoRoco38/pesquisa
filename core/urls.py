from django.urls import path
from . import views

urlpatterns = [
    path(
        "survey/respond/<str:token>/<int:question_id>/<int:rating>/",
        views.respond,
        name="survey_respond"
    ),
    path("send/<int:recipient_id>/", views.send_survey, name="send_survey"),
]
