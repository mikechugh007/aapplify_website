from decouple import config
import django.db
from openai import OpenAI

import json
client=OpenAI(api_key=config("OPENAI_API_KEY"))


def gpt_generate_mail(prompt,stream=False):
    print('stream',stream)
    response=client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role":"system","content": "You are an AI email assistant. Your task is to help users compose clear, professional, and polite emails. Consider the context provided by the user and maintain a friendly yet formal tone. Include a proper greeting, body content that addresses the user's intent, and a courteous closing."},
            {"role":"user","content":prompt},
        ],
        stream=stream,
        n=3

    )
    # response=response.parse_obj()
    if not stream:
        contents=[choice.message.content for choice in response.choices]
        # response_json_str=json.dumps(choices)
        print(contents)
        return contents
    


