import streamlit as st
from code_fetcher import fetch_code
from static_analysis import run_static_analysis
from llm_review import get_code_review

def main():
    st.title("Coderate: Automated Code Review")

    repo_url = st.text_input("GitHub Repo URL or Local Path:")
    analysis_types = st.multiselect(
        "Analysis Types",
        ["Style", "Debug", "Security"],
        default=["Style", "Debug"]
    )
    
    if st.button("Analyze Code") and repo_url and analysis_types:
        with st.spinner("Analyzing code..."):
            try:
                # Fetch code
                code_snippets = fetch_code(repo_url)
                
                if not code_snippets:
                    st.warning("No Python files found!")
                    return
                
                # Process each file
                for file_name, code in code_snippets:
                    with st.expander(f"File: {file_name}"):
                        st.code(code, language='python')
                        
                        # Static analysis
                        analysis_results = run_static_analysis(code, analysis_types)
                        if analysis_results:
                            st.subheader("Static Analysis Results")
                            st.text(analysis_results)
                            
                            # AI Review
                            st.subheader("AI Suggestions")
                            suggestions = get_code_review(code, analysis_results)
                            st.markdown(suggestions)
                        else:
                            st.success("No static analysis issues found!")
                
            except Exception as e:
                st.error(f"Analysis failed: {str(e)}")


if __name__ == "__main__":
    main()