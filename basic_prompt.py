from google import genai
import rich
from rich.markdown import Markdown

client = genai.Client()

response = client.models.generate_content(
    model='gemini-3.5-flash-lite',
    contents="""We are a business selling logging and monitoring products.
    What are good products to give away at our booth at PyCon?"""
)

# print(response.text)
rich.print(Markdown(response.text))
print(response.usage_metadata)

