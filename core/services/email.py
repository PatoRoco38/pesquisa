from django.conf import settings
from django.urls import reverse
from django.core.mail import EmailMultiAlternatives

def send_survey_email(recipient):
    survey = recipient.survey
    questions = survey.questions.order_by("order")

    base_url = settings.SITE_URL

    html_body = "<html><body>"
    html_body += "<p>Olá! Por favor, avalie os itens abaixo (0 a 10):</p>"

    for q in questions:
        html_body += f"<p><strong>{q.text}</strong><br>"

        for r in range(0, 11):
            link = f"{base_url}{reverse('survey_respond', args=[recipient.token, q.id, r])}"
            html_body += (
                f'<a href="{link}" '
                f'style="margin:2px; padding:6px 8px; '
                f'border:1px solid #ccc; border-radius:4px; '
                f'text-decoration:none; color:#000;">{r}</a>'
            )

        html_body += "</p><br>"

    html_body += (
        "<p>Se quiser deixar um comentário, "
        "basta responder este e-mail.</p>"
    )
    html_body += "</body></html>"

    text_body = "Olá! Avalie os itens abaixo respondendo este e-mail.\n"

    msg = EmailMultiAlternatives(
        subject=f"Avaliação — {survey.title}",
        body=text_body,
        from_email=settings.DEFAULT_FROM_EMAIL,
        to=[recipient.email],
    )

    msg.attach_alternative(html_body, "text/html")
    msg.send()
