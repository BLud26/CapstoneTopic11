from google import genai

client = genai.Client()

response = client.models.generate_content(
    model='gemini-3.5-flash-lite',
    contents="""We are a business selling logging and monitoring products.
    What are good products to give away at our booth at PyCon?
    Last year we gave away tote bags, and they were very popular and met out budget."""
)

print(response.text)

