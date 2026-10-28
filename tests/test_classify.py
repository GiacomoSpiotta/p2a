from p2a.report import Signals
from p2a.classify import classify


def test_text_only():
    d = classify("x", Signals())
    assert d.primary_class == "text_only"


def test_library():
    s = Signals(languages={"python": 10}, install_files=["pyproject.toml"],
                tutorial_files=["docs/tutorial.ipynb"], notebooks=1, has_tests=True,
                data_files=1, functions_per_script={"a.py": 5, "b.py": 4})
    d = classify("x", s)
    assert d.primary_class == "library"
    assert d.recoverability == "high"


def test_monolithic():
    s = Signals(languages={"python": 1}, data_files=1,
                functions_per_script={"analysis.py": 0})
    d = classify("x", s)
    assert d.primary_class == "monolithic"
    assert "install_spec" in d.missing


def test_missing_data_overrides_structure():
    s = Signals(languages={"python": 2}, install_files=["requirements.txt"],
                functions_per_script={"run.py": 4})
    d = classify("x", s)
    assert d.primary_class == "missing_data"
    assert "data" in d.missing
