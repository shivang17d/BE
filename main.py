from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from nlp import run_nlp , load_models  # Import your function from the parent directory
from fastapi.responses import JSONResponse
from datetime import datetime

templates = Jinja2Templates(directory="server/templates")

app = FastAPI()
app.mount("/static", StaticFiles(directory="server/static"), name="static")



@app.on_event("startup")
async def startup_event():
    print("Loading NLP models...")
    load_models()  # Assuming you have a function to load NLP models




@app.get("/")
async def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/story1.html")
async def story1(request: Request):
    return templates.TemplateResponse("story1.html", {"request": request})


@app.post("/story1.html")
async def story1(request: Request):
    form_data = await request.form()
    speech_to_text = form_data.get("speechToText", "").lower()
    arr = [speech_to_text]

    # Assuming run_nlp function processes the text and returns the updated image URL
    updated_image_url = run_nlp(arr)
    
    # Append timestamp to image URL
    timestamp = datetime.now().timestamp()
    updated_image_url_with_timestamp = f"{updated_image_url}?timestamp={timestamp}"

    # Return the URL of the updated image with timestamp in JSON format
    return JSONResponse(content={"image_url": updated_image_url_with_timestamp})

@app.get("/story4.html")
async def story1(request: Request):
    return templates.TemplateResponse("story4.html", {"request": request})


@app.post("/story4.html")
async def story1(request: Request):
    form_data = await request.form()
    speech_to_text = form_data.get("speechToText", "").lower()
    arr = [speech_to_text]

    # Assuming run_nlp function processes the text and returns the updated image URL
    updated_image_url = run_nlp(arr)
    
    # Append timestamp to image URL
    timestamp = datetime.now().timestamp()
    updated_image_url_with_timestamp = f"{updated_image_url}?timestamp={timestamp}"

    # Return the URL of the updated image with timestamp in JSON format
    return JSONResponse(content={"image_url": updated_image_url_with_timestamp})


# @app.post("/")
# async def home_post(request: Request):
#     form_data = await request.form()
#     speech_to_text = form_data.get("speechToText", "")  # Retrieve the text from the form field
#     # Now you can do whatever you want with the speech_to_text
#     # For example, you can pass it to your NLP function:
#     speech_to_text=speech_to_text.lower()
#     arr=[speech_to_text]
#     print(arr)
#     run_nlp(arr)  # Assuming run_nlp function processes the text
#     return templates.TemplateResponse("index2.html", {"request": request})
