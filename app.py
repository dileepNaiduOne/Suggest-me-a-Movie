import streamlit as st
import google.generativeai as genai
from langchain import PromptTemplate, LLMChain
from langchain_google_genai import ChatGoogleGenerativeAI


# Setup Local Environment
import os
from dotenv import load_dotenv
import re
load_dotenv() # Activate the Local Environment
genai.configure(api_key=os.getenv("GOOGLE-API-KEY"))


# Designing the webpage
st.title("Suggest a Movie...")
user_input = st.text_input("Like what movie you want...")



#Template
demo_template = '''
You are a world's top most best movie lover. You are very very accurate in suggesting similar kind of movies. Remember, the suggestion should be very accurate. 
I will be giving you a movie name, suggest top 3 movies which is very similar to the given movie name. The core idea is that if a person is liking a movie, then he should be
liking your suggestion too

The movie name is {text}. Now suggest me top 3 movies only names.'''


demo_template = PromptTemplate(input_variable=["prompt"], 
                                  template = demo_template)

# Intiate the model
llm = ChatGoogleGenerativeAI(model="gemini-pro", api_key = os.getenv("GOOGLE-API-KEY"))


llm_chain = LLMChain(prompt=demo_template, llm=llm)
if len(user_input) != 0:
    suggestion = llm_chain.run(user_input)
    # print(suggestion)
    # print(re.findall(r"\d+\.\s+(.+)", suggestion))

    st.write(suggestion)

