from fastapi import FastAPI
from langserve import add_routes
from langchain.prompts import ChatPromptTemplate
from langchain_community.llms import Ollama 
import uvicorn


app=FastAPI(title="Doctor Bot",
        version="1.0",
        description="Doctor bot server"
        )

add_routes(
    app,
    Ollama(),
    path="/ollama")


prompt1 = ChatPromptTemplate.from_messages(
    [
        ("system", """You are Doctor virmani In a reputed hospital in india,
         the user will ask you some queries and you have to answer them with the treatment plan,precautions,treatment and the next step to take precisely,
         also add CONSULT A DOCTOR BEFORE FOLLOWING ANY ADVICE if any health related quer is asked to you,
         dont make up things by yourself or try to answer innovative answers,if you dont know anything just simply deny
         """),
        ("user", "Question:{question}")
    ]
)

prompt2 = ChatPromptTemplate.from_messages(
    [
        ("system", """You are Doctor virmani In a reputed hospital in india,
         the user will ask you some queries and you have to answer the diffrential diagnosis of that query precisely,and give the causes,treatment and treatment plan of all the possible reaponss  
         also add CONSULT A DOCTOR BEFORE FOLLOWING ANY ADVICE if any health related quer is asked to you,
         dont make up things by yourself or try to answer innovative answers,if you dont know anything just simply deny
         """),
        ("user", "Question:{question}")
    ]
)

prompt3 = ChatPromptTemplate.from_template(
    """You are Doctor Virmani in a reputed hospital in India.
     The user has provided the following context and query:
     {context}
     Please answer the query with the differential diagnosis, causes, treatment, and treatment plan.
     Also, add CONSULT A DOCTOR BEFORE FOLLOWING ANY ADVICE if any health-related query is asked to you.
     Don't make up things by yourself or try to answer innovative answers. If you don't know anything, just simply deny."""
)


llm=Ollama(model="llama3")

add_routes(
    app,
     prompt1| llm,
    path='/disease_query'
)

add_routes(
    app,
    prompt2 | llm,
    path='/diffrential_diagnosis'
)

add_routes(
    app,
    prompt3 | llm,
    path='/diffrential_diagnosis_with_context'
)


if __name__=="__main__":
    uvicorn.run(app,host="localhost",port=8000)
    
















