'''
This is the main file for the app

This is the test comment for the app
'''

from flask import Flask, render_template, request, Response
from langchain.chat_models import ChatOpenAI
from langchain.prompts import ChatPromptTemplate, MessagesPlaceholder 
from langchain.memory import ConversationBufferMemory
from langchain.chains import LLMChain
from langchain.chat_models import ChatOpenAI
from langchain.schema import StrOutputParser

chat = ChatOpenAI(model_name="gpt-3.5-turbo")

app = Flask(__name__)

def chat_resp(query):
    # Prompt
    prompt = ChatPromptTemplate.from_template("You are ICS Arabia chatbot so answer {query} accordingly")

    # Memory
    memory = ConversationBufferMemory(
        memory_key="chat_history", 
        return_messages=True
    )

    # # Chain
    # chatbot = LLMChain(
    #     llm=llm,
    #     prompt=prompt,
    #     memory=memory
    # )

    runnable = prompt | chat | StrOutputParser()

    # query = "What is AI in 1000 words"
    for chunk in runnable.stream({"query": query}):
        # print(chunk, end="", flush=True)
        yield chunk

def stream_response(query):
    for chunk in chat.stream(query):
        yield chunk.content

@app.route('/', methods=['GET', 'POST'])
def index():
    return "Hello, Welcome to the app"

@app.route('/chat', methods=['GET', 'POST'])
def chat_response():
    query = "What is AI?"
    return Response(chat_resp(query), mimetype='text/event-stream')


if __name__ == '__main__':
    app.run()