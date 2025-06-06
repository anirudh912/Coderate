import os
import tempfile
from pathlib import Path
import shutil
import git

def fetch_code(repo_or_path: str) -> list[tuple[str, str]]:
    """Fetch code from a GitHub repo or local path."""
    code_snippets = []
    try:
        if repo_or_path.startswith(('http://', 'https://', 'git@')):
            # clone GitHub repo
            temp_dir = tempfile.mkdtemp()
            try:
                git.Repo.clone_from(repo_or_path, temp_dir)
                repo_dir = Path(temp_dir)
                for py_file in repo_dir.rglob('*.py'):
                    with open(py_file, 'r') as f:
                        code_snippets.append((str(py_file.relative_to(repo_dir)), f.read()))
            finally:
                if os.path.exists(temp_dir):
                    shutil.rmtree(temp_dir)
        else:
            # read local path
            path = Path(repo_or_path)
            if path.is_file() and path.suffix == '.py':
                with open(path, 'r') as f:
                    code_snippets.append((str(path.name), f.read()))
            elif path.is_dir():
                for py_file in path.rglob('*.py'):
                    with open(py_file, 'r') as f:
                        code_snippets.append((str(py_file.relative_to(path)), f.read()))
        return code_snippets
    except Exception as e:
        raise RuntimeError(f"Error fetching code: {str(e)}")
