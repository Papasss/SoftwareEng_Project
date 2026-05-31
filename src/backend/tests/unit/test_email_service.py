from pathlib import Path
from unittest.mock import Mock, patch

from participium.services.email_service import (
    BaseEmailGateway,
    ConsoleEmailGateway,
    SmtpEmailGateway,
    build_email_gateway,
)


# Base gateway should execute without errors
def test_base_email_gateway_send():
    gateway = BaseEmailGateway()

    gateway.send(
        "user@test.com",
        "Subject",
        "Body",
    )


# Console gateway should create outbox directory
def test_console_gateway_creates_directory(tmp_path):
    outbox = tmp_path / "outbox"

    ConsoleEmailGateway(
        outbox_dir=outbox,
        sender="sender@test.com",
    )

    assert outbox.exists()
    assert outbox.is_dir()


# Console gateway should write email content to file
def test_console_gateway_send(tmp_path):
    gateway = ConsoleEmailGateway(
        outbox_dir=tmp_path,
        sender="sender@test.com",
    )

    gateway.send(
        "receiver@test.com",
        "Hello",
        "Test body",
    )

    files = list(tmp_path.iterdir())

    assert len(files) == 1

    content = files[0].read_text()

    assert "sender@test.com" in content
    assert "receiver@test.com" in content
    assert "Hello" in content
    assert "Test body" in content


# SMTP gateway with TLS and login
@patch("participium.services.email_service.smtplib.SMTP")
def test_smtp_gateway_send_tls_login(mock_smtp):
    smtp_instance = mock_smtp.return_value.__enter__.return_value

    gateway = SmtpEmailGateway(
        host="localhost",
        port=25,
        username="user",
        password="pass",
        sender="sender@test.com",
        use_tls=True,
    )

    gateway.send(
        "receiver@test.com",
        "Subject",
        "Body",
    )

    smtp_instance.starttls.assert_called_once()
    smtp_instance.login.assert_called_once_with(
        "user",
        "pass",
    )
    smtp_instance.send_message.assert_called_once()


# SMTP gateway without TLS and credentials
@patch("participium.services.email_service.smtplib.SMTP")
def test_smtp_gateway_send_without_login(mock_smtp):
    smtp_instance = mock_smtp.return_value.__enter__.return_value

    gateway = SmtpEmailGateway(
        host="localhost",
        port=25,
        username=None,
        password=None,
        sender="sender@test.com",
        use_tls=False,
    )

    gateway.send(
        "receiver@test.com",
        "Subject",
        "Body",
    )

    smtp_instance.starttls.assert_not_called()
    smtp_instance.login.assert_not_called()
    smtp_instance.send_message.assert_called_once()


# Factory should return SMTP gateway
def test_build_email_gateway_smtp():
    settings = Mock()

    settings.mail_backend = "smtp"
    settings.smtp_host = "localhost"
    settings.smtp_port = 25
    settings.smtp_username = "user"
    settings.smtp_password = "pass"
    settings.mail_from = "sender@test.com"
    settings.smtp_use_tls = True

    gateway = build_email_gateway(settings)

    assert isinstance(gateway, SmtpEmailGateway)


# Factory should return Console gateway
def test_build_email_gateway_console(tmp_path):
    settings = Mock()

    settings.mail_backend = "console"
    settings.smtp_host = None
    settings.mail_outbox_dir = tmp_path
    settings.mail_from = "sender@test.com"

    gateway = build_email_gateway(settings)

    assert isinstance(gateway, ConsoleEmailGateway)