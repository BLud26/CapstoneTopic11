
from google import genai
from google.genai import types
from google.genai.types import GenerateContentConfig
import rich
from rich.markdown import Markdown
import sys
import os
import chromadb
from chromadb import Documents, EmbeddingFunction, Embeddings
import pandas



client = genai.Client()

class GeminiEmbeddingFunction(EmbeddingFunction):
    document_mode = True # true = generating embeddings, False = searching for embeddings in the db

    def __init__(self):
        pass

    def __call__(self, input: Documents):
        if self.document_mode:
            embedding_task = 'retrieval_document'
        else:
            embedding_task = 'retrieval_query'

        response = client.models.embed_content(
            model='gemini-embedding-001',
            contents=input,
            config=types.EmbedContentConfig(
                task_type=embedding_task
            )
        )

        return [e.values for e in response.embeddings] #list comprehension

embed_function = GeminiEmbeddingFunction()
embed_function.document_mode = True # generate embedding mode

chroma_client = chromadb.PersistentClient(path='./chroma_db')
db = chroma_client.get_or_create_collection(name='zoomies_clothes', embedding_function=embed_function)

with open('sporty_products.csv', 'r') as file:
    clothing_data = pandas.read_csv(file)
    ids = clothing_data.style_number.astype(str).tolist()
    documents = list(clothing_data.product_description)

db.upsert(
    ids=ids,
    documents=documents
)

embed_function.document_mode = False # querying the database, finding relevant documents

# query = 'What are the best pants for running in winter'
# results = db.query(query_texts=[query], n_results=5) # how many results to return
# [all_items] = results['documents']
# print(all_items)


chat = client.chats.create(model='gemini-3.5-flash-lite')

try:
    with open('chat_system_instruction.txt', 'r') as f:
        system_instruction = f.read()
except:
    print('Missing system instruction, quitting')
    sys.exit()

while True:
    question = input('Enter your message>')

    # Perform a RAG search to find relevant documents from the database


    results = db.query(query_texts=[question], n_results=5) # how many results to return
    [all_items] = results['documents']
    print(all_items)

    # Create a prompt that includes those documents

    prompt_with_rag = f"""The user has the following question
    
    USER_QUESTION: {question}
    
    Here is information from the product database that may help answer the user's question.
    
    """

    for item in all_items:
        item_one_line = item.replace('\n', ' ')
        prompt_with_rag += f"PRODUCT: {item_one_line}"
    print(prompt_with_rag)



    response = chat.send_message(
        prompt_with_rag,
        config=GenerateContentConfig(
            system_instruction=system_instruction
        )
    )

    rich.print(Markdown(response.text))
    print(response.usage_metadata)

