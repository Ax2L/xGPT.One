In this tutorial, we will create a personalized Q&A app that can extract information from PDF documents using your selected open-source Large Language Models (LLMs). We will cover the benefits of using open-source LLMs, look at some of the best ones available, and demonstrate how to develop open-source LLM-powered applications using Shakudo.

If you want to skip directly to code, we’ve made it available on [GitHub](https://github.com/devsentient/examples/tree/main/LLMs/QA_app)!

## Why are open-source LLMs becoming popular in the AI space?

Let's start by understanding why developers increasingly prefer open-source LLMs over commercial offerings, like OpenAI's APIs.

### Customization and optimization

Open-source LLMs are highly adaptable. They allow users to modify and optimize the models to cater to their needs. This flexibility enables the LLMs to understand and process unique data effectively. Ecosystems of hugging face, LangChain and Pytorch make open-source models easy to infer and finetune for specific use cases.

### Autonomy and cost efficiency

Adopting open-source LLMs significantly reduces dependency on large AI providers, giving you the freedom to select your preferred technology stack. This autonomy minimizes issues related to vendor lock-in and fosters an environment of collaboration within the developer community.

Cost efficiency is another vital benefit of employing open-source LLMs. For small-scale use (thousands of requests/day), the OpenAI's ChatGPT API is relatively cost-effective at around $1.30/day. For large-scale use (millions of requests/day), it can quickly rise to $1,300/day. In contrast, open-source LLMs on an NVIDIA A100 cost approximately $4/hour or $96/day. 

### Enhanced data security

Open-source LLMs provide better data privacy and security. Unlike third-party AI services, these models allow you to maintain complete control over your data, which minimizes the risk of data breaches. OpenAI offers an enterprise license that allows businesses to use and fine-tune their LLMs. This can help businesses address data privacy concerns by allowing them to train the models on their data. However, the enterprise license is expensive and requires a significant amount of technical expertise to use. 

Fine-tuning can be time-consuming and expensive. It can also be difficult to ensure that the model is not biased or harmful. Open-source LLMs still offer the best data privacy and security, allowing businesses to completely control their data and training process.

### Lower Latency

For applications where real-time user interaction is crucial, the high latency of GPT-4 can be a significant drawback. When optimized and deployed efficiently, open-source models can offer much lower latencies, which makes them more suitable for user interfacing applications.

### Innovation and Contribution to AI Development

Open-source LLMs enable companies and developers to contribute to the future of AI. The freedom to control the model's architecture, training data, and training process promotes experimentation with novel techniques and strategies. It allows you to stay updated with the latest developments in AI research and contribute to the AI community by sharing your models and techniques.

### Top open-source LLMs (June 2023)

When it comes to open-source LLMs, there's a variety to choose from, including top ones like Falcon-40B-Instruct and Guanaco-65b.  [OpenLLM Leaderboard](https://huggingface.co/spaces/HuggingFaceH4/open_llm_leaderboard) compares text-generative LLMs on different benchmarks. 

#### Text Generation Models:



#### Text Embedding models:

[MTEB leaderboard](https://huggingface.co/spaces/mteb/leaderboard) similarly compares text-embedding models on different tasks.



## Building a PDF Knowledge Bot with Open-source LLMs on Shakudo

### Solution Overview:

For any textual knowledge base (in our case, PDFs), we first need to extract text snippets from the knowledge base and use an embedding model to create a vector store representing the semantic content of the snippets. When a question is asked, we estimate its embedding and find relevant snippets using an efficient similarity search from vector stores. After extracting the snippets, we engineer a prompt and generate an answer using the LLM generation model. The prompt can be tuned based on the specific LLM used.

Experimentation and development are crucial elements in the field of data science. Shakudo's session facilitates the selection of the appropriate computing resources. It provides the flexibility to choose from Jupyter Notebooks, VS Code Server (provided by the platform) or connecting via SSH to use a preferred local editor.

[](https://www.shakudo.io/blog/build-pdf-bot-open-source-llms#)

[](https://www.shakudo.io/blog/build-pdf-bot-open-source-llms#)[![](https://uploads-ssl.webflow.com/625447c67b621ab49bb7e3e5/6490ae677630935d12886555_build-kb-chatapp-shakudo-datastack.jpg)](https://uploads-ssl.webflow.com/625447c67b621ab49bb7e3e5/6490ae677630935d12886555_build-kb-chatapp-shakudo-datastack.jpg)

Overview of pdf chatbot llm solution

### Step 0: Loading LLM Embedding Models and Generative Models

We begin by setting up the models and embeddings that the knowledge bot will use, which are critical in interpreting and processing the text data within the PDFs.

#### LLM Embedding Models

We use the following Open Source models in the codebase:

-   [INSTRUCTOR XL](https://huggingface.co/hkunlp/instructor-xl) : Instructor xl is an instruction-finetuned text embedding model that can generate embeddings tailored for any task instruction. The instruction for embedding text snippets is "Represent the document for retrieval:". The instruction for embedding user questions is "Represent the question for retrieving supporting documents:"
-   [SBERT](https://huggingface.co/sentence-transformers/all-mpnet-base-v2) : SBERT maps sentences and paragraphs to vectors using a BERT-like model. It's a good start when we’re prototyping our application.

Hugging faces [MTEB leaderboard](https://huggingface.co/spaces/mteb/leaderboard) compares embedding models on different tasks. Instructor XL ranks very highly on this list, even better than [OpenAI's ADA](https://platform.openai.com/docs/guides/embeddings).

#### LLM Generation Models

 Open source models used in the codebase are

-   [FlanT5 Models](https://huggingface.co/docs/transformers/model_doc/flan-t5) : FlanT5 is text2text generator that is finetuned on several tasks like summarisation and answering questions. It uses the encode-decoder architecture of transformers. The model is Apache 2.0 licensed, which can be used commercially.
-   [FastChatT5 3b Model](https://huggingface.co/sentence-transformers/all-mpnet-base-v2) : It's a FlanT5-based chat model trained by fine tuning FlanT5 on user chats from ChatGPT. The model is Apache 2.0 licensed.
-   [Falcon7b Model](https://huggingface.co/tiiuae/falcon-7b) : Falcon7b is a smaller version of Falcon-40b, which is a text generator model (decoder-only model). Falcon-40B is currently the best open-source model on the [OpenLLM Leaderboard](https://huggingface.co/spaces/HuggingFaceH4/open_llm_leaderboard). One major reason for its high performance is its training with high-quality data. 

[![](https://uploads-ssl.webflow.com/625447c67b621ab49bb7e3e5/6490aeca1e9c538657d1692c_build-kb-chatapp-shakudo-llmsUsed.jpg)](https://uploads-ssl.webflow.com/625447c67b621ab49bb7e3e5/6490aeca1e9c538657d1692c_build-kb-chatapp-shakudo-llmsUsed.jpg)

Open source models used in the codebase

There are other high-performing open-source models (MPT-7B, StableLM, RedPajama, Guanaco) in the [OpenLLM Leaderboard](https://huggingface.co/spaces/HuggingFaceH4/open_llm_leaderboard), which can be easily integrated with hugging face pipelines.

Let’s go ahead and first set up **SBERT** for the embedding model and **FLANT5-Base** for the generation model. We chose these models because they can run on an 8 core CPU. FastChat-T5 and Flacon-Instruct-7B require GPU. Loading them is similar and is shown in [Codebase](https://github.com/devsentient/examples/blob/main/LLMs/QA_app/pdf_qa.py):

To employ these models, we use [Hugging Face pipelines](https://huggingface.co/docs/transformers/main_classes/pipelines), which simplify the process of loading the models and using them for inference. 

-   For encoder-decoder models like FlanT5, the pipeline’s task is ”text2text-generation”. 
-   The auto device map feature assists in efficiently loading the language model (LLM) by utilizing GPU memory. If the entire model cannot fit in the GPU memory, some layers are loaded onto the CPU memory instead. If the model still cannot fit completely, the remaining weights are stored in disk space until needed.
-   Loading in 8-bit [quantizes](https://huggingface.co/blog/hf-bitsandbytes-integration) the LLM and can lower the memory requirements by half.

The creation of the models is governed by the configuration settings and is handled by the **create\_sbert\_mpnet()** and **create\_flan\_t5\_base()** functions, respectively.

If we want to load Falcon, the pipeline would be as below and its task is ”text-generation” as Falcon is a decoder-only model. We need to allow remote code execution because the code comes from the Falcon author’s repository and not from hugging face.

This setup forms the foundation of the knowledge bot's capability to understand and generate responses to textual input.

### Step 1: Ingesting the Data into Vector Store (ChromaDB)

In this step, let’s load our PDF and split it into manageable text snippets.

### Step 2: Retrieving Snippets and Prompt Engineering

Now, we retrieve relevant snippets based on question embeddings and then construct a prompt to query the LLM.

### Step 3: Querying the LLM

Finally, we query the LLM using our question. The PDF knowledge bot will return the relevant information extracted from the PDF.

#### Packaging into a Class

To make the code more organized, we can encapsulate all functionalities into a class.

We can now initialize and run the **PdfQA** class with the following code:

### Step 4: Building the Streamlit app 

Shakudo integrates with various tools you can choose to build your front end. For this app, let’s wrap our web application around our PdfQA class with Streamlit, a Python library that simplifies app creation.

Below is the code breakdown:

We start by importing the necessary modules

Now, let’s set the page configuration and have a session state of the class to avoid instantiating the class multiple times in the same session.

To load the model and embedding on the GPU or CPU only once across all the client sessions, we cache the LLM and embedding pipelines.

Create our Steamlit app sidebar to include radio buttons for model selection and a file uploader. Once the file is submitted, It triggers the model loading and PDF ingestion to create a vector store.

Add a text input box for the question. Once we submit the question, it triggers the retrieval of relevant text snippets from the vector store and queries the LLM with an appropriate prompt.

This user interface allows the user to upload a PDF file, choose the model to use and ask a question.

### Step 5: Deploying with Shakudo

Finally, our app is ready, and we can deploy it as a service on Shakudo. The platform makes the deployment process easier, allowing you to put your application online quickly. 

[![](https://uploads-ssl.webflow.com/625447c67b621ab49bb7e3e5/6490b0c3fe55343c108e2280_build-kb-chatapp-shakudo-buildOnShakudo.jpg)](https://uploads-ssl.webflow.com/625447c67b621ab49bb7e3e5/6490b0c3fe55343c108e2280_build-kb-chatapp-shakudo-buildOnShakudo.jpg)

High-level diagram of deploying llm app on Shakudo

Finally, our app is ready, and we can deploy it as a service on Shakudo. The platform makes the deployment process easier, allowing you to put your application online quickly. 

Deploying applications on Shakudo offers enhanced security and control. Unlike many other deployments, Shakudo locks your application behind the SSO or your organization. The services and the self-hosted models run entirely within your cloud tenancy and on your dedicated Shakudo cluster, providing you with the flexibility to avoid vendor lock-in and enabling you to retain control over your applications running in the cloud

To deploy your app on Shakudo, we need two key files: pipeline.yaml, which describes our deployment pipeline, and run.sh, a bash script to set up and run our application. Here's what these files look like.

-   ‘pipeline.yaml’:

-   ‘run.sh’:

In this script:

-   Set the project directory and navigate into it.
-   Install the necessary Python libraries from the requirements.txt file.
-   Run the Streamlit app on port 8787.

Now, our application is live! We can browse through the user interface to see how it works.

[![](https://uploads-ssl.webflow.com/625447c67b621ab49bb7e3e5/6490b1853b8aff0c3c2c885c_build-kb-chatapp-shakudo-streamlit-ui.png)](https://uploads-ssl.webflow.com/625447c67b621ab49bb7e3e5/6490b1853b8aff0c3c2c885c_build-kb-chatapp-shakudo-streamlit-ui.png)

LLM app Streamlit UI

Shakudo Services not only simplifies the deployment of your applications but also has a robust approach to security. Deploying your models within your Virtual Private Cloud (VPC) is one of the most secure ways of hosting models, as it isolates them from the public internet and provides better control over your data.

## Conclusion

In this tutorial, we described the advantages of using open-source LLMs over Commercial APIs. We showed how to integrate OSS LLMs Falcon, FastChat, and FlanT5 to query the internal Knowledge Base with the help of Hugging Face pipelines and LangChain.

Hosting and managing open-source LLMs can be a complex and challenging task. Shakudo simplifies LLM infrastructure, saving time, resources, and expertise. For a first-hand experience of our platform, we encourage you to reach out to our team and [book a demo](https://www.shakudo.io/sign-up).

To understand about the practical applications with OpenAI APIs, we recommend reading our previous post about "[Building a Confluence Q&A App with LangChain and ChatGPT](https://www.shakudo.io/blog/building-confluence-kb-qanda-app-langchain-chatgpt)" where we showcase a real-world use case, a chatbot to query your confluence directories. For further reading on LangChain, check out [CommandBar's in-depth guide](https://www.commandbar.com/blog/langchain-guide).

#### Resources:

\* The code is adapted based on the work in [LLM-WikipediaQA](https://github.com/georgesung/LLM-WikipediaQA/tree/main), where the author compares FastChat-T5, Flan-T5 with ChatGPT running a Q&A on Wikipedia Articles.