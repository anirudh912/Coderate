import streamlit as st
from code_fetcher import fetch_code
from static_analysis import run_static_analysis
from llm_review import get_code_review
from report_gen import generate_report

def main():
    st.title("Coderate: AI-Powered Code Review")
    
    # input fields
    repo_url = st.text_input("GitHub Repo URL or Local Path:")
    analysis_types = st.multiselect(
        "Analysis Types",
        ["Style", "Debug", "Security"],
        default=["Style", "Debug"]
    )
    
    if st.button("Analyze Code") and repo_url and analysis_types:
        with st.spinner("Analyzing code..."):
            try:
                # fetch code
                code_snippets = fetch_code(repo_url)
                
                if not code_snippets:
                    st.warning("No Python files found!")
                    return
                
                # process each file
                analysis_results = []
                ai_suggestions = []
                for file_name, code in code_snippets:
                    with st.expander(f"File: {file_name}"):
                        st.code(code, language='python')
                        
                        # static analysis
                        analysis_result = run_static_analysis(code, analysis_types)
                        analysis_results.append(analysis_result)
                        if analysis_result:
                            st.subheader("Static Analysis Results")
                            st.text(analysis_result)
                            
                            # ai review
                            suggestion = get_code_review(code, analysis_result)
                            ai_suggestions.append(suggestion)
                            st.subheader("AI Suggestions")
                            st.markdown(suggestion)
                        else:
                            st.success("No static analysis issues found!")
                
                # generate and download report
                report = generate_report(code_snippets, analysis_results, ai_suggestions)
                st.download_button(
                    "Download Report",
                    data=report,
                    file_name="code_review_report.md",
                    mime="text/markdown"
                )
                
            except Exception as e:
                st.error(f"Analysis failed: {str(e)}")

if __name__ == "__main__":
    main()
