import imaplib
import email
from email.header import decode_header

IMAP_SERVER = "imap.gmail.com"
EMAIL_ACCOUNT = "avaliacao@speedvote.com"
PASSWORD = "SENHA_AQUI"

def read_inbox():
    mail = imaplib.IMAP4_SSL(IMAP_SERVER)
    mail.login(EMAIL_ACCOUNT, PASSWORD)

    mail.select("inbox")

    status, messages = mail.search(None, "UNSEEN")

    for num in messages[0].split():
        status, data = mail.fetch(num, "(RFC822)")
        raw_email = data[0][1]

        msg = email.message_from_bytes(raw_email)

        subject, encoding = decode_header(msg["Subject"])[0]
        if isinstance(subject, bytes):
            subject = subject.decode(encoding or "utf-8")

        to_address = msg["To"]

        print("Assunto:", subject)
        print("Para:", to_address)

        # Corpo do e-mail
        if msg.is_multipart():
            for part in msg.walk():
                if part.get_content_type() == "text/plain":
                    body = part.get_payload(decode=True).decode()
                    print("Corpo:", body)
        else:
            body = msg.get_payload(decode=True).decode()
            print("Corpo:", body)

    mail.logout()