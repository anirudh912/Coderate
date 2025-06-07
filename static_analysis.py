import subprocess
import tempfile
import os
from typing import List

def run_static_analysis(file_content: str, analysis_types: List[str]) -> str:
    analysis_output = []
    try:
        with tempfile.NamedTemporaryFile(suffix='.py', delete=False, mode='w') as f:
            f.write(file_content)
            temp_path = f.name

        if "Style" in analysis_types:
            flake8_out = subprocess.run(['flake8', temp_path], capture_output=True, text=True)
            analysis_output.append(f"flake8:\n{flake8_out.stdout}")

        if "Debug" in analysis_types:
            pylint_out = subprocess.run(['pylint', temp_path], capture_output=True, text=True)
            analysis_output.append(f"pylint:\n{pylint_out.stdout}")

        if "Security" in analysis_types:
            bandit_out = subprocess.run(['bandit', temp_path], capture_output=True, text=True)
            analysis_output.append(f"bandit:\n{bandit_out.stdout}")

        return '\n'.join(analysis_output)
    except Exception as e:
        return f"Static analysis error: {str(e)}"
    finally:
        if os.path.exists(temp_path):
            os.unlink(temp_path)