# LangChain Job Description Generator

## Overview

The **LangChain Job Description Generator** is a Python-based tool that leverages AI and web search capabilities to create detailed and structured job descriptions. Utilizing the power of [LangGraph](https://github.com/langgraph/langgraph) and [LangChain](https://github.com/langchain-ai/langchain), this tool automates the process of gathering company information and role-specific responsibilities to generate comprehensive job postings.

## Features

- **Automated Information Gathering:** Uses Tavily search to collect relevant information about the company and the job role.
- **AI-Powered Generation:** Employs OpenAI's GPT model to craft detailed job descriptions.
- **Graph-Based Workflow:** Implements a state graph to manage the workflow, ensuring a structured and efficient process.
- **Easy to Use:** Simple command-line interface for generating job descriptions with minimal setup.

## Getting Started

### Prerequisites

- Python 3.13 or higher
- An OpenAI API key
- A Tavily API key

### Installation

1. **Clone the Repository**   ```bash
   git clone https://github.com/your-username/langchain-job-description-generator.git
   cd langchain-job-description-generator   ```

2. **Create a Virtual Environment**   ```bash
   python -m venv .venv
   source .venv/bin/activate  # On Windows use `.venv\Scripts\activate`   ```

3. **Install Dependencies**   ```bash
   pip install -r requirements.txt   ```

4. **Set Up Environment Variables**

   Create a `.env` file in the project root with the following content:   ```env
   OPENAI_API_KEY=your_openai_api_key
   TAVILY_API_KEY=your_tavily_api_key   ```

### Usage

Run the script to generate a job description:
```bash
python generate_job_description.py
```

By default, the script generates a job description for a "Software Engineer" at "Arche AI - Coding Workflow Automation". You can modify the `run_graph` function call in `generate_job_description.py` to generate descriptions for different roles and companies.

## Streamlit App

To run the Streamlit app, use the following command:
```bash
streamlit run streamlit_app.py
```

### Example

To generate a job description for a "Software Engineer" at "Google", you can modify the `run_graph` function call in `generate_job_description.py` as follows:
```python
run_graph("Google", "Software Engineer")
```

This will generate a job description for a "Software Engineer" at "Google" and save it as `Google_Software Engineer.md`.

## Project Structure

- `generate_job_description.py`: Main script for generating job descriptions.
- `requirements.txt`: List of dependencies for the project.
- `.env_sample`: Sample environment variables file.
- `README.md`: This file.

## Understanding the Workflow

The `generate_job_description.py` script utilizes a graph-based workflow to manage the process of generating job descriptions. Here's a brief overview of the workflow:

1. **Input Node:** Captures the `firm_name` and `role` from the user input.
2. **Search Node:** Uses Tavily to perform web searches and gather information about the company and the role.
3. **Job Description Node:** Employs OpenAI's GPT model to generate a comprehensive job description based on the collected information.
4. **Graph Execution:** The workflow is executed, and the resulting job description is saved as a Markdown file.

### Code Snippet: Defining the State

```python
class State(TypedDict):
    """
    Represents the state object that flows through the graph.
    """
    firm_name: str
    role: str
    search_results: list
    job_description: str
```

### Code Snippet: Adding Nodes to the Graph

```python
graph_builder.add_node("input", input_node)
graph_builder.add_node("search", search_node)
graph_builder.add_node("generate_job_description", job_description_node)
```

### Running the Graph

```python
result = graph.invoke({"firm_name": firm_name, "role": role})
with open(f"{firm_name}{role}.md", "w") as file:
    file.write(result["job_description"].content)
```

## Learning LangGraph

This project serves as a practical example to learn **LangGraph**, a powerful library for building state-based workflows. By examining the `generate_job_description.py` script, you can understand how to define states, add nodes, and manage the flow of data through the graph.

### Key Concepts

- **StateGraph:** Manages the states and transitions in the workflow.
- **Nodes:** Represent individual tasks or steps in the workflow.
- **Edges:** Define the order and dependencies between nodes.

For more detailed information, refer to the [LangGraph Documentation](https://github.com/langgraph/langgraph).

## Contributing

Contributions are welcome! Please open an issue or submit a pull request for any improvements or bug fixes.

## License

This project is licensed under the [MIT License](LICENSE).

## Acknowledgements

- [LangGraph](https://github.com/langgraph/langgraph)
- [LangChain](https://github.com/langchain-ai/langchain)
- [OpenAI](https://openai.com/)
- [Tavily](https://tavily.com/)