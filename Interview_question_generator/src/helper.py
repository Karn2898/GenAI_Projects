from langchain.docstore.document import Document
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.llms import HuggingFaceEndpoint
from langchain_community.chat_models import ChatHuggingFace
from langchain.prompts import ChatPromptTemplate
from langchain.chains.summarize import load_summarize_chain
from langchain.vectorstores import FAISS
from langchain.chains import RetrievalQA
import os
from dotenv import load_dotenv
from src.prompt import *
from src.helper import llm_pipeline
load_dotenv()
HUGGINGFACE_TOKEN = os.getenv('HUGGINGFACE_TOKEN')
os.environ['HUGGINGFACE_TOKEN'] = HUGGINGFACE_TOKEN
def file_processing(file_path):
    #data preprocessing
    loader=PyPDFLoader(file_path)
    data=loader.load()
    df['data']=df['data'].str.lower()

    def remove_url(data):
      pattern=re.compile(r'http?://S+|.S+')
      return pattern.sub(r'',text)
      remove_url(data)
      
    question_gen=""
    for page in data:
      question_gen+=page.page_content

    from langchain_text_splitters import CharacterTextSplitter, TokenTextSplitter
    split_question_gen=TokenTextSplitter(
        encoding_name="cl100k_base",
        chunk_size=10000,
        chunk_overlap=200
    )

    chunk_ques_gen=split_question_gen.split_text(question_gen)

    from langchain_core.documents import Document
    document_question_gen=[Document(page_content=t) for t in chunk_ques_gen]

    splitter_ans_gen=TokenTextSplitter(
      encoding_name="cl100k_base",
      chunk_size=1000,
      chunk_overlap=100
    )

    document_ans_gen=splitter_ans_gen.split_documents(
        document_question_gen
    )

    return document_question_gen, document_ans_gen

def llm_pipeline(file_path):
    document_question_gen , document_ans_gen = file_processing(file_path)
    
    llm_question_ge_pipeline=ChatHuggingFace(
        temperature= 0.3 ,
        model=""
    )
    
    PROMPT_QUESTIONS=ChatPromptTemplate(template=prompt_template , input_variables =["text"])
    
    REFINE_PROMPT=ChatPromptTemplate(input_variables=["exixting_answer", "text"],
                                     template=refine_template)
    
    ques_gen_chain=load_summarize_chain(ll=llm_ques_gen_pipeline,
                                        chain_type="refine")
    