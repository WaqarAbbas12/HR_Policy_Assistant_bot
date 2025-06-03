import weaviate
from weaviate.classes.init import AdditionalConfig, Timeout
import weaviate.classes.config as wc
from dotenv import load_dotenv
import os

load_dotenv()
api_endpoint = os.getenv("DOCKER_API_ENDPOINT")
vectorizer = os.getenv("VECTORIZER")
LLM = os.getenv("LLM")

def connectDB():
    try:
        client = weaviate.connect_to_local(
            additional_config=AdditionalConfig(
                timeout=Timeout(init=10, query=60, insert=120)
            )
        )
        print(f"Connection Status:{client.is_ready()}")
    except Exception as e:
        print(e)
    return client


def create_collection(
    client, api_endpoint=api_endpoint, vectorizer=vectorizer, LLM=LLM
):
    try:
        client.collections.create(
            name="Document",
            generative_config=wc.Configure.Generative.ollama(
                api_endpoint=api_endpoint, model=LLM
            ),
            vectorizer_config=wc.Configure.Vectorizer.text2vec_ollama(
                api_endpoint=api_endpoint, model=vectorizer
            ),
            properties=[wc.Property(name="body", data_type=wc.DataType.TEXT)],
        )
        print("Collection Created")
    except Exception as e:
        print(e)
