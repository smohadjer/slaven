from fastapi_mail import ConnectionConfig
from pydantic import BaseSettings

from models.models import FormData


class Settings(BaseSettings):
    MAIL_USERNAME: str
    MAIL_PASSWORD: str
    MAIL_FROM: str

# specify .env file location as Config attribute
    class Config:
        env_file: str = ".env"


settings = Settings()


conf = ConnectionConfig(
    MAIL_USERNAME=settings.MAIL_USERNAME,
    MAIL_PASSWORD=settings.MAIL_PASSWORD,
    MAIL_FROM=settings.MAIL_FROM,
    MAIL_PORT=587,
    MAIL_SERVER="smtp.gmail.com",
    MAIL_TLS=True,
    MAIL_SSL=False
)


def get_template(resp: FormData, formatted_training_types, _training_times):
    template = f"""
                <html>
            <body>

           <table>
          <tr valign="top">
            <td>Vorname:</td>
            <td>{resp.firstname}</td>
          </tr>
                <tr>
            <td>Nachname:</td>
            <td>{resp.lastname}</td>
          </tr>
          <tr valign="top">
            <td>Straße und Hausnr:</td>
            <td>{resp.address}</td>
          </tr>
          <tr valign="top">
            <td>Stadt:</td>
            <td>{resp.city}</td>
          </tr>
          <tr valign="top">
            <td>Postleitzahl:</td>
            <td>{resp.postalcode}</td>
          </tr>
          <tr valign="top">
            <td>Geburtsdatum:</td>
            <td>{resp.birthday}</td>
          </tr>
          <tr valign="top">
            <td>Telefonnummer:</td>
            <td>{resp.phone}</td>
          </tr>
          <tr valign="top">
            <td>E-Mail:</td>
            <td>{resp.email}</td>
          </tr>
          <tr valign="top">
            <td>Trainingswunsch:</td>
            <td>{formatted_training_types}</td>
          </tr>
          <tr valign="top">
            <td>Trainingszeiten:</td>
            <td>{_training_times}</td>
          </tr>

    </table> 
    </body>
                </html>
                """
    return template
