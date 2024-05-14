import os
import sys

SCRIPT_DIR = os.path.abspath(__file__)
sys.path.append(os.path.dirname(SCRIPT_DIR))

from lambda_function import handler

# payload="""Can you explain what is Layer Normalization in Transformer models?"""
payload="What can you tell me about ULMFit? Explain in 5 bullet points"
url= "https://magazine.sebastianraschka.com/p/understanding-large-language-models"

# event = {
#     "text_to_be_masked": "My name is Bond, James Bond. My Phone number is (543) 968-1898"
# }

event = {
    "body": {"prompt": payload, "url": url}
}


context = {}

return_event = handler(event, context)
print(return_event)