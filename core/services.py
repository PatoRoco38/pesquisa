from django.conf import settings
from django.urls import reverse
from django.core.mail import EmailMultiAlternatives

def send_survey_email(recipient):
    survey = recipient.survey
    questions = survey.questions.order_by("order")
    base = settings.SITE_URL

    html_parts = []

    for q in questions:
        buttons = ""
        for r in range(11):
            link = f"{base}{reverse('survey_respond', args=[recipient.token, q.id, r])}"
            buttons += f"""
            <a href="{link}"
               style="margin:4px; padding:6px 10px;
                      border:1px solid #ccc;
                      text-decoration:none;
                      border-radius:4px;
                      color:#000;">
               {r}
            </a>
            """
        html_parts.append(f"<p><strong>{q.text}</strong><br>{buttons}</p>")

    html_body = f"""
    <html>
      <body>
        <p>Olá, por favor avalie abaixo (0 a 10):</p>
        {''.join(html_parts)}
        <p>Se quiser comentar, basta responder este e-mail.</p>
      </body>
    </html>
    """

    text_body = "Olá, avalie a pesquisa clicando nos links."

    msg = EmailMultiAlternatives(
        subject=f"Avaliação: {survey.title}",
        body=text_body,
        from_email=settings.DEFAULT_FROM_EMAIL,
        to=[recipient.email],
    )
    msg.attach_alternative(html_body, "text/html")
    msg.send()
