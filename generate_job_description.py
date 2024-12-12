import os
from typing import Annotated
from typing_extensions import TypedDict
from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages
from langchain_openai import OpenAI
from langchain_community.tools.tavily_search import TavilySearchResults
from dotenv import load_dotenv


#load env
load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
TAVILY_API_KEY = os.getenv("TAVILY_API_KEY")

"""
This module generates detailed job descriptions using a combination of web search results
and AI-powered text generation. It uses a graph-based workflow to gather information
and create structured job postings.
"""

#define state for the graph
class State(TypedDict):
    """
    Represents the state object that flows through the graph.
    
    Attributes:
        firm_name (str): Name of the company hiring
        role (str): Job title/role being hired for
        search_results (list): Results from Tavily search about company and role
        job_description (str): Final generated job description
    """
    firm_name: str
    role: str
    search_results: list
    job_description: str

graph_builder = StateGraph(State)

### Now we define the nodes for the graph
def input_node(state: State):
    """
    Input node for the graph.
    This node is used to get the firm name and role from the user.
    """
    firm = state.get("firm_name")
    role = state.get("role")
    if not firm or not role:
        raise ValueError("Firm name and role must be provided.")
    return state  # Passes the input forward without changes

graph_builder.add_node("input", input_node)

## Add a tool node - Tavily search tool
tavily_search = TavilySearchResults(max_results=2, api_key=os.getenv("TAVILY_API_KEY"))

def search_node(state: State):
    """
    Performs web searches to gather context about the company and role.
    
    Args:
        state (State): Current graph state containing firm_name and role
        
    Returns:
        dict: Contains search_results list with [firm_info, role_info]
    """
    firm = state["firm_name"]
    role = state["role"]
    
    # Search for firm information using Tavily
    firm_info = tavily_search.invoke(f"About {firm}")
    
    # Search for general role requirements and responsibilities
    role_info = tavily_search.invoke(f"Responsibilities of a {role}")
    
    return {
        "search_results": [firm_info, role_info]
    }

graph_builder.add_node("search", search_node)

## Add LLM Node to generate a job description
from langchain_openai import ChatOpenAI

llm = ChatOpenAI(model="gpt-4o-mini")

def job_description_node(state: State):
    """
    Generates a structured job description using gathered information.
    
    Args:
        state (State): Contains firm_name, role, and search_results
        
    Returns:
        dict: Contains the generated job_description
    """
    firm = state["firm_name"]
    role = state["role"]
    search_results = state["search_results"]
    
    firm_info = search_results[0]
    role_info = search_results[1]
    
    prompt = f"""
    Create a comprehensive job description for the role of {role} at {firm}. 
    Here is some information about the firm:
    {firm_info}
    
    And here are the responsibilities of the role:
    {role_info}
    
    Based on this information, generate a detailed job description that includes:
    - Job Title
    - Company Overview
    - Responsibilities
    - Qualifications
    - Benefits
    """

    job_desc = llm.invoke(prompt)
    
    return {
        "job_description": job_desc
    }

graph_builder.add_node("generate_job_description", job_description_node)

#Add edges for graph -- this is how the graph flows
graph_builder.add_edge(START, "input") # Connect START to Input
graph_builder.add_edge("input", "search") # Connect Input to Search
graph_builder.add_edge("search", "generate_job_description") # Connect Search to Job Description
graph_builder.add_edge("generate_job_description", END) # Connect Job Description to END

# Compile the graph 
graph = graph_builder.compile()

# Function to run graph and store output of job description as .md file
def run_graph(firm_name: str, role: str) -> None:
    """
    Executes the job description generation workflow and saves the result.
    
    Args:
        firm_name (str): Name of the hiring company
        role (str): Job title/role being hired for
        
    Outputs:
        Creates a markdown file named '{firm_name}_{role}.md' with the job description
    """
    result = graph.invoke({"firm_name": firm_name, "role": role})
    with open(f"{firm_name}_{role}.md", "w") as file:
        file.write(result["job_description"].content)

# Entry point for direct script execution
if __name__ == "__main__":
    # Example usage - generates a Software Engineer job description for Arche AI
    run_graph("Arche AI - Coding Workflow Automation", "Software Engineer")

