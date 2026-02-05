from fastapi import Depends, FastAPI
from openai import AsyncOpenAI
from dotenv import load_dotenv
import os
from pydantic import BaseModel, Field

load_dotenv()

app = FastAPI(title="Structured Output Example")

client = AsyncOpenAI(
    api_key=os.getenv("OPENAI_API_KEY"),
    base_url=os.getenv("API_URL")
)

class Action(BaseModel):
    description: str = Field(description="Description of the action taken.")
    action_taken: str = Field(description="Actual action taken to resolve the issue.")

class TicketResolution(BaseModel):
    steps: list[Action]
    final_resolution: str = Field(description="The final resolution of the issue that will be sent to the customer.")

class QueryRequest(BaseModel):
    request: str

class QueryResponse(BaseModel):
    answer: str

def question_to_question_request(
        request: str = "vraag",
        ) -> QueryRequest:
    return QueryRequest(request=request)

async def get_ticket_response(user, system):
    completion = await client.chat.completions.parse(
        model=os.getenv("LLM_MODEL"),
        messages=[
            {"role": "system", "content": system},
            {"role": "user", "content": user}
        ],
        response_format=TicketResolution,
    )
    return completion

@app.post("/")
async def verwerk_formulier(
    request: QueryRequest = Depends(question_to_question_request), 
) -> TicketResolution:
        
    # user = """
    # Hi, i am having a problem with my recent order. I received the wrong item. I ordered a blue t-shirt, but I received a red one instead. Can you help me with this?
    # I would like to return the red t-shirt and get the blue one I ordered. Thank you! Can I expect a replacement soon?
    # """

    system = """ 
    You are an AI assistant that helps users with their customer service inquiries. Your goal is to respond with a structured solution to the user's problem, 
    including the steps taken to resolve the issue, the expected timeline for resolution, a description and the action taken. IMPORTANT: Allways respond to the client using the TicketResolution final_resolution.
    """
    ticket_resolution = await get_ticket_response(request.request, system)
    # If the model refuses to respond, you will get a refusal message
    message = ticket_resolution.choices[0].message
    
    # Nu kun je bij .refusal en .parsed
    if (message.refusal):
        print(f"Model weigerde: {message.refusal}")
    else:
        print(f"Geparsed resultaat: {message.parsed}")
    return TicketResolution(steps=message.parsed.steps, final_resolution=message.parsed.final_resolution)
    



    






