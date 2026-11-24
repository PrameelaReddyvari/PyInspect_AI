
import ast


def predict_bugs(source_code):
    bugs = []

    try:
        tree = ast.parse(source_code)
    except SyntaxError as error:
        return {
            "success": False,
            "message": f"Syntax error on line {error.lineno}: {error.msg}",
            "bugs": []
        }

    defined_variables = set()
    used_variables = set()

    # Detect possible bugs
    for node in ast.walk(tree):

        # 1. Detect division by zero
        if isinstance(node, ast.BinOp):
            if isinstance(node.op, (ast.Div, ast.FloorDiv, ast.Mod)):
                if isinstance(node.right, ast.Constant):
                    if node.right.value == 0:
                        bugs.append({
                            "bug": "Possible Division by Zero",
                            "line": node.lineno,
                            "severity": "High",
                            "explanation": "The operation uses zero as the divisor.",
                            "suggestion": "Check whether the divisor is zero before performing the operation."
                        })

        # 2. Detect variables
        if isinstance(node, ast.Name):
            if isinstance(node.ctx, ast.Store):
                defined_variables.add(node.id)
            elif isinstance(node.ctx, ast.Load):
                used_variables.add(node.id)

    # 3. Detect variables that are never used
    unused = defined_variables - used_variables

    for variable in unused:
        bugs.append({
            "bug": f"Unused Variable: {variable}",
            "line": 1,
            "severity": "Low",
            "explanation": f"The variable '{variable}' is assigned but never used.",
            "suggestion": "Remove the variable if it is not needed."
        })

    return {
        "success": True,
        "total_bugs": len(bugs),
        "bugs": bugs
    }
