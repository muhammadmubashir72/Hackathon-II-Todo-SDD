from fastapi import FastAPI
from pydantic import BaseModel
from agents import Agent, Runner, OpenAIChatCompletionsModel, AsyncOpenAI
import os
from dotenv import load_dotenv, find_dotenv
import gradio as gr
import asyncio
from fastapi.middleware.cors import CORSMiddleware

# Load environment variables
load_dotenv(find_dotenv())

external_client = AsyncOpenAI(
    api_key=os.getenv("GEMINI_API_KEY"),
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/",
)

llm_model = OpenAIChatCompletionsModel(
    model="gemini-2.5-flash",
    openai_client=external_client
)

agent = Agent(
    name="Legal Assistant",
    model=llm_model,
    instructions="""
    You are a Pakistan legal assistant.
    Explain laws simply.
    No legal advice.
    """
)

class ChatRequest(BaseModel):
    message: str

# Create FastAPI app
app = FastAPI()

# Add CORS middleware to allow requests from Flutter app
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins for compatibility
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    return {"message": "Pakistan Legal Assistant API is running!"}

@app.post("/chat")
async def chat_endpoint(req: ChatRequest):
    result = await Runner.run(
        starting_agent=agent,
        input=req.message
    )
    return {
        "reply": result.final_output
    }

# Define the chat function for Gradio
def predict(message, history):
    # Convert the synchronous function to asynchronous and run it
    async def run_agent():
        result = await Runner.run(
            starting_agent=agent,
            input=message
        )
        return result.final_output
    
    # Run the async function
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    response = loop.run_until_complete(run_agent())
    loop.close()
    
    return response

# Create Gradio interface
with gr.Blocks(title="Pakistan Legal Assistant") as demo:
    gr.Markdown("# Pakistan Legal Assistant")
    gr.Markdown("Ask about Pakistani laws. This is for educational purposes only, not legal advice.")
    
    chatbot = gr.Chatbot()
    msg = gr.Textbox(label="Your Question")
    clear = gr.ClearButton([msg, chatbot])
    
    def respond(message, chat_history):
        bot_message = predict(message, chat_history)
        chat_history.append((message, bot_message))
        return "", chat_history

    msg.submit(respond, [msg, chatbot], [msg, chatbot])

# Mount the Gradio app to the FastAPI app
app = gr.mount_gradio_app(app, demo, path="/gradio")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=7860)