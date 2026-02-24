import imaplib
import email
import re

from django.conf import settings
from django.core.management.base import BaseCommand

from survey.models import SurveyRecipient, SurveyResponse


class Command(BaseCommand):
    help = "Busca respostas de pesquisas na caixa de entrada"

    def handle(self, *args, **kwargs):
        self.stdout.write("🔌 Conectando ao servidor de e-mail...")

        mail = imaplib.IMAP4_SSL(settings.IMAP_SERVER)
        mail.login(settings.IMAP_EMAIL, settings.IMAP_PASSWORD)

        mail.select("inbox")

        status, messages = mail.search(None, "UNSEEN")

        if status != "OK":
            self.stdout.write(self.style.ERROR("Erro ao buscar mensagens"))
            return

        message_numbers = messages[0].split()

        if not message_numbers:
            self.stdout.write("📭 Nenhuma resposta nova.")
            mail.logout()
            return

        self.stdout.write(f"📨 {len(message_numbers)} mensagem(ns) encontrada(s).")

        for num in message_numbers:
            status, data = mail.fetch(num, "(RFC822)")
            raw_email = data[0][1]
            msg = email.message_from_bytes(raw_email)

            to_address = msg.get("To", "")

            token = self.extract_token(to_address)

            if not token:
                self.stdout.write("⚠️ Token não encontrado — ignorando")
                continue

            try:
                recipient = SurveyRecipient.objects.get(token=token)
            except SurveyRecipient.DoesNotExist:
                self.stdout.write(f"⚠️ Token inválido: {token}")
                continue

            if recipient.responded:
                self.stdout.write(f"⚠️ Resposta duplicada ignorada: {recipient.email}")
                continue

            body = self.get_email_body(msg)

            nota = self.extract_nota(body)
            comentario = self.extract_comentario(body)

            if nota is None:
                self.stdout.write("⚠️ Nota não encontrada — ignorando")
                continue

            SurveyResponse.objects.create(
                recipient=recipient,
                nota=nota,
                comentario=comentario,
            )

            recipient.responded = True
            recipient.save()

            self.stdout.write(
                self.style.SUCCESS(
                    f"✅ Resposta salva — {recipient.email} | Nota: {nota}"
                )
            )

        mail.logout()
        self.stdout.write("🏁 Processamento finalizado.")

    # -----------------------------
    # Helpers
    # -----------------------------

    def extract_token(self, to_address):
        match = re.search(r'avaliacao\+(.+?)@', to_address)
        return match.group(1) if match else None

    def get_email_body(self, msg):
        if msg.is_multipart():
            for part in msg.walk():
                if part.get_content_type() == "text/plain":
                    return part.get_payload(decode=True).decode(errors="ignore")
        return msg.get_payload(decode=True).decode(errors="ignore")

    def extract_nota(self, body):
        match = re.search(r'Nota:\s*(\d+)', body)
        return int(match.group(1)) if match else None

    def extract_comentario(self, body):
        match = re.search(r'Comentario:\s*(.*)', body, re.DOTALL)
        return match.group(1).strip() if match else ""