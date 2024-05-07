import os
import sys

SCRIPT_DIR = os.path.abspath(__file__)
sys.path.append(os.path.dirname(SCRIPT_DIR))

from lambda_function import lambda_handler

payload="""
Hello, my name is David Johnson and I live in Maine.
I work as a software engineer at Amazon.
You can call me at (123) 456-7890.
My credit card number is 4095-2609-9393-4932 and my crypto wallet id is 16Yeky6GMjeNkAiNcBY7ZhrLoMSgg1BoyZ.
 
On September 18 I visited microsoft.com and sent an email to test@presidio.site, from the IP 192.168.0.1.
My passport: 191280342 and my phone number: (212) 555-1234.
This is a valid International Bank Account Number: IL150120690000003111111. Can you please check the status on bank account 954567876544?
Kate's social security number is 078-05-1126.  Her driver license? it is 1234567A.
"""

payload_2="""Hello, my name is Senthil Kumar and I live in Chennai.
I work as a software engineer at XYZ. my email id is senthil_kumar@gmail.com. I need to avail refund for a purchase in your site made from the credit card number 5549-8979-6588-8762. Reach me at mobile +91 9876541230"""

# event = {
#     "text_to_be_masked": "My name is Bond, James Bond. My Phone number is (543) 968-1898"
# }

event = {
    "text_to_be_masked": payload_2
}


context = {}

return_event = lambda_handler(event, context)
print(return_event)