from typing import Optional, Union
import logging

from fastapi_mail import ConnectionConfig
from pydantic import BaseSettings
from datetime import datetime

from models.models import FormTrainingChildren, FormTrainingAdult, FormCampChildren
import pathlib

path = pathlib.Path("main.py").resolve().parent.parent


class Settings(BaseSettings):
    MAIL_USERNAME: str
    MAIL_PASSWORD: str
    MAIL_FROM: str
    # MONGO_URI: str
    # DB_NAME: str
    # registration_collection: str = "Registration"

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


def get_html_template(resp: Union[FormTrainingAdult, FormCampChildren, FormTrainingChildren],
                      children: bool,
                      formatted_training_types: Optional[str] = None, _training_times: Optional[str] = None):
    template = f"""
            <html>
                <body>

               <table>
                <tr valign="top">
                    <td>Anmeldungsdatum:</td>
                    <td>{resp.timestamp.strftime("%d/%m/%Y")}</td>
                  </tr>
              <tr valign="top">
              """
    if children:
        template += "<td>Vorname des Kinds:</td>"
    else:
        template += "<td>Vorname:</td>"
    template += f"""
                    <td>{resp.first_name}</td>
                </tr>
                <tr>
              """
    if children:
        template += "<td>Nachname des Kinds:</td>"
    else:
        template += "<td>Nachname:</td>"

    template += f"""        
                <td>{resp.last_name}</td>
              </tr>
          """
    if children:
        template += f"""
                    <tr>
                        <td>Name der Eltern:</td>
                        <td>{resp.name_parent}</td>
                    </tr>
                    <tr valign="top">
                        <td>Geburtsdatum:</td>
                        <td>{resp.birthday.strftime("%d/%m/%Y")}</td>
                    </tr>"""
        
    template += f"""
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
        <td>Telefonnummer:</td>
        <td>{resp.phone}</td>
      </tr>
      <tr valign="top">
        <td>E-Mail:</td>
        <td>{resp.email}</td>
      </tr>"""
    if formatted_training_types:
        template += f"""
                    <tr valign="top">
                        <td>Trainingswunsch:</td>
                        <td>{formatted_training_types}</td>
                        </tr>
                    """
    if _training_times:
        template += f"""
                    <tr valign="top">
                        <td>Trainingszeiten:</td>
                        <td>{_training_times}</td>
                    </tr>
                    """
    if type(resp) == FormTrainingAdult or type(resp) == FormTrainingChildren:
        template += f"""
                    <tr valign="top">
                        <td>Trainingsort:</td>
                        <td>{resp.location}</td>
                    </tr>
                    """
    template += f"""
                <tr valign="top">
                    <td>Weitere Hinweise:</td>
                    <td>{resp.comments}</td>
                </tr>

            </table> 
        </body>
    </html>
    """
    return template
