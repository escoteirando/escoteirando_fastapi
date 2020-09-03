import math
import smtplib
import ssl
import time
from email.mime.text import MIMEText
from queue import Queue
from threading import Thread

from src.app import get_logger
from src.cross_cutting import Singleton

logger = get_logger(__name__)


@Singleton
class MailerService:
    def __init__(self, config):
        self.smtp_host = config.MAILER_SMTP_HOST
        self.smtp_port = config.MAILER_SMTP_PORT
        self.smtp_user = config.MAILER_SMTP_USER
        self.smtp_pass = config.MAILER_SMTP_PASS
        self.smtp_ssl = config.MAILER_SMTP_SSL
        self.sender_email = config.MAILER_SENDER_EMAIL
        self.sender_name = config.MAILER_SENDER_NAME
        self.send_interval = math.ceil((60 * 60) / config.MAILER_THROTTLE)
        self.email_queue = Queue()
        self.last_sent = 0
        self.is_sending = False
        logger.info("INIT")

    def send(self, to_email: str, subject: str, body: str) -> bool:
        self.email_queue.put((to_email, subject, body))
        self.send_thread_start()

    def send_mail_smtp(self, to_email: str, subject: str, body: str):
        success = False
        try:
            msg = MIMEText(body)
            msg["Subject"] = subject
            msg["From"] = self.sender_email
            msg["To"] = to_email

            # Create a secure SSL context
            context = ssl.create_default_context()
            with smtplib.SMTP_SSL(
                self.smtp_host, self.smtp_port, context=context
            ) as server:
                server.ehlo()

                server.login(self.smtp_user, self.smtp_pass)
                server.send_message(msg)
                # server.sendmail(self.sender_email, to_email, email_text)
            success = True
        except Exception as exc:
            logger.error("Error sending email: %s", exc)

        return success

    def send_thread_start(self):
        if self.is_sending:
            return
        try:
            send_thread = Thread(target=self.send_all, name="MailerThread")

            send_thread.start()
        except Exception as exc:
            logger.error("Error on start mailer thread %s", exc)

    def send_all(self):
        logger.info("Starting sending emails")
        sent_ok, sent_error = 0, 0
        try:
            self.is_sending = True
            while not self.email_queue.empty():
                wait_interval = time.time() - self.last_sent
                if wait_interval < self.send_interval:
                    logger.info(
                        "Waiting %s seconds...", self.send_interval - wait_interval
                    )
                    time.sleep(self.send_interval - wait_interval)

                to_email, subject, body = self.email_queue.get()
                if self.send_mail_smtp(to_email, subject, body):
                    sent_ok += 1
                else:
                    sent_error += 1
                self.last_sent = time.time()
        except Exception as exc:
            sent_error += 1
            logger.error("Error sending email: %s", exc)
        finally:
            if sent_error == 0:
                logger.info("Sent %s emails", sent_ok)
            elif sent_ok == 0:
                logger.error("All %s emails failed to sending", sent_error)
            else:
                logger.warning(
                    "Sent %s emails and %s failed", sent_error + sent_ok, sent_error
                )
            self.is_sending = False
