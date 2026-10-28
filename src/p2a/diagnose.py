"""Diagnosi statica: legge i file del repository e produce i segnali.

Nessun codice viene eseguito. Costa secondi e non ha bisogno di un modello.
"""

from pathlib import Path
import ast
import re

from .report import Signals

INSTALL_FILES = {
    "pyproject.toml", "setup.py", "setup.cfg", "requirements.txt",
    "environment.yml", "environment.yaml", "Pipfile", "poetry.lock",
    "DESCRIPTION", "renv.lock", "Project.toml",
}
CONFIG_SUFFIXES = {".yaml", ".yml", ".toml", ".json", ".cfg", ".ini"}
DATA_SUFFIXES = {".csv", ".tsv", ".h5", ".h5ad", ".parquet", ".npy", ".npz",
                 ".rds", ".rda", ".fasta", ".fa", ".bed", ".vcf", ".xlsx"}
LANG_SUFFIXES = {".py": "python", ".R": "r", ".r": "r", ".ipynb": "notebook",
                 ".jl": "julia", ".m": "matlab", ".sh": "shell"}
TUTORIAL_HINT = re.compile(r"tutorial|example|demo|vignette|notebook|quickstart", re.I)
ABS_PATH = re.compile(r"""['"](/home/|/Users/|/mnt/|/data/|[A-Z]:\\)""")
DATA_LINK = re.compile(
    r"https?://\S*(zenodo|figshare|doi\.org|dataverse|huggingface\.co/datasets|"
    r"ncbi\.nlm\.nih\.gov/geo|ebi\.ac\.uk|osf\.io|dropbox|drive\.google)\S*", re.I)
SKIP_DIRS = {".git", ".venv", "venv", "node_modules", "__pycache__", ".ipynb_checkpoints"}


def _iter_files(root: Path):
    for p in root.rglob("*"):
        if any(part in SKIP_DIRS for part in p.parts):
            continue
        if p.is_file():
            yield p


def _read(p: Path, limit: int = 400_000) -> str:
    try:
        return p.read_text(errors="ignore")[:limit]
    except OSError:
        return ""


def _count_functions(src: str) -> int:
    try:
        tree = ast.parse(src)
    except SyntaxError:
        return 0
    return sum(isinstance(n, ast.FunctionDef) for n in ast.walk(tree))


def diagnose_static(root: Path) -> Signals:
    s = Signals()
    for p in _iter_files(root):
        rel = str(p.relative_to(root))
        name = p.name
        suffix = p.suffix

        if name in INSTALL_FILES:
            s.install_files.append(rel)
        if name == "Dockerfile":
            s.has_dockerfile = True
        if name.startswith("test_") or "tests" in p.parts or name == "testthat":
            s.has_tests = True
        if suffix in DATA_SUFFIXES:
            s.data_files += 1
        if suffix in CONFIG_SUFFIXES and name not in INSTALL_FILES:
            s.config_files.append(rel)

        lang = LANG_SUFFIXES.get(suffix)
        if lang:
            s.languages[lang] = s.languages.get(lang, 0) + 1
        if suffix == ".ipynb":
            s.notebooks += 1
        if TUTORIAL_HINT.search(rel) and suffix in {".ipynb", ".md", ".Rmd", ".py", ".R"}:
            s.tutorial_files.append(rel)

        if suffix in {".py", ".R", ".Rmd", ".md", ".ipynb"}:
            text = _read(p)
            s.absolute_paths += len(ABS_PATH.findall(text))
            s.data_links.extend(m.group(0) for m in DATA_LINK.finditer(text))
            if suffix == ".py":
                if "argparse" in text or "click" in text or "typer" in text:
                    s.uses_argparse = True
                if "__main__" in text:
                    s.entry_scripts.append(rel)
                s.functions_per_script[rel] = _count_functions(text)

    s.data_links = sorted(set(s.data_links))
    return s
