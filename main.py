from fastapi import FastAPI, Form, File, UploadFile
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from starlette.requests import Request
from PIL import Image
import io
import base64

app = FastAPI()
templates = Jinja2Templates(directory="templates")

font_mapping = {
    "arial": "'Arial', sans-serif",
    "verdana": "'Verdana', sans-serif",
    "helvetica": "'Helvetica', sans-serif",
    "georgia": "'Georgia', serif",
    "tahoma": "'Tahoma', sans-serif",
    "times-new-roman": "'Times New Roman', serif",
    "trebuchet-ms": "'Trebuchet MS', sans-serif",
    "calibri": "'Calibri', sans-serif",
    "garamond": "'Garamond', serif",
    "lucida-sans": "'Lucida Sans', sans-serif"
}


@app.get("/", response_class=HTMLResponse)
async def get_form(request: Request):
    return templates.TemplateResponse("form.html", {"request": request})


@app.post("/generate", response_class=HTMLResponse)
async def generate_signature(
    request: Request,
    design: str = Form(...),
    name: str = Form(...),
    title: str = Form(...),
    company: str = Form(None),
    email: str = Form(None),
    phone: str = Form(None),
    facebook: str = Form(None),
    twitter: str = Form(None),
    linkedin: str = Form(None),
    instagram: str = Form(None),
    calendly: str = Form(None),
    profile_picture: UploadFile = File(None),
    company_logo: UploadFile = File(None),
    colorcode: str = Form(None),
    fontfamily: str = Form(...),
    border_shape: str = Form(...)
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

    if not colorcode:
        colorcode = "#5a76ff"

    # Determine border radius based on border shape
    if border_shape == "square":
        border_radius = "0px"
    elif border_shape == "c-square":
        border_radius = "10%"
    elif border_shape == "circle":
        border_radius = "50%"
    else:
        border_radius = "50%"

    # Retrieve the CSS value for the selected font family
    fontfamily_css = font_mapping.get(fontfamily, "'Arial', sans-serif")

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
        "colorcode": colorcode,
        "fontfamily": fontfamily_css,
        "border_radius": border_radius,
    })


async def convert_to_base64(file: UploadFile):
    image = Image.open(io.BytesIO(await file.read()))
    buffered = io.BytesIO()
    image.save(buffered, format="PNG")
    return base64.b64encode(buffered.getvalue()).decode("utf-8")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
