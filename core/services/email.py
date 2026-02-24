from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from urllib.parse import quote

def send_survey_email(recipient):
    survey = recipient.survey
    questions = survey.questions.order_by("order")

    token = recipient.token
    reply_email = f"avaliacao+{token}@speedvote.com"

    html_body = "<html><body>"
    html_body += "<p>Olá! Por favor, avalie os itens abaixo (0 a 10):</p>"

    for q in questions:
        html_body += f"<p><strong>{q.text}</strong><br>"

        for r in range(0, 11):
            subject = quote(f"Avaliação — {survey.title}")

            body = quote(
                f"Pesquisa: {survey.title}\n"
                f"Pergunta ID: {q.id}\n"
                f"Nota: {r}\n"
                f"Comentario:\n"
            )

            mailto_link = f"mailto:{reply_email}?subject={subject}&body={body}"

            html_body += (
                f'<a href="{mailto_link}" '
                f'style="margin:2px; padding:6px 8px; '
                f'border:1px solid #ccc; border-radius:4px; '
                f'text-decoration:none; color:#000;">{r}</a>'
            )

        html_body += "</p><br>"

    html_body += (
        "<p>Após escolher a nota, escreva um comentário (opcional) "
        "e envie a resposta.</p>"
    )
    html_body += "</body></html>"

    text_body = (
        "Olá! Avalie os itens clicando na nota desejada "
        "e respondendo este e-mail.\n"
    )

    msg = EmailMultiAlternatives(
        subject=f"Avaliação — {survey.title}",
        body=text_body,
        from_email=settings.DEFAULT_FROM_EMAIL,
        to=[recipient.email],
    )

    msg.attach_alternative(html_body, "text/html")
    msg.send()