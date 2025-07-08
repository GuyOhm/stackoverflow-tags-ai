from pathlib import Path

def get_project_root() -> Path:
    """
    Traverses up the directory tree to find the project root,
    marked by the presence of the `pyproject.toml` file.
    """
    current_path = Path.cwd()
    while not (current_path / "pyproject.toml").exists():
        if current_path.parent == current_path:
            raise FileNotFoundError("Could not find project root with 'pyproject.toml'")
        current_path = current_path.parent
    return current_path 