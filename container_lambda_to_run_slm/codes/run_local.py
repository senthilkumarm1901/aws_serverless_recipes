import os
import sys

SCRIPT_DIR = os.path.abspath(__file__)
sys.path.append(os.path.dirname(SCRIPT_DIR))

from lambda_function import handler

payload="""What is the capital of India?
"""

# event = {
#     "text_to_be_masked": "My name is Bond, James Bond. My Phone number is (543) 968-1898"
# }

event = {
    "body": {"prompt": payload}
}


context = {}

return_event = handler(event, context)
print(return_event)