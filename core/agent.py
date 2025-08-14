# core/agent.py

import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain.agents import AgentExecutor, create_react_agent
from langchain_core.prompts import ChatPromptTemplate
from langchain import hub

# Import your custom file-handling tools
from .tools import WriteFileTool, ReadFileTool, ListDirectoryTool, DeleteFileTool, CreateDirectoryTool

# --- AGENT INITIALIZATION ---
class ReactAgent:
    """
    The "Brain" of the application. It uses a language model via OpenRouter
    to process user requests and decide which tools to use.
    """
    def __init__(self):
        # --- THIS IS THE FIX ---
        # Load the .env file to get the OpenRouter API key
        load_dotenv()
        openrouter_api_key = os.getenv("OPENROUTER_API_KEY")

        if not openrouter_api_key:
            raise ValueError("OPENROUTER_API_KEY not found in .env file. Please check your configuration.")

        # Initialize the Chat Client to use OpenRouter
        # We point it to the OpenRouter URL and provide your key.
        # We'll use a fast and capable model like Claude 3 Haiku.
        self.llm = ChatOpenAI(
            model="deepseek/deepseek-r1-0528:free",
            api_key=openrouter_api_key,
            base_url="https://openrouter.ai/api/v1",
            temperature=0,
            streaming=True,
        )
        # --- END OF FIX ---

        # Define the tools the agent can use
        self.tools = [WriteFileTool(), ReadFileTool()]
        
        # Get the ReAct agent prompt from LangChain Hub
        prompt = hub.pull("hwchase17/react")
        
        # Create the agent by binding the tools to the LLM
        agent = create_react_agent(self.llm, self.tools, prompt)
        
        # Create the agent executor, which runs the agent's thought process
        self.agent_executor = AgentExecutor(
            agent=agent, 
            tools=self.tools, 
            verbose=True, # Set to True to see the agent's thoughts
            handle_parsing_errors=True, # Helps prevent crashes on weird outputs
            max_iterations=10 # Prevents infinite loops
        )

    def get_agent_response(self, user_message, thread_id: str):
        """
        Invokes the agent to get a response for the user's message.
        (Note: thread_id is included for future stateful conversation)
        """
        response = self.agent_executor.invoke({
            "input": user_message.content,
        })
        return response

