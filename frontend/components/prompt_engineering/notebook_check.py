import phoenix as px

# To view traces in Phoenix, you will first have to start a Phoenix server. You can do this by running the following:
session = px.launch_app()


# Once you have started a Phoenix server, you can start your LlamaIndex application with the `OpenInferenceTraceCallback` as a callback. To do this, you will have to add the callback to the initialization of your LlamaIndex application:

from phoenix.trace.llama_index import (
    OpenInferenceTraceCallbackHandler,
)

# Initialize the callback handler
callback_handler = OpenInferenceTraceCallbackHandler()

# LlamaIndex application initialization may vary
# depending on your application
service_context = ServiceContext.from_defaults(
    llm_predictor=LLMPredictor(llm=ChatOpenAI(model_name="gpt-3.5-turbo", temperature=0)),
    embed_model=OpenAIEmbedding(model="text-embedding-ada-002"),
    callback_manager=CallbackManager(handlers=[callback_handler]),
)
index = load_index_from_storage(
    storage_context,
    service_context=service_context,
)
query_engine = index.as_query_engine()

# Query your LlamaIndex application
query_engine.query("What is the meaning of life?")
query_engine.query("Why did the cow jump over the moon?")

# View the traces in the Phoenix UI
px.active_session().url