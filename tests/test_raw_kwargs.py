import ast
import glob
import importlib
import inspect
import pytest

def test_raw_kwargs():
    files = glob.glob("pyrogram/**/*.py", recursive=True)
    issues = []
    for filepath in files:
        if "pyrogram/raw" in filepath or "pyrogram/errors/exceptions" in filepath:
            continue
        with open(filepath, "r", encoding="utf-8") as f:
            tree = ast.parse(f.read(), filepath)
        for node in ast.walk(tree):
            if isinstance(node, ast.Call):
                func = node.func
                parts = []
                while isinstance(func, ast.Attribute):
                    parts.append(func.attr)
                    func = func.value
                if isinstance(func, ast.Name):
                    parts.append(func.id)
                parts.reverse()
                if len(parts) >= 3 and parts[0] == "raw" and parts[1] in ("types", "functions", "base"):
                    mod_path = ".".join(parts[:-1])
                    cls_name = parts[-1]
                    try:
                        mod = importlib.import_module("pyrogram." + mod_path)
                        cls = getattr(mod, cls_name, None)
                    except Exception:
                        cls = None
                    if cls is None:
                        issues.append(f"{filepath}:{node.lineno} - Missing class/function {mod_path}.{cls_name}")
                    else:
                        sig = inspect.signature(cls.__init__)
                        params = sig.parameters
                        for keyword in node.keywords:
                            if keyword.arg is not None and keyword.arg not in params:
                                issues.append(
                                    f"{filepath}:{node.lineno} - {mod_path}.{cls_name} got unexpected kwarg '{keyword.arg}'"
                                )

    assert not issues, "Found raw calls with invalid class or invalid kwargs:\n" + "\n".join(issues)
