from fastapi import APIRouter, Request

from models.models import FormData
from service.client import Tennis

router = APIRouter(tags=["Main Router"])


@router.post("/tennis-form")
async def register_camp(request: Request):
    return await Tennis.registration(request)


@router.post("/schema", response_model=FormData)
async def form_schema(body: FormData):
    return body
