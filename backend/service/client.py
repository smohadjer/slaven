import asyncio
import logging
from datetime import datetime

from fastapi import Request, HTTPException, BackgroundTasks, status
from fastapi_mail import FastMail, MessageSchema, ConnectionConfig  # type:ignore
from motor.motor_asyncio import AsyncIOMotorCollection  # type:ignore
from pydantic import ValidationError
from starlette.responses import RedirectResponse

from config import conf, get_html_template
# from db import client
from models.models import FormTrainingChildren, AgeGroup, Types, FormTrainingAdult, FormCampChildren


# from db import client


class _Tennis(type):
    # @property
    # def registration_collection(self) -> AsyncIOMotorCollection:
    #     db = settings.DB_NAME
    #     collection = settings.registration_collection
    #     return client[db].get_collection(collection)

    async def registration(self, request: Request):
        formatted_training_hours: list[str] = []
        referer = request.headers.get("referer")
        logging.error(f"{referer=}")
        data = await request.form()
        email = data.get("email", "")
        _address = str(data.get("address", "")).replace("+", " ")
        _hours = data.getlist("training_time")
        email_subject = data.get("email_subject", "").replace("+", " ")
        city = data.get("city", "").replace("+", " ")
        name_of_parent = data.get("name_parent", "").replace("+", " ")
        age_group = data.get("age_group", "")
        type_of_form = data.get("type", "")
        logging.error(f"{age_group=}")

        for i in _hours:
            no_commas = i.replace(",", " ")
            formatted_training_hours.append(no_commas.translate({ord("+"): None}))
        _training_times = ", ".join(formatted_training_hours)

        if age_group == AgeGroup.JUGEND.value:
            if type_of_form == Types.TRAINING.value:
                try:
                    resp = FormTrainingChildren(
                        first_name=data.get("first_name", ""),
                        last_name=data.get("last_name", ""),
                        name_parent=name_of_parent,
                        address=_address,
                        city=city,
                        postal_code=data.get("postal_code", ""),
                        birthday=datetime.strptime(data.get("birthday", ""), "%Y-%m-%d"),
                        phone=data.get("phone", ""),
                        email=email,
                        location=data.get("training_location", ""),
                        training_type=data.getlist("training_type"),
                        training_time=formatted_training_hours,
                        privacy=True if data.get("privacy") == "true" else False,
                        season=data.get("season", ""),
                        year=data.get("year"),
                        type=data.get("type", ""),
                        age_group=data.get("age_group", ""),
                        comments=data.get("comments", ""))
                except ValidationError as e:
                    raise HTTPException(status_code=400, detail=e.errors())
                formatted_training_types = ", ".join(resp.training_type)

                html = get_html_template(resp, children=True, formatted_training_types=formatted_training_types,
                                         _training_times=_training_times)

                # TODO: remove this try except and use background tasks
                try:
                    await self.send_mail(email_subject, email, html)
                    return RedirectResponse(url=referer + "slaven/training-anmeldung-jugend.html#confirmed",
                                        status_code=status.HTTP_303_SEE_OTHER)

                except Exception as e:
                    raise HTTPException(status_code=400, detail=str(e))


                # b_task.add_task(self.background_mail, email_subject, email, html)
                # logging.info("Sending mail in background")
            elif type_of_form == Types.CAMP.value:
                try:
                    resp = FormCampChildren(
                        first_name=data.get("first_name", ""),
                        last_name=data.get("last_name", ""),
                        name_parent=name_of_parent,
                        address=_address,
                        city=city,
                        postal_code=data.get("postal_code", ""),
                        birthday=datetime.strptime(data.get("birthday", ""), "%Y-%m-%d"),
                        phone=data.get("phone", ""),
                        email=email,
                        privacy=True if data.get("privacy") == "true" else False,
                        season=data.get("season", ""),
                        year=data.get("year"),
                        type=data.get("type", ""),
                        age_group=data.get("age_group", ""),
                        comments=data.get("comments", ""))
                except ValidationError as e:
                    raise HTTPException(status_code=400, detail=e.errors())

                html = get_html_template(resp, children=True, _training_times=_training_times)

                try:
                    await self.send_mail(email_subject, email, html)
                    return RedirectResponse(url=referer + "slaven/camp_sommer_2023.html#confirmed",
                                            status_code=status.HTTP_303_SEE_OTHER)

                except Exception as e:
                    raise HTTPException(status_code=400, detail=str(e))

        elif age_group == AgeGroup.ERWACHSENE:
            if type_of_form == Types.TRAINING:
                try:
                    resp = FormTrainingAdult(
                        first_name=data.get("first_name", ""),
                        last_name=data.get("last_name", ""),
                        address=_address,
                        city=city,
                        postal_code=data.get("postal_code", ""),
                        birthday=datetime.strptime(data.get("birthday", ""), "%Y-%m-%d"),
                        phone=data.get("phone", ""),
                        email=email,
                        location=data.get("training_location", ""),
                        training_time=formatted_training_hours,
                        privacy=True if data.get("privacy") == "true" else False,
                        season=data.get("season", ""),
                        year=data.get("year"),
                        type=data.get("type", ""),
                        age_group=data.get("age_group", ""),
                        comments=data.get("comments", ""))
                except ValidationError as e:
                    raise HTTPException(status_code=400, detail=e.errors())
                html = get_html_template(resp, _training_times=_training_times, children=False)

                try:
                    await self.send_mail(email_subject, email, html)
                    return RedirectResponse(url=referer + "slaven/training-anmeldung.html#confirmed",
                                            status_code=status.HTTP_303_SEE_OTHER)

                except Exception as e:
                    raise HTTPException(status_code=400, detail=str(e))

            elif type_of_form is Types.CAMP:
                raise HTTPException(status_code=400, detail=f"{type_of_form} is not supported right now")
        else:
            raise HTTPException(status_code=400, detail=f"{age_group} is not supported right now")

    async def send_mail(self, subject: str, recipients: str, html: str) -> None:
        message = MessageSchema(subject=subject, recipients=[recipients], html=html, subtype="html")
        fm: FastMail = FastMail(conf)
        await fm.send_message(message)
        logging.info(f"Email to {recipients} sent")

    async def background_mail(self, subject: str, recipients: str, html: str):
        loop = asyncio.get_event_loop()
        loop.create_task(self.send_mail(subject, recipients, html))


class Tennis(metaclass=_Tennis):
    pass
