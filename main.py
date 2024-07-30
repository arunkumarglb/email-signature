from fastapi import FastAPI, Form, File, UploadFile
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from starlette.requests import Request
from PIL import Image
import io
import base64

app = FastAPI()
templates = Jinja2Templates(directory="templates")


@app.get("/", response_class=HTMLResponse)
async def get_form(request: Request):
    return templates.TemplateResponse("form.html", {"request": request})


@app.post("/generate", response_class=HTMLResponse)
async def generate_signature(
    request: Request,
    design: str = Form(...),
    name: str = Form(...),
    title: str = Form(...),
    company: str = Form(...),
    email: str = Form(...),
    phone: str = Form(...),
    facebook: str = Form(...),
    twitter: str = Form(...),
    linkedin: str = Form(...),
    instagram: str = Form(...),
    calendly: str = Form(...),
    profile_picture: UploadFile = File(None),
    company_logo: UploadFile = File(None),
):
    profile_image_b64 = None
    company_logo_b64 = None

    if profile_picture:
        profile_image_b64 = await convert_to_base64(profile_picture)

    if company_logo:
        company_logo_b64 = await convert_to_base64(company_logo)
    print('template_name', design)
    if design == "concept1":
        template_name = "signature.html"

    elif design == "concept2":
        template_name = "signature2.html"

    elif design == "concept3":
        template_name = "signature3.html"
    else:
        # Handle default case or error handling if needed
        template_name = "signature.html"

    return templates.TemplateResponse(template_name, {
        "request": request,
        "name": name,
        "title": title,
        "company": company,
        "email": email,
        "phone": phone,
        "facebook": facebook,
        "twitter": twitter,
        "linkedin": linkedin,
        "instagram": instagram,
        "calendly": calendly,
        "profile_image": profile_image_b64,
        "company_logo": company_logo_b64,
    })


async def convert_to_base64(file: UploadFile):
    image = Image.open(io.BytesIO(await file.read()))
    buffered = io.BytesIO()
    image.save(buffered, format="PNG")
    return base64.b64encode(buffered.getvalue()).decode("utf-8")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
