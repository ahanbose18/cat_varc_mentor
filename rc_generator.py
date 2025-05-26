import requests
import logging
from openai import OpenAI , OpenAIError, RateLimitError, AuthenticationError
import os
from dotenv import load_dotenv
import streamlit as st

#print(api_key_const)
# Set these as environment variables securely in deployment
# openai.api_key = "sk-9494420cb3834a5fbb1261a0385a84ec"
# openai.api_base = "https://openrouter.ai/api/v1"

# Initialize OpenAI client

def initialize_openai_client():
    try:

        api_key_const = st.secrets["OPENAI_API_KEY"]
        api_url_const = st.secrets["OPENAI_API_URL"]
        client = OpenAI(api_key = api_key_const , base_url= api_url_const)
        #print(client)
        return client
    except AuthenticationError as e:
        logging.error(f"OpenAI API error: {e}")
        return "Error: Failed to generate passage due to an OpenAI API error."




def generate_rc_passage(topic, difficulty='Moderate',passage_length = '400'):
    try:
        client = initialize_openai_client()
        prompt = (
            f"You are a CAT exam content generator. Generate a {difficulty.lower()} difficulty, {passage_length}-word reading comprehension passage "
            f"on the topic '{topic}'. The tone can be neutral, argumentative or exploratory or anything else. Follow the passage with 5 Questions including but not limited to: Tone, Inference, Main Idea. Also include questions on Specific Detail, Logical Reasoning. Give 4 answer choices for each question. Format:\n\nPassage:\n<text>\n\nQuestions:\n1. <question> \nA <Option> \nB <Option> \nC <Option> \nD <Option> \n2. <question> \nA <Option> \nB <Option> \nC <Option> \nD <Option>\n3. <question> \nA <Option> \nB <Option> \nC <Option> \nD <Option>\n4. <question> \nA <Option> \nB <Option> \nC <Option> \nD <Option>\n5. <question> \nA <Option> \nB <Option> \nC <Option> \nD <Option>.\n\n"
            f"After each question, provide the correct answer in the format: Answer: [A/B/C/D]"
            f"Include explanations in depth around 10 to 12 lines as well for each question in the format: Explanation: <explanation>.\n\n"
            f"Ensure the passage is coherent, engaging, and suitable for CAT exam standards. Do not include any answers in the passage itself, only in the answer section.\n\n"
                                                                                                          
        )

        response =   client.chat.completions.create(
            model= st.secrets["OPENAI_API_MODEL"],  # or deepseek-llm
            messages=[{"role": "user", "content": prompt}],
            temperature=0.7,
        )

    

        # print(response)

        # if response.status_code == 200:
        #     return response.json()["response"]
        # else:
        #     raise Exception(f"Error {response.status_code}: {response.text}")
        return response.choices[0].message.content


    except OpenAIError as e:
        logging.error(f"OpenAI API error: {e}")
        return "Error: Failed to generate passage due to an OpenAI API error."

    except Exception as e:
        logging.exception("Unexpected error occurred while generating RC passage.")
        return "Error: An unexpected error occurred while generating the RC passage."




    try:
        response = client.chat.completions.create(
            model= "meta-llama/llama-3.3-8b-instruct:free",
            messages=[
                {
                    "role": "system",
                    "content": "You are an expert in CAT-style Reading Comprehension."
                },
                {
                    "role": "user",
                    "content": (
                        f"Now provide the answers and detailed 10 line explanations for the "
                        f"{difficulty} level RC passage and questions on '{topic}' "
                        "that you just generated."
                    )
                }
            ],
            temperature=0.7,
            max_tokens=600
        )
        return response.choices[0].message.content
    except OpenAIError as e:
        print("OpenAI API error:", e)
        return None
    except Exception as e:
        print("Unexpected error occurred while generating RC answers.", e)
        return None
