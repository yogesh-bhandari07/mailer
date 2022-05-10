import pandas as pd
from typing import Optional
import pydantic
from sqlalchemy import null 
import uvicorn
from fastapi import FastAPI, Request, Form, UploadFile,File
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from databases import Database
import models
import smtplib
import ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import string
from database import SessionLocal
import os

from database import SessionLocal
import requests
from bs4 import BeautifulSoup


sender_email='yk99xxxxxx@gmail.com'
password='xxxxx'

# database = Database("sqlite:///mailer.db")
# db = SessionLocal()

def send_email(receiver_email, html):
    message = MIMEMultipart("alternative")
    message["Subject"] = "Matra Mailer Testing"
    message["From"] = sender_email
    message["To"] = receiver_email

    # Create the HTML version of your message
    

    part1 = MIMEText(html, "html")
    message.attach(part1)

    # Create secure connection with server and send email
    context = ssl.create_default_context()
    with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
        server.login(sender_email, password)
        server.sendmail(
            sender_email, receiver_email, message.as_string()
        )


# Start fastapi application
app = FastAPI()
# database on & off
# @app.on_event("startup")
# async def database_connect():
#     await database.connect()

# @app.on_event("shutdown")
# async def database_disconnect():
    # await database.disconnect()

# add static files and templates
app.mount("/static", StaticFiles(directory="./static"), name="static")
templates = Jinja2Templates(directory="./templates")

# Render Home page
@app.get("/", response_class=HTMLResponse)
async def landing_page(request: Request):
    return templates.TemplateResponse('index.html', {'request': request})


@app.post("/submit", response_class=HTMLResponse)
async def submit(request: Request,mailer: Optional[UploadFile]=File(None),csv: UploadFile=File(...),client:str=Form(...),mailer_url:Optional[str]=None,mailer_code:Optional[str]=None):


    csv=pd.read_csv(csv.file, sep=',')
    contents = await mailer.read()
    print('content',len(content))
    
    if contents!=None:
        dir_path = os.path.dirname(os.path.realpath(__file__))
        filename = f'{dir_path}/static/assets/uploads/{mailer.filename}'
        f = open(f'{filename}', 'wb')
        content = await mailer.read()
        f.write(content)
        f.close()
        html_mailer = open(f'{dir_path}/static/assets/uploads/{mailer.filename}', "r")
        html=html_mailer.read()
        html_mailer.close()
        os.remove(f'{dir_path}/static/assets/uploads/{mailer.filename}')
        
    elif mailer_url!=None:
        print('mailer_url')
        URL = mailer_url
        page = requests.get(URL)
        html = BeautifulSoup(page.content, "html.parser")

    elif mailer_code!=None:
        print('mailer_code')
        html=mailer_code



    
    mails=csv.Email    
    for i in mails:
        send_email(i, html)

    return templates.TemplateResponse('final-page.html', {'request': request})


if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, log_level="info", reload=True)