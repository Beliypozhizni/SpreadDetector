from fastapi import APIRouter, Request, status
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

router = APIRouter(tags=["Templates"])
templates = Jinja2Templates(directory="src/templates")


@router.get("/", response_class=HTMLResponse, status_code=status.HTTP_200_OK)
async def home_page(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})
