import phoenix as px
import pandas as pd
import numpy as np

openai_api_key = "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"

# Launch phoenix
session = px.launch_app()

# Once you have started a Phoenix server, you can start your LangChain application with the OpenInferenceTracer as a callback. To do this, you will have to instrument your LangChain application with the tracer:

from phoenix.trace.langchain import OpenInferenceTracer, LangChainInstrumentor

# If no exporter is specified, the tracer will export to the locally running Phoenix server
tracer = OpenInferenceTracer()
LangChainInstrumentor(tracer).instrument()

# Initialize your LangChain application
from langchain.chains import RetrievalQA
from langchain.chat_models import ChatOpenAI
from langchain.embeddings import OpenAIEmbeddings
from langchain.retrievers import KNNRetriever

embeddings = OpenAIEmbeddings(model="text-embedding-ada-002")
documents_df = pd.read_parquet(
    "http://storage.googleapis.com/arize-assets/phoenix/datasets/unstructured/llm/context-retrieval/langchain-pinecone/database.parquet"
)
knn_retriever = KNNRetriever(
    index=np.stack(documents_df["text_vector"]),
    texts=documents_df["text"].tolist(),
    embeddings=OpenAIEmbeddings(),
)
chain_type = "stuff"  # stuff, refine, map_reduce, and map_rerank
chat_model_name = "gpt-3.5-turbo"
llm = ChatOpenAI(model_name=chat_model_name)
chain = RetrievalQA.from_chain_type(
    llm=llm,
    chain_type=chain_type,
    retriever=knn_retriever,
)

# Instrument the execution of the runs with the tracer. By default the tracer uses an HTTPExporter
query = "What is euclidean distance?"
response = chain.run(query, callbacks=[tracer])

# By adding the tracer to the callbacks of LangChain, we've created a one-way data connection between your LLM application and Phoenix.

# To view the traces in Phoenix, simply open the UI in your browser.
session.url