import base64
import json
from llama_cpp import Llama

import os
os.environ['HF_HOME'] = '/tmp/model'
os.environ['TRANSFORMERS_CACHE']='/tmp/model'

# llm = Llama(
#     # model_path="./model/phi-2.Q4_K_M.gguf",
#     model_path="./model/Phi-3-mini-4k-instruct-q4.gguf",
#     n_ctx=2048,
#     n_threads=6,  # maximum in AWS Lambda
# )

from langchain_community.embeddings import HuggingFaceEmbeddings; \
embed_model_name = 'sentence-transformers/all-MiniLM-L6-v2'; 
device='cpu'; 
encode_kwargs= {'normalize_embeddings': False}; 
embed_model = HuggingFaceEmbeddings(model_name=embed_model_name, model_kwargs={'device': device}, encode_kwargs=encode_kwargs, cache_folder='/tmp/model'
)

from langchain_community.document_loaders import WebBaseLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import GPT4AllEmbeddings

from langchain_community.embeddings import LlamaCppEmbeddings
from langchain_community.llms import LlamaCpp
from langchain.callbacks.manager import CallbackManager
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler

from langchain.chains import RetrievalQA
from langchain.prompts import PromptTemplate


def handler(event, context):
    print("Event is:", event)
    print("Context is:", context)

    try:
        if event.get('isBase64Encoded', False):
            body = base64.b64decode(event['body']).decode('utf-8')
        else:
            body = event['body']
            try:
                body_json = json.loads(body)
            except: 
                body_json = body
        prompt = body_json["prompt"]
        context_data_url = body_json["url"]
    except (KeyError, json.JSONDecodeError) as e:
        return {"statusCode": 400, "body": f"Error processing request: {str(e)}"}

    loader = WebBaseLoader(context_data_url)
    
    data = loader.load()

    text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=0)
    all_splits = text_splitter.split_documents(data)

    vectorstore = Chroma.from_documents(documents=all_splits, embedding=embed_model)
    n_batch = 1  # Should be between 1 and n_ctx, consider the amount of RAM of your Apple Silicon Chip.
    callback_manager = CallbackManager([StreamingStdOutCallbackHandler()])

    # running the way phi3 model is run
    # https://huggingface.co/microsoft/Phi-3-mini-4k-instruct-gguf/blob/main/README.md
    # output = llm(
    #     f"<|user|>\n{prompt}<|end|>\n<|assistant|>",
    #     max_tokens=256,  # Generate up to 256 tokens
    #     stop=["<|end|>"], 
    #     echo=False, # do not want to repeat the input
    # )

    llm = LlamaCpp(
        model_path="./model/Phi-3-mini-4k-instruct-q4.gguf",
        n_batch=n_batch,
        n_ctx=2048,
        # f16_kv=True, 
        callback_manager=callback_manager,
        verbose=False,
    )

    docs = vectorstore.similarity_search(prompt)
    inital_prompt = '''You are an assistant for question-answering tasks. 
    Use the context to answer the question. 
    If you don't know the answer, just say that you don't know. 
    Keep the answer concise.

    Question: '''
    # QA_CHAIN_PROMPT = PromptTemplate(input_variables=["context", "question"],template=full_prompt,)

    rag_pipeline = RetrievalQA.from_chain_type(
        llm=llm, chain_type='stuff',
        # chain_type_kwargs={"prompt":QA_CHAIN_PROMPT},
        retriever=vectorstore.as_retriever()
    )
    question = prompt

    # output = rag_pipeline({"query": question })

    final_prompt = f"<|user|>\n{inital_prompt + prompt}<|end|>\n<|assistant|>"

    output = rag_pipeline(final_prompt)

    # answer = {"main_output": output['result'], 
    #         "full_output": output
    # }

    print(f"The answer to the query: {prompt}")
    print(output['result'])

    return {
        "statusCode": 200,
        "body": json.dumps(output)
    }