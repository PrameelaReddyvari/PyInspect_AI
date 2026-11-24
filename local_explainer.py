
import ast


def explain_python_code(source_code, analysis_results=None):
    """
    Generate a beginner-friendly Python explanation locally.
    Does not require an internet connection or Gemini API.
    """

    if not source_code or not source_code.strip():
        return {
            "success": False,
            "explanation": "Please enter Python code."
        }

    try:
        tree = ast.parse(source_code)
    except SyntaxError as error:
        return {
            "success": False,
            "explanation": (
                f"Python syntax error on line {error.lineno}: "
                f"{error.msg}"
            )
        }

    explanations = []

    explanations.append("PROGRAM OVERVIEW")
    explanations.append(
        "This program contains Python statements that are "
        "analyzed using Python's built-in AST module."
    )

    explanations.append("\nLINE-BY-LINE EXPLANATION")

    for line_number, line in enumerate(source_code.splitlines(), 1):
        if not line.strip():
            continue

        explanations.append(
            f"Line {line_number}: {line.strip()}"
        )

    explanations.append("\nPYTHON CONCEPTS")

    concepts = set()

    for node in ast.walk(tree):

        if isinstance(node, ast.FunctionDef):
            concepts.add("Functions")

        elif isinstance(node, ast.For):
            concepts.add("For loops")

        elif isinstance(node, ast.While):
            concepts.add("While loops")

        elif isinstance(node, ast.If):
            concepts.add("Conditional statements")

        elif isinstance(node, (ast.List, ast.ListComp)):
            concepts.add("Lists")

        elif isinstance(node, (ast.Dict, ast.DictComp)):
            concepts.add("Dictionaries")

        elif isinstance(node, ast.ClassDef):
            concepts.add("Classes")

        elif isinstance(node, ast.Try):
            concepts.add("Exception handling")

        elif isinstance(node, ast.Import):
            concepts.add("Module imports")

        elif isinstance(node, ast.Lambda):
            concepts.add("Lambda functions")

    if concepts:
        for concept in sorted(concepts):
            explanations.append(f"- {concept}")
    else:
        explanations.append(
            "- Basic Python statements and expressions"
        )

    explanations.append("\nFUNCTIONS")

    functions = [
        node for node in ast.walk(tree)
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef))
    ]

    if functions:
        for function in functions:
            arguments = [
                arg.arg for arg in function.args.args
            ]

            explanations.append(
                f"- {function.name}(): accepts arguments "
                f"{', '.join(arguments) if arguments else 'none'}."
            )
    else:
        explanations.append("No functions were detected.")

    explanations.append("\nEXECUTION FLOW")

    explanations.append(
        "Python normally executes top-level statements from "
        "top to bottom. Function bodies run when their functions "
        "are called. Loops repeat statements and conditions "
        "select which statements execute."
    )

    explanations.append("\nINPUT AND OUTPUT")

    has_input = any(
        isinstance(node, ast.Call)
        and isinstance(node.func, ast.Name)
        and node.func.id == "input"
        for node in ast.walk(tree)
    )

    has_print = any(
        isinstance(node, ast.Call)
        and isinstance(node.func, ast.Name)
        and node.func.id == "print"
        for node in ast.walk(tree)
    )

    explanations.append(
        "Input detected: " + ("Yes" if has_input else "Not detected")
    )

    explanations.append(
        "Print output detected: " + ("Yes" if has_print else "Not detected")
    )

    explanations.append(
        "This analyzer does not execute the submitted program, "
        "so it does not calculate runtime output."
    )

    explanations.append("\nLEARNING POINT")

    explanations.append(
        "Read the program carefully, identify its functions "
        "and control structures, and understand how data moves "
        "through the statements."
    )

    return {
        "success": True,
        "explanation": "\n".join(explanations),
        "model": "Local Python Explainer",
        "method": "local"
    }

