from fastapi import FastAPI, Form, Request, Response, File
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.encoders import jsonable_encoder
import uvicorn 
import os 
import aiofiles 
import json 
import csv 
import threading
import webbrowser

app=FastAPI()
BASE_DIR = os.path.dirname(os.path.dirname(__file__))
app.mount("/static", StaticFiles(directory=os.path.join(BASE_DIR, "static")), name="static")
templates = Jinja2Templates(directory=os.path.join(BASE_DIR, "templates"))

@app.post("/upload")
async def chat(request: Request , pdf_file :bytes =File(), filename :str =Form(...)):
    base_folder='static/docs/'
    if not os.path.exists(base_folder):
        os.makedirs(base_folder)
    pdf_filename=os.path.join(base_folder,filename)
    
    async with aiofiles.open(pdf_filename, 'wb') as f:
        await f.write(pdf_file)
    response_data = jsonable_encoder({"msg": "success", "pdf_filename": pdf_filename})
    return Response(content=json.dumps(response_data), media_type="application/json")
    
    
def get_csv(file_path):
    from helper import llm_pipeline
    answer_generation_chain , ques_list =llm_pipeline(file_path)
    base_folder='static/output/'
    if not os.path.isdir(base_folder):
      
        os.mkdir(base_folder) 
    output_file=base_folder + "QA.csv"
    with open(output_file , "w", newline = "" ,encoding="utf-8") as csvfile: 
        csv_writer= csv.writer(csvfile)
        csv_writer.writerow(["Question" , "Answer"])
        
        for question in ques_list:
            print("Question:", question)
            answer = answer_generation_chain.run(question)
            print("Answer:", answer)
            
            csv_writer.writerow([question , answer])
    return output_file

if __name__ == "__main__":
    if os.environ.get("APP_BROWSER_OPENED") != "1":
        os.environ["APP_BROWSER_OPENED"] = "1"
        threading.Timer(1.0, lambda: webbrowser.open("http://localhost:8080/docs")).start()
    uvicorn.run("app:app", host="0.0.0.0", port=8080, reload=True)