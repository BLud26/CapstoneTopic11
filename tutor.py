from google import genai
from google.genai.types import GenerateContentConfig
import rich
from rich.markdown import Markdown

client = genai.Client()
chat = client.chats.create(model='gemini-3.5-flash-lite')

while True:
    question = input('Enter your message')
    response = chat.send_message(
        #model='gemini-3.5-flash-lite',
        #contents="""Write a problem to calculate the area of a circle.""",
        question,
        config=GenerateContentConfig(
            system_instruction="""You are a helpful programming tutor for Java programming students.
            You can explain concepts and programs but dont' give the users the answers. If the 
            user asks for code, ask them questions and explain concepts to help them write it 
            themselves. Be positive and encouraging at all times."""
        )
    )

    rich.print(Markdown(response.text))

