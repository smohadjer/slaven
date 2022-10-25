import asyncio
import logging
from datetime import datetime
from urllib.parse import unquote_plus

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
        email = unquote_plus(data.get("email", ""))
        _address = unquote_plus(str(data.get("address", "")))
        _hours = [unquote_plus(i) for i in (data.getlist("training_time"))]
        email_subject = unquote_plus(data.get("email_subject", ""))
        city = unquote_plus(data.get("city", ""))
        name_of_parent = unquote_plus(data.get("name_parent", ""))
        age_group = unquote_plus(data.get("age_group", ""))
        type_of_form = unquote_plus(data.get("type", ""))
        first_name = unquote_plus(data.get("first_name", ""))
        last_name = unquote_plus(data.get("last_name", ""))
        postal_code = unquote_plus(data.get("postal_code", ""))
        birthday = datetime.strptime(data.get("birthday", ""), "%Y-%m-%d")
        phone = unquote_plus(data.get("phone", ""))
        location = unquote_plus(data.get("training_location", ""))
        training_group = data.getlist("training_group")
        privacy = True if data.get("privacy") == "true" else False
        season = unquote_plus(data.get("season", ""))
        year = unquote_plus(data.get("year"))
        _type = unquote_plus(data.get("type", ""))
        comments = unquote_plus(data.get("comments", ""))
        logging.error(f"{age_group=}")

        for i in _hours:
            no_commas = i.replace(",", " ")
            formatted_training_hours.append(no_commas)
        _training_times = "<br /> ".join(formatted_training_hours)

        if age_group == AgeGroup.JUGEND.value:
            if type_of_form == Types.TRAINING.value:
                try:
                    resp = FormTrainingChildren(
                        first_name=first_name,
                        last_name=last_name,
                        name_parent=name_of_parent,
                        address=_address,
                        city=city,
                        postal_code=postal_code,
                        birthday=birthday,
                        phone=phone,
                        email=email,
                        location=location,
                        training_group=training_group,
                        training_time=formatted_training_hours,
                        privacy=privacy,
                        season=season,
                        year=year,
                        type=_type,
                        age_group=age_group,
                        comments=comments)
                except ValidationError as e:
                    raise HTTPException(status_code=400, detail=e.errors())
                formatted_training_groups = ", ".join(resp.training_group)

                html = get_html_template(resp, children=True, formatted_training_groups=formatted_training_groups,
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
                        first_name=first_name,
                        last_name=last_name,
                        name_parent=name_of_parent,
                        address=_address,
                        city=city,
                        postal_code=postal_code,
                        birthday=birthday,
                        phone=phone,
                        email=email,
                        privacy=privacy,
                        season=season,
                        year=year,
                        type=_type,
                        age_group=age_group,
                        comments=comments)
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
                        first_name=first_name,
                        last_name=last_name,
                        address=_address,
                        city=city,
                        postal_code=postal_code,
                        birthday=birthday,
                        phone=phone,
                        email=email,
                        location=location,
                        training_time=formatted_training_hours,
                        privacy=privacy,
                        season=season,
                        year=year,
                        type=_type,
                        age_group=age_group,
                        comments=comments)
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
