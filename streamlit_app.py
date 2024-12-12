import streamlit as st
from generate_job_description import run_graph

def main():
    st.title("AI Job Description Generator")
    
    # Add description
    st.markdown("""
    This tool generates detailed job descriptions using AI and web search results.
    Simply enter the company name and role below.
    """)
    
    # Input fields
    firm_name = st.text_input("Company Name", placeholder="e.g., Arche AI")
    role = st.text_input("Job Title", placeholder="e.g., Software Engineer")
    
    # Generate button
    if st.button("Generate Job Description"):
        if firm_name and role:
            with st.spinner("Generating job description..."):
                try:
                    # Run the graph
                    run_graph(firm_name, role)
                    
                    # Read the generated file
                    with open(f"{firm_name}_{role}.md", "r") as file:
                        job_description = file.read()
                    
                    # Create tabs for different views
                    tab1, tab2 = st.tabs(["Formatted Preview", "Raw Text"])
                    
                    with tab1:
                        st.markdown("### Generated Job Description")
                        st.markdown(job_description)
                    
                    with tab2:
                        st.text_area("Raw Text (Copy/Paste)", value=job_description, height=400)
                    
                    # Add download buttons
                    col1, col2 = st.columns(2)
                    with col1:
                        st.download_button(
                            label="Download as Markdown",
                            data=job_description,
                            file_name=f"{firm_name}_{role}.md",
                            mime="text/markdown"
                        )
                    with col2:
                        st.download_button(
                            label="Download as Text",
                            data=job_description,
                            file_name=f"{firm_name}_{role}.txt",
                            mime="text/plain"
                        )
                except Exception as e:
                    st.error(f"An error occurred: {str(e)}")
        else:
            st.warning("Please enter both company name and job title.")

if __name__ == "__main__":
    main() 