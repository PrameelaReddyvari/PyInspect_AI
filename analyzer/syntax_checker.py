import ast


def check_syntax(source_code):

    if not source_code.strip():
        return {
            "success": False,
            "errors": [{
                "type": "Empty Code",
                "message": "Please enter Python code.",
                "line": None,
                "column": None
            }]
        }

    try:
        ast.parse(source_code)

        return {
            "success": True,
            "errors": [],
            "message": "No syntax errors found."
        }

    except SyntaxError as error:
        return {
            "success": False,
            "errors": [{
                "type": "Syntax Error",
                "message": error.msg,
                "line": error.lineno,
                "column": error.offset
            }]
        }