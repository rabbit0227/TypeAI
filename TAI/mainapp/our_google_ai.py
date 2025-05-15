import requests
import json
from google import genai
from google.genai import types


# api_key = ''

# mymodl = "gemini-1.5-flash-latest"

def correctionAi(text, highlight, blacklist):

    api_key = 'AIzaSyDeFNDpPzMoVfzWsckj7Bhsk9VDNXnx6so'
    client = genai.Client(api_key=api_key)

    # myinput = input('enter prompt : ')
    # print(myinput)
    # print("-"*40)
    text_prompt = '''
        From this text
        "{user_text}" and this highlight words in it "{highlighted_text}" and this blacklisted list "{blacklist_text}"
        only return the corrected spelling text and remove the blacklisted words if there is any, make sure to only return the corrected text only.
        '''
    text_prompt = text_prompt.replace('user_text', text)
    text_prompt = text_prompt.replace('highlighted_text', highlight)
    text_prompt = text_prompt.replace('blacklist_text', str(blacklist))

    response = client.models.generate_content(
        model="gemma-3-27b-it",
        contents=[text_prompt],
        config=types.GenerateContentConfig(
        safety_settings=[
            types.SafetySetting(
                category=types.HarmCategory.HARM_CATEGORY_HARASSMENT,
                threshold=types.HarmBlockThreshold.BLOCK_NONE,),
            types.SafetySetting(
                category=types.HarmCategory.HARM_CATEGORY_HATE_SPEECH,
                threshold=types.HarmBlockThreshold.BLOCK_NONE,),
            types.SafetySetting(
                category=types.HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT,
                threshold=types.HarmBlockThreshold.BLOCK_NONE,),
            types.SafetySetting(
                category=types.HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT,
                threshold=types.HarmBlockThreshold.BLOCK_NONE,)

        ]
        )
    )

    return response.text

# runAi()
# print(correctionAi("The atomik apple, slices six way.","The ****** apple, slices six way.",["slices"])[:-2])