
import ast
import re


def calculate_quality_score(source_code):

    try:
        tree = ast.parse(source_code)

    except SyntaxError as error:
        return {
            "success": False,
            "message": f"Syntax error on line {error.lineno}: {error.msg}"
        }

    lines = source_code.splitlines()

    code_lines = [
        line for line in lines if line.strip()
    ]

    comment_lines = [
        line for line in lines
        if line.strip().startswith("#")
    ]

    functions = [
        node for node in ast.walk(tree)
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef))
    ]

    loops = [
        node for node in ast.walk(tree)
        if isinstance(node, (ast.For, ast.While))
    ]

    conditions = [
        node for node in ast.walk(tree)
        if isinstance(node, ast.If)
    ]

    classes = [
        node for node in ast.walk(tree)
        if isinstance(node, ast.ClassDef)
    ]

    complexity = 1 + sum(
        isinstance(node, (ast.If, ast.For, ast.While, ast.And, ast.Or))
        for node in ast.walk(tree)
    )

    # Category scores
    breakdown = {
        "Code Structure": 20,
        "Readability": 20,
        "Naming Conventions": 20,
        "Code Complexity": 20,
        "Best Practices": 20
    }

    suggestions = []

    # Readability
    long_lines = [
        line for line in code_lines if len(line) > 100
    ]

    if long_lines:
        breakdown["Readability"] -= min(10, len(long_lines) * 2)
        suggestions.append("Reduce long lines to improve readability.")

    if len(code_lines) >= 10 and not comment_lines:
        breakdown["Readability"] -= 3
        suggestions.append("Add meaningful comments where necessary.")

    # Structure
    if len(code_lines) > 20 and not functions:
        breakdown["Code Structure"] -= 5
        suggestions.append("Divide lengthy code into reusable functions.")

    if len(code_lines) > 40 and not classes and not functions:
        breakdown["Code Structure"] -= 3
        suggestions.append("Consider organizing related logic into functions or classes.")

    # Naming conventions
    bad_names = []

    for node in ast.walk(tree):
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
            if not re.fullmatch(r"[a-z_][a-z0-9_]*", node.name):
                bad_names.append(node.name)

    if bad_names:
        breakdown["Naming Conventions"] -= 5
        suggestions.append("Use consistent Python naming conventions.")

    # Complexity
    if complexity > 15:
        breakdown["Code Complexity"] -= 10
        suggestions.append("Simplify complex logic and nested conditions.")

    elif complexity > 8:
        breakdown["Code Complexity"] -= 5
        suggestions.append("Consider breaking complex logic into smaller functions.")

    # Best practices
    if "except:" in source_code:
        breakdown["Best Practices"] -= 5
        suggestions.append("Avoid bare except statements.")

    if source_code and not source_code.endswith("\n"):
        breakdown["Best Practices"] -= 2
        suggestions.append("Add a newline at the end of the file.")

    # Calculate final score
    score = sum(breakdown.values())

    if score >= 85:
        rating = "Excellent"
        recommendation = "Your code follows good coding practices."
    elif score >= 70:
        rating = "Good"
        recommendation = "Your code is good, but some improvements are possible."
    elif score >= 50:
        rating = "Needs Improvement"
        recommendation = "Focus on improving readability and structure."
    else:
        rating = "Poor"
        recommendation = "Review your code structure and coding practices."

    if not suggestions:
        suggestions.append("No major issues detected by the current checks.")

    return {
        "success": True,
        "score": score,
        "rating": rating,
        "breakdown": breakdown,
        "suggestions": suggestions,
        "statistics": {
            "total_lines": len(lines),
            "code_lines": len(code_lines),
            "comment_lines": len(comment_lines),
            "functions": len(functions),
            "loops": len(loops),
            "conditions": len(conditions),
            "classes": len(classes),
            "complexity_indicator": complexity
        },
        "recommendation": recommendation
    }
