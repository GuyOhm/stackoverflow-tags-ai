from pathlib import Path

def get_project_root() -> Path:
    """
    Remonte l'arborescence pour trouver la racine du projet,
    marquée par la présence du fichier `pyproject.toml`.
    """
    current_path = Path.cwd()
    while not (current_path / "pyproject.toml").exists():
        if current_path.parent == current_path:
            raise FileNotFoundError("Could not find project root with 'pyproject.toml'")
        current_path = current_path.parent
    return current_path 