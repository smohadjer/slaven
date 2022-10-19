from fastapi_mail import ConnectionConfig
from pydantic import BaseSettings
from datetime import datetime

from models.models import FormTrainingChildren, FormTrainingAdult
import pathlib

path = pathlib.Path("main.py").resolve().parent.parent


class Settings(BaseSettings):
    MAIL_USERNAME: str
    MAIL_PASSWORD: str
    MAIL_FROM: str

# specify .env file location as Config attribute
    class Config:
        env_file: str = f"{path}/.env"


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


def get_training_children_template(resp: FormTrainingChildren, formatted_training_types, _training_times):
    template = f"""
                <html>
            <body>

           <table>
            <tr valign="top">
                <td>Anmeldungsdatum:</td>
                <td>{resp.timestamp.strftime("%d/%m/%Y")}</td>
              </tr>
          <tr valign="top">
            <td>Vorname des Kinds:</td>
            <td>{resp.first_name}</td>
          </tr>
                <tr>
            <td>Nachname des Kinds:</td>
            <td>{resp.last_name}</td>
          </tr>
          </tr>
                <tr>
            <td>Name der Eltern:</td>
            <td>{resp.name_parent}</td>
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
            <td>{resp.postal_code}</td>
          </tr>
          <tr valign="top">
            <td>Geburtsdatum:</td>
            <td>{resp.birthday.strftime("%d/%m/%Y")}</td>
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
          <tr valign="top">
            <td>Ort:</td>
            <td>{resp.location}</td>
          </tr>
          <tr valign="top">
            <td>Weitere Hinweise:</td>
            <td>{resp.comments}</td>
          </tr>

    </table> 
    </body>
                </html>
                """
    return template


def get_adult_training_form(resp: FormTrainingAdult, _training_times):
    template = f"""
                    <html>
                <body>

               <table>
               <tr valign="top">
                <td>Anmeldungsdatum:</td>
                <td>{resp.timestamp.strftime("%d/%m/%Y")}</td>
              </tr>
              <tr valign="top">
                <td>Vorname:</td>
                <td>{resp.first_name}</td>
              </tr>
                    <tr>
                <td>Nachname:</td>
                <td>{resp.last_name}</td>
              </tr>
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
                <td>{resp.postal_code}</td>
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
                <td>Trainingszeiten:</td>
                <td>{_training_times}</td>
              </tr>
              <tr valign="top">
                <td>Ort:</td>
                <td>{resp.location}</td>
              </tr>
              <tr valign="top">
                <td>Weitere Hinweise:</td>
                <td>{resp.comments}</td>
              </tr>

        </table> 
        </body>
                    </html>
                    """
    return template
