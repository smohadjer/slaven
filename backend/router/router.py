from fastapi import APIRouter, Request, BackgroundTasks, status
from starlette.concurrency import run_in_threadpool
from starlette.responses import RedirectResponse

from models.models import FormTrainingChildren
from service.client import Tennis

router = APIRouter(tags=["Main Router"])


@router.post("/tennis-form")
async def register_camp(request: Request, b_task: BackgroundTasks):
    referer = request.headers.get("referer")
    await Tennis.registration(request, b_task)
    return RedirectResponse(url=referer + "slaven/training-anmeldung.html#confirmed",
                            status_code=status.HTTP_303_SEE_OTHER)


@router.post("/schema", response_model=FormTrainingChildren)
async def form_schema(body: FormTrainingChildren):
    return body
