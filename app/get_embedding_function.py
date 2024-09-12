from langchain_community.embeddings import OllamaEmbeddings
from langchain_community.embeddings.bedrock import BedrockEmbeddings


def get_embedding_function():
    #embeddings = BedrockEmbeddings(
    #    credentials_profile_name="default", region_name="us-east-1"
    #)
    embeddings = OllamaEmbeddings(model="nomic-embed-text", base_url="http://192.168.1.64:11434")
    return embeddings
