from openai import OpenAI
from dotenv import load_dotenv
import os
from pydantic import BaseModel, Field

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
MODEL = "gpt-4o-2024-08-06"

class Action(BaseModel):
    description: str = Field(description="Description of the action taken.")
    action_taken: str = Field(description="Actual action taken to resolve the issue.")

class TicketResolution(BaseModel):
    steps: list[Action]
    final_resolution: str = Field(description="The final resolution of the issue that will be sent to the customer.")

user = """
Hi, i am having a problem with my recent order. I received the wrong item. I ordered a blue t-shirt, but I received a red one instead. Can you help me with this?
I would like to return the red t-shirt and get the blue one I ordered. Thank you! Can I expect a replacement soon?
"""

system = """ 
You are an AI assistant that helps users with their customer service inquiries. Your goal is to respond with a structured solution to the user's problem, 
including the steps taken to resolve the issue, the expected timeline for resolution, a description and the action taken.
"""

def get_ticket_response(user, system):
    completion = client.beta.chat.completions.parse(
        model="gpt-4o-2024-08-06",
        messages=[
            {"role": "system", "content": system},
            {"role": "user", "content": user}
        ],
        response_format=TicketResolution,
    )
    return completion
    
ticket_resolution =  get_ticket_response(user, system).choices[0].message
# If the model refuses to respond, you will get a refusal message
if (ticket_resolution.refusal):
    print(ticket_resolution.refusal)
else:
    print(ticket_resolution.parsed)
    
