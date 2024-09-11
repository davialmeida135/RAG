import argparse
from langchain_chroma import Chroma
from langchain.prompts import ChatPromptTemplate
from langchain_community.llms.ollama import Ollama

from get_embedding_function import get_embedding_function
import time
CHROMA_PATH = "chroma"

'''PROMPT_TEMPLATE = """
Answer the question based only on the following context:

{context}

---

Answer the question based on the above context with a limit of 5 sentences: {question}
"""
'''

PROMPT_TEMPLATE = """ 
Responda a pergunta baseado apenas no seguinte contexto:
{context}

---

Responda a pergunta baseado apenas no contexto acima com limite de 5 frases: {question}
"""


def main():
    # Create CLI.
    start_time = time.time() 
    '''parser = argparse.ArgumentParser()
    parser.add_argument("query_text", type=str, help="The query text.")
    args = parser.parse_args()
    parse_time = time.time() - start_time'''
    query_text = "Como funciona a proficiência no BTI?"
    query_rag(query_text)
    query_time = time.time() 
    #print(f"Parse Time: {parse_time}")
    print(f"Query Time: {query_time - start_time}")


def query_rag(query_text: str):
    # Prepare the DB.
    query_time = time.time()
    embedding_function = get_embedding_function()
    db = Chroma(persist_directory=CHROMA_PATH, embedding_function=embedding_function)
    

    # Search the DB.
    results = db.similarity_search_with_score(query_text, k=5)
    
    for doc, _score in results:
        print(doc.page_content)
        
    embed_time = time.time() - query_time
    context_text = "\n\n---\n\n".join([doc.page_content for doc, _score in results])
    prompt_template = ChatPromptTemplate.from_template(PROMPT_TEMPLATE)
    prompt = prompt_template.format(context=context_text, question=query_text)
    # print(prompt)

    model = Ollama(model="gemma2:2b", base_url="http://192.168.1.64:11434")
    #model = Ollama(model="gemma2:2b")
    load_model_time = time.time() - query_time
    response_text = model.invoke(prompt)
    answer_time = time.time() - query_time

    sources = [doc.metadata.get("id", None) for doc, _score in results]
    formatted_response = f"Response: {response_text}\nSources: {sources}"
    print(formatted_response)
    print(f"Embed Time: {embed_time}\n load_model_time: {load_model_time}\n Answer Time: {answer_time} ")
    return response_text


#if __name__ == "__main__":
#    main()
