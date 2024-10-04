import streamlit as st
import google.generativeai as genai
from langchain import PromptTemplate, LLMChain
from langchain_google_genai import ChatGoogleGenerativeAI
from imdb import IMDb
from PIL import Image
import requests


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
    suggestion_list = re.findall(r"\d+\.\s+(.+)", suggestion)
    print(suggestion_list)

    st.write(f"WoW!!! This is nice movie. And you may also like \n\n{suggestion}\n\nPlease wait, Getting the Posters... ")

    image_link_list = []
    for movie in suggestion_list:
        ia = IMDb()

        movie_object = ia.search_movie(movie)
        id = movie_object[0].getID()
        movie = ia.get_movie(id)
        img_url = movie['cover url']

        image_link_list.append(Image.open(requests.get(img_url, stream=True).raw))

    cols = st.columns(3) 
    cols[0].image(image_link_list[0], width=200)
    cols[1].image(image_link_list[1], width=200)
    cols[2].image(image_link_list[2], width=200)


