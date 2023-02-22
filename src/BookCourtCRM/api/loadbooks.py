from fastapi import (
    APIRouter,
    BackgroundTasks,
    UploadFile,
    File,
    Depends,
)

from fastapi.responses import StreamingResponse

from BookCourtCRM.models.auth import Company
from BookCourtCRM.services.auth import get_current_user
from BookCourtCRM.services.loadbooks import LoadBooksService

router = APIRouter(
    prefix="/load_books",
)


@router.post("/import")
def import_csv(
    background_tasks: BackgroundTasks,
    file: UploadFile = File(...),
    company: Company = Depends(get_current_user),
    loadbooks_service: LoadBooksService = Depends(),
):
    background_tasks.add_task(
        loadbooks_service.import_csv,
        company.id,
        file.file,
    )