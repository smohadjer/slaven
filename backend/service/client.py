import asyncio
import logging
from datetime import datetime

from fastapi import Request, HTTPException, BackgroundTasks
from fastapi_mail import FastMail, MessageSchema, ConnectionConfig  # type:ignore
from motor.motor_asyncio import AsyncIOMotorCollection  # type:ignore
from pydantic import ValidationError

from config import conf, get_training_children_template
from models.models import FormTrainingChildren, AgeGroup, Types
# from db import client


class _Tennis(type):
    # @property
    # def registration_collection(self) -> AsyncIOMotorCollection:
    #     db = settings.DB_NAME
    #     collection = settings.registration_collection
    #     return client[db].get_collection(collection)

    async def registration(self, request: Request, b_task: BackgroundTasks) -> None:
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

        for i in _hours:
            no_commas = i.replace(",", " ")
            formatted_training_hours.append(no_commas.translate({ord("+"): None}))
        _training_times = ", ".join(formatted_training_hours)

        if age_group == AgeGroup.JUGEND.value:
            if type_of_form == Types.TRAINING:
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

                html = get_training_children_template(resp, formatted_training_types, _training_times)
                b_task.add_task(self.background_mail, email_subject, email, html)
                logging.info("Sending mail in background")
            elif type_of_form == Types.CAMP:
                raise HTTPException(status_code=400, detail=f"{type_of_form} is not supported right now")
        elif age_group == AgeGroup.ERWACHSENE:
            if type_of_form == Types.TRAINING:
                raise HTTPException(status_code=400, detail=f"{type_of_form} is not supported right now")
            elif type_of_form is Types.CAMP:
                raise HTTPException(status_code=400, detail=f"{type_of_form} is not supported right now")

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
