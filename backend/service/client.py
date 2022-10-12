import logging
from datetime import datetime, date

from fastapi import Request, HTTPException, status
from fastapi.responses import RedirectResponse
from fastapi_mail import FastMail, MessageSchema, ConnectionConfig  # type:ignore
from motor.motor_asyncio import AsyncIOMotorCollection
from pydantic import ValidationError

from config import conf, get_template
from models.models import FormData, FormEvent
from config import settings
from db import client


class _Tennis(type):
    @property
    def registration_collection(self) -> AsyncIOMotorCollection:
        db = settings.DB_NAME
        collection = settings.registration_collection
        return client[db].get_collection(collection)

    async def registration(self, request: Request):  # TODO: Return the Json, for developement we redirect for now
        formatted_training_hours: list[str] = []
        referer = request.headers.get("referer")
        logging.error(f"{referer=}")
        data = await request.form()
        email = data.get("email", "")
        _address = str(data.get("address", "")).replace("+", " ")
        _hours = data.getlist("training_time")
        email_subject = data.get("email_subject", "").replace("+", " ")

        for i in _hours:
            no_commas = i.replace(",", " ")
            formatted_training_hours.append(no_commas.translate({ord("+"): None}))
        _training_times = ", ".join(formatted_training_hours)

        try:
            resp = FormData(
                first_name=data.get("first_name", ""),
                last_name=data.get("last_name", ""),
                address=_address,
                city=data.get('city', ""),
                postal_code=data.get("postal_code", ""),
                birthday=datetime.strptime(data.get("birthday", ""), "%Y-%m-%d"),
                phone=data.get("phone", ""),
                email=email,
                training_type=data.getlist("training_type"),
                training_time=formatted_training_hours,
                privacy=True if data.get("privacy") == "true" else False,
                season=data.get("season", ""),
                year=data.get("year"),
                type=data.get("type", ""),
                age_group=data.get("age_group", ""))
        except ValidationError as e:
            raise HTTPException(status_code=400, detail=e.errors())

        formatted_training_types = ", ".join(resp.training_type)

        form_in_db = FormEvent.parse_obj(resp)
        await self.registration_collection.insert_one(form_in_db.dict())

        try:
            await self.send_mail(subject=email_subject, recipients=email,
                                 html=get_template(resp, formatted_training_types, _training_times))
        except Exception as e:
            raise HTTPException(status_code=400, detail=f"error: {e}")

        return RedirectResponse(url=referer+"slaven/training-anmeldung.html#confirmed",
                                status_code=status.HTTP_303_SEE_OTHER)

    async def send_mail(self, subject: str, recipients: str, html: str) -> None:
        message = MessageSchema(subject=subject, recipients=[recipients], html=html, subtype="html")
        fm: FastMail = FastMail(conf)
        await fm.send_message(message)


class Tennis(metaclass=_Tennis):
    pass
