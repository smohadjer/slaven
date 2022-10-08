import logging

from fastapi import Request, HTTPException, status
from fastapi.responses import RedirectResponse
from fastapi_mail import FastMail, MessageSchema, ConnectionConfig  # type:ignore
from pydantic import ValidationError

from config import conf, get_template
from models.models import FormData


class _Tennis(type):

    async def registration(self, request: Request):  # TODO: Return the Json, for developement we redirect for now
        formatted_training_hours: list[str] = []
        referer = request.headers.get("referer")
        logging.error(f"{referer=}")
        data = await request.form()
        email = data.get("email", "")
        _address = str(data.get("address", "")).replace("+", " ")
        _hours = data.getlist("training_time")

        for i in _hours:
            no_commas = i.replace(",", " ")
            formatted_training_hours.append(no_commas.translate({ord("+"): None}))
        _training_times = ", ".join(formatted_training_hours)

        email_subject = data.get("subject", "").replace("+", " ")

        try:
            resp = FormData(firstname=data.get("firstname", ""), lastname=data.get("lastname", ""), address=_address,
                            city=data.get('city', ""),
                            postalcode=data.get("postalcode", ""), birthday=data.get("birthday", ""),
                            phone=data.get("phone", ""),
                            email=email, training_type=data.getlist("training_type"),
                            training_time=formatted_training_hours, privacy=data.get("privacy", ""))
        except ValidationError as e:
            raise HTTPException(status_code=400, detail=e.errors())

        formatted_training_types = ", ".join(resp.training_type)

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
