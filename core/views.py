from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect
from django.utils import timezone
from django.contrib import messages
from .models import Recipient
from .services import send_survey_email
from .models import Recipient, Question, Response

def send_survey(request, recipient_id):
    recipient = get_object_or_404(Recipient, id=recipient_id)
    send_survey_email(recipient)
    messages.success(request, "Pesquisa enviada com sucesso!")
    return redirect("/admin/core/recipient/")

def respond(request, token, question_id, rating):
    recipient = get_object_or_404(Recipient, token=token)
    question = get_object_or_404(Question, id=question_id, survey=recipient.survey)

    Response.objects.update_or_create(
        recipient=recipient,
        question=question,
        defaults={
            "rating": rating,
            "created_at": timezone.now()
        }
    )

    return HttpResponse(
        "<h2>Resposta registrada ✔️</h2>"
        "<p>Você pode fechar esta página.</p>"
    )
