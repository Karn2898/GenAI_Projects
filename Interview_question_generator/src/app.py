from fastapi import FastAPI , Form , Request , Response , File , Depends , HTTPException , status 
from fastapi.responses import RedirectResponse
from fastapi.staticfiles import staticfiles
from fastapi.templating import jsonable_encoder 
import uvicorn 
import os 
import aiofiles 
import json 
import csv 

app=FastAPI()
app.mount("/static", StaticFiles(directory = "static"), name="static")
templates=JinjsTemplates(directory="templates")

@app.get("/")
async def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})