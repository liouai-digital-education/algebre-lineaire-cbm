"""Exécute chaque notebook rédigé de bout en bout, dans une copie temporaire.

Les cellules marquées « raises-exception » (erreurs volontaires) peuvent lever une exception.
Nécessite nbclient et ipykernel : pip install -r requirements.txt
"""
import json
import pathlib
import shutil

import nbformat
import pytest
from nbclient import NotebookClient

RACINE = pathlib.Path(__file__).resolve().parent.parent


def notebooks_rediges():
    for chemin in sorted((RACINE / "fr").rglob("*.ipynb")):
        if ".ipynb_checkpoints" in chemin.parts:
            continue
        meta = json.loads(chemin.read_text(encoding="utf-8"))["metadata"].get("cbm", {})
        if meta.get("statut") == "rédigé":
            yield chemin


@pytest.mark.parametrize("chemin", list(notebooks_rediges()), ids=lambda p: p.name)
def test_notebook_s_execute(chemin, tmp_path):
    # Copie du dossier du module : les données sont trouvées, et progression.json est écrit hors du dépôt
    copie = tmp_path / chemin.parent.name
    shutil.copytree(chemin.parent, copie)
    nb = nbformat.read(copie / chemin.name, as_version=4)
    NotebookClient(nb, timeout=120, kernel_name="python3",
                   resources={"metadata": {"path": str(copie)}}).execute()
