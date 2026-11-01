"""Conservative, non-executing scene implementation classification.

Presence is not a quality verdict: renders and director review still decide that.
Short scenes can delegate drawings to helpers; line count is not evidence of a stub.
"""
import ast


def implementation_state(source):
    try:
        tree = ast.parse(source)
    except SyntaxError:
        return "invalid"
    constructs = [n for cls in tree.body if isinstance(cls, ast.ClassDef)
                  for n in cls.body if isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef))
                  and n.name == "construct"]
    if not constructs:
        # Inherited implementations cannot be decided without importing user code.
        return "built" if any(isinstance(n, ast.ClassDef) for n in tree.body) else "skeleton"
    timing = {"say", "wait", "wait_until", "until"}
    for construct in constructs:
        for node in ast.walk(construct):
            if isinstance(node, ast.Call):
                f = node.func
                if isinstance(f, ast.Attribute) and f.attr in timing:
                    continue
                if isinstance(f, ast.Name) and f.id in {"range", "enumerate", "NotImplementedError"}:
                    continue
                # A visual or delegated helper call is implementation evidence.
                return "built"
    return "skeleton"
