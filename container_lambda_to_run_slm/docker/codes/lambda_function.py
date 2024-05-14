import base64
import json
from llama_cpp import Llama


llm = Llama(
    # model_path="./model/phi-2.Q4_K_M.gguf",
    model_path="./model/Phi-3-mini-4k-instruct-q4.gguf",
    n_ctx=2048,
    n_threads=6,  # maximum in AWS Lambda
)


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
    except (KeyError, json.JSONDecodeError) as e:
        return {"statusCode": 400, "body": f"Error processing request: {str(e)}"}

    # running the way phi3 model is run
    # https://huggingface.co/microsoft/Phi-3-mini-4k-instruct-gguf/blob/main/README.md
    output = llm(
        f"<|user|>\n{prompt}<|end|>\n<|assistant|>",
        max_tokens=256,  # Generate up to 256 tokens
        stop=["<|end|>"], 
        echo=False, # do not want to repeat the input
    )

    answer = {"main_output": output['choices'][0]['text'], 
            "full_output": output
    }

    return {
        "statusCode": 200,
        "body": json.dumps(answer)
    }