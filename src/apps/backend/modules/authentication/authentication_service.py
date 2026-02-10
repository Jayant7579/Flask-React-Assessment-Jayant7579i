import urllib.parse
from dataclasses import asdict

from modules.account.types import Account, PhoneNumber
from modules.authentication.internals.access_token.access_token_util import AccessTokenUtil
from modules.authentication.internals.otp.otp_util import OTPUtil
from modules.authentication.internals.otp.otp_writer import OTPWriter
from modules.authentication.internals.password_reset_token.password_reset_token_reader import PasswordResetTokenReader
from modules.authentication.internals.password_reset_token.password_reset_token_util import PasswordResetTokenUtil
from modules.authentication.internals.password_reset_token.password_reset_token_writer import PasswordResetTokenWriter
from modules.authentication.types import (
    OTP,
    AccessToken,
    AccessTokenPayload,
    CreateOTPParams,
    OTPBasedAuthAccessTokenRequestParams,
    PasswordResetToken,
    VerifyOTPParams,
)
from modules.config.config_service import ConfigService
from modules.notification.email_service import EmailService
from modules.notification.sms_service import SMSService
from modules.notification.types import EmailRecipient, EmailSender, SendEmailParams, SendSMSParams


class AuthenticationService:
    @staticmethod
    def create_access_token_by_username_and_password(*, account: Account) -> AccessToken:
        result = AccessTokenUtil.generate_access_token(account=account)
        return result

    @staticmethod
    def create_access_token_by_phone_number(
        *, params: OTPBasedAuthAccessTokenRequestParams, account: Account
    ) -> AccessToken:
        otp = AuthenticationService.verify_otp(
            params=VerifyOTPParams(phone_number=params.phone_number, otp_code=params.otp_code)
        )
        AccessTokenUtil.validate_otp_for_access_token(otp=otp)

        result = AccessTokenUtil.generate_access_token(account=account)
        return result

    @staticmethod
    def verify_access_token(*, token: str) -> AccessTokenPayload:
        result = AccessTokenUtil.verify_access_token(token=token)
        return result

    @staticmethod
    def create_password_reset_token(params: Account) -> PasswordResetToken:
        token = PasswordResetTokenUtil.generate_password_reset_token()
        password_reset_token = PasswordResetTokenWriter.create_password_reset_token(params.id, token)
        AuthenticationService.send_password_reset_email(
            account_id=params.id, first_name=params.first_name, username=params.username, password_reset_token=token
        )
        result = password_reset_token
        return result

    @staticmethod
    def get_password_reset_token_by_account_id(account_id: str) -> PasswordResetToken:
        result = PasswordResetTokenReader.get_password_reset_token_by_account_id(account_id)
        return result

    @staticmethod
    def set_password_reset_token_as_used_by_id(password_reset_token_id: str) -> PasswordResetToken:
        result = PasswordResetTokenWriter.set_password_reset_token_as_used(password_reset_token_id)
        return result

    @staticmethod
    def verify_password_reset_token(account_id: str, token: str) -> PasswordResetToken:
        result = PasswordResetTokenReader.verify_password_reset_token(account_id=account_id, token=token)
        return result

    @staticmethod
    def send_password_reset_email(account_id: str, first_name: str, username: str, password_reset_token: str) -> None:
        web_app_host = ConfigService[str].get_value(key="web_app_host")
        default_email = ConfigService[str].get_value(key="mailer.default_email")
        default_email_name = ConfigService[str].get_value(key="mailer.default_email_name")
        forgot_password_mail_template_id = ConfigService[str].get_value(key="mailer.forgot_password_mail_template_id")

        template_data = {
            "first_name": first_name,
            "password_reset_link": f"{web_app_host}/accounts/{account_id}/reset_password?token={urllib.parse.quote(password_reset_token)}",
            "username": username,
        }

        password_reset_email_params = SendEmailParams(
            template_id=forgot_password_mail_template_id,
            recipient=EmailRecipient(email=username),
            sender=EmailSender(email=default_email, name=default_email_name),
            template_data=template_data,
        )

        EmailService.send_email_for_account(
            account_id=account_id, bypass_preferences=True, params=password_reset_email_params
        )

    @staticmethod
    def create_otp(*, params: CreateOTPParams, account_id: str) -> OTP:
        recipient_phone_number = PhoneNumber(**asdict(params)["phone_number"])
        otp = OTPWriter.create_new_otp(params=params)

        if not OTPUtil.should_use_default_otp_for_phone_number(recipient_phone_number.phone_number):
            send_sms_params = SendSMSParams(
                message_body=f"{otp.otp_code} is your One Time Password (OTP) for verification.",
                recipient_phone=recipient_phone_number,
            )
            SMSService.send_sms_for_account(account_id=account_id, bypass_preferences=True, params=send_sms_params)

        result = otp
        return result

    @staticmethod
    def verify_otp(*, params: VerifyOTPParams) -> OTP:
        result = OTPWriter.verify_otp(params=params)
        return result
