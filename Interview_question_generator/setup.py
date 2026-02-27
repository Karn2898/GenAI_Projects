from setuptools import find_packages , setup
setup(name="Interview question Generator",
      version="0.0.0",
      author="Tamaghna Sarkar",
      author_email="tamaghna5@gmail.com",
      packages=find_packages(),
      install_requires=[]
)
 
@app.post("/upload")
async def chat(request: Request , pdf_file :bytes =File(), filename :str =Form(...)):
    base_folder='static/docs/'
    if not os.path.exists(base_folder):
        os.makedirs(base_folder)
    pdf_filename=os.path.join(base_folder,filename)
    
    async with aiofiles.open(pdf_filename, 'wb') as f:
        await f.write(pdf_file)
    response_data= jsonable_encoder(json.dumps({"msg": 'success' , "pdf_filename": pdf_filename}))  res=Response(response_data) return res
    
    
def get_csv(file_path):
    answer_generation_chain , ques_list =llm_pipeline(file_path)
    base_folder='static/output/'
    if not os.path.isdir(base_folder):
        