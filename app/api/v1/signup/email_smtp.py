from fastapi import BackgroundTasks
from fastapi_mail import FastMail, MessageSchema, ConnectionConfig
import random

from config import settings
from db.redis import get_redis_client

conf = ConnectionConfig(
    MAIL_USERNAME=settings.MAIL_USERNAME,
    MAIL_PASSWORD=settings.MAIL_PASSWORD,
    MAIL_FROM=settings.MAIL_FROM,
    MAIL_PORT=settings.MAIL_PORT,
    MAIL_SERVER=settings.MAIL_SERVER,
    MAIL_FROM_NAME=settings.MAIL_FROM_NAME,
    MAIL_STARTTLS=True,
    MAIL_SSL_TLS=False,
    USE_CREDENTIALS=True,
    TEMPLATE_FOLDER="./api/v1/signup/",
)


def create_email_body(code: int):
    return (
        """
    <!DOCTYPE html>
    <html lang="en" xmlns="http://www.w3.org/1999/xhtml" xmlns:v="urn:schemas-microsoft-com:vml" xmlns:o="urn:schemas-microsoft-com:office:office">
    <head>
        <meta charset="utf-8"> 
        <meta name="viewport" content="width=device-width"> 
        <meta http-equiv="X-UA-Compatible" content="IE=edge"> 
        <meta name="x-apple-disable-message-reformatting"> 
        <title>AWS Builder ID Email Verification</title>

        <style>
            html,
            body {
                margin: 0 auto !important;
                padding: 0 !important;
                height: 100% !important;
                width: 100% !important;
                font-family: "Amazon Ember", "Helvetica Neue", Roboto, Arial, sans-serif;
            }

            * {
                -ms-text-size-adjust: 100%;
                -webkit-text-size-adjust: 100%;
            }

            div[style*="margin: 16px 0"] {
                margin: 0 !important;
            }

            table,
            td {
                mso-table-lspace: 0pt !important;
                mso-table-rspace: 0pt !important;
            }

            table {
                border-spacing: 0 !important;
                border-collapse: collapse !important;
                table-layout: fixed !important;
                margin: 0 auto !important;
            }
            table table table {
                table-layout: auto;
            }

            img {
                -ms-interpolation-mode:bicubic;
            }

            *[x-apple-data-detectors],  /* iOS */
            .x-gmail-data-detectors,    /* Gmail */
            .x-gmail-data-detectors *,
            .aBn {
                border-bottom: 0 !important;
                cursor: default !important;
                color: inherit !important;
                text-decoration: none !important;
                font-size: inherit !important;
                font-family: inherit !important;
                font-weight: inherit !important;
                line-height: inherit !important;
            }

            .a6S {
                display: none !important;
                opacity: 0.01 !important;
            }

            img.g-img + div {
                display: none !important;
            }

            .button-link {
                text-decoration: none !important;
            }

            /* iPhone 4, 4S, 5, 5S, 5C, and 5SE */
            @media only screen and (min-device-width: 320px) and (max-device-width: 374px) {
                .email-container {
                    min-width: 320px !important;
                }
            }
            /* iPhone 6, 6S, 7, 8, and X */
            @media only screen and (min-device-width: 375px) and (max-device-width: 413px) {
                .email-container {
                    min-width: 375px !important;
                }
            }
            /* iPhone 6+, 7+, and 8+ */
            @media only screen and (min-device-width: 414px) {
                .email-container {
                    min-width: 414px !important;
                }
            }

            .button-td,
            .button-a {
                transition: all 100ms ease-in;
            }
            .button-td:hover,
            .button-a:hover {
                background: #EB5F07 !important;
                border-color: #EB5F07 !important;
            }

            /* Media Queries */
            @media screen and (max-width: 600px) {
                .email-container {
                    padding-top: 0 !important;
                }

                #emailBodyContainer {
                    border: 0 !important;
                    border-bottom: 1px solid #DDD !important;
                }

                body,
                center {
                    background: #FFF !important;
                }

                #logoContainer td {
                    padding: 20px 0 20px 0 !important;
                }

                #footer {
                    background: #F9F9F9 !important;
                }
            }

        </style>

        <!--[if gte mso 9]>
        <xml>
            <o:OfficeDocumentSettings>
                <o:AllowPNG/>
                <o:PixelsPerInch>96</o:PixelsPerInch>
            </o:OfficeDocumentSettings>
        </xml>
        <![endif]-->

    </head>
    <body width="100%" bgcolor="#F0F2F3" style="margin: 0; mso-line-height-rule: exactly;">
        <center style="width: 100%; background: #F0F2F3; text-align: left;">
        <!--[if mso | IE]>
        <table role="presentation" border="0" cellpadding="0" cellspacing="0" width="100%" bgcolor="#F9F9F9">
        <tr>
        <td>
        <![endif]-->

            <div style="margin: auto; max-width: 600px; padding-top: 50px;" class="email-container">
                <!--[if mso]>
                <table role="presentation" cellspacing="0" cellpadding="0" border="0" width="600" align="center">
                <tr>
                <td>
                <![endif]-->

                <!-- Email Body : BEGIN -->
                <table role="presentation" cellspacing="0" cellpadding="0" border="0" align="center" width="100%" id="emailBodyContainer" style="border: 0px; border-bottom: 1px solid #D6D6D6; max-width: 600px;">

                        <tr>
                            <td class="module" style="background-color: #FFF; color: #444; font-family: 'Amazon Ember',  'Helvetica Neue', Roboto, Arial, sans-serif; font-size: 14px; line-height: 140%; padding: 25px 35px;">
                                
                <h1 style="font-size: 20px; font-weight: bold; line-height: 1.3; margin: 0 0 15px 0;">Verify your FastAPI Template</h1>
                            <p style="margin: 0 0 15px 0; padding: 0 0 0 0;">Hi there, </p>
                <p style="margin: 0 0 15px 0; padding: 0;">Thank you for getting started with FastAPI Template! FastAPI Template is a new template for start new project.</p> 
                <p style="margin: 0; padding: 0;">We want to make sure it's really you. Please enter the following verification code. If you didn't want to create an FastAPI Template, ignore this email. </p> 
                
            
                            </td>
                        </tr>
                        <tr>
                        <td class="module module-otp" style="background-color: #FFF; color: #444; font-family: 'Amazon Ember', 'Helvetica Neue', Roboto, Arial, sans-serif; font-size: 14px; line-height: 140%; padding: 25px 35px; padding-top: 0; text-align: center;">

                                <div class="label" style="font-weight: bold; padding-bottom: 15px;">Verification code:</div>
                                <div class="code" style="color: #000; font-size: 36px; font-weight: bold; padding-bottom: 15px;">"""
        + str(code)
        + """</div>
                                <div class="description" style>This code will expire 10 minutes after it was sent.</div>

                            </td>
                        </tr>
                </table>
                <!-- Email Body : END -->

                <!--[if mso]>
                </td>
                </tr>
                </table>
                <![endif]-->
            </div>
        <!--[if mso | IE]>
        </td>
        </tr>
        </table>
        <![endif]-->
        </center>
    </body>
    </html>
    """
    )


def create_FastMail(email_to: str, body: str):
    message = MessageSchema(
        subject="FastAPI Template",
        recipients=[email_to],
        body=body,
        subtype="html",
    )

    return message


async def create_verify_code(email: str, username: str):
    code = random.randint(100000, 999999)

    redis_client = await get_redis_client()

    await redis_client.set(f"{email}:{username}", code, ex=600)

    return code


async def verify_code(email: str, username: str, code: int):
    redis_client = await get_redis_client()

    stored_code = await redis_client.get(f"{email}:{username}")

    if stored_code == code:
        await redis_client.delete(f"{email}:{username}")
        return True
    else:
        return False


async def send_email_async(email_to: str, username: str):
    code = await create_verify_code(email_to, username)
    body = create_email_body(code)

    message = create_FastMail(email_to, body)

    fm = FastMail(conf)
    await fm.send_message(message)


async def send_email_background(
    background_tasks: BackgroundTasks, email_to: str, username: str
):
    code = await create_verify_code(email_to, username)
    body = create_email_body(code)

    message = create_FastMail(email_to, body)

    fm = FastMail(conf)

    background_tasks.add_task(fm.send_message, message)
