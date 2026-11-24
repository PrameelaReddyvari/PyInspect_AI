from analyzer.syntax_checker import check_syntax
from analyzer.quality_checker import check_code_quality
from analyzer.security_checker import check_security


def analyze_code(source_code):

    # Step 1: Check input
    if not isinstance(source_code, str) or not source_code.strip():
        return {
            "success": False,
            "message": "Please enter Python code.",
            "syntax": None,
            "quality": None,
            "security": None
        }

    # Step 2: Syntax analysis
    syntax_result = check_syntax(source_code)

    # Stop further checks if syntax is invalid
    if not syntax_result["success"]:
        return {
            "success": False,
            "message": "Syntax errors detected. Fix them before further analysis.",
            "syntax": syntax_result,
            "quality": None,
            "security": None
        }

    # Step 3: Code quality analysis
    quality_result = check_code_quality(source_code)

    # Step 4: Security analysis
    security_result = check_security(source_code)

    # Step 5: Return combined results
    return {
        "success": (
            quality_result["success"]
            and security_result["success"]
        ),
        "message": "Code analysis completed.",
        "syntax": syntax_result,
        "quality": quality_result,
        "security": security_result
    }