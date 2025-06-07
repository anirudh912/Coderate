from typing import List, Tuple

def generate_report(code_snippets: List[Tuple[str, str]], analysis_results: List[str], ai_suggestions: List[str]) -> str:
    """Generate a Markdown report with code, static analysis, and AI suggestions."""
    report_lines = ["# Code Review Report\n"]

    for i, (file_name, code) in enumerate(code_snippets):
        report_lines.append(f"## File: {file_name}\n")
        report_lines.append("### Code:\n")
        report_lines.append(f"``````\n")

        if i < len(analysis_results) and analysis_results[i]:
            report_lines.append("### Static Analysis Results:\n")
            report_lines.append(f"``````\n")

        if i < len(ai_suggestions) and ai_suggestions[i]:
            report_lines.append("### AI Suggestions:\n")
            report_lines.append(ai_suggestions[i] + "\n")

    return "\n".join(report_lines)
