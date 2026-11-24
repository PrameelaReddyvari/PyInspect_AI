import ast


class SecurityAnalyzer(ast.NodeVisitor):

    def __init__(self):
        self.issues = []

    def add_issue(self, node, rule, message, severity="High"):
        self.issues.append({
            "rule": rule,
            "message": message,
            "severity": severity,
            "line": node.lineno
        })

    def visit_Call(self, node):

        function_name = ""

        if isinstance(node.func, ast.Name):
            function_name = node.func.id

        elif isinstance(node.func, ast.Attribute):
            function_name = node.func.attr

        # Detect eval()
        if function_name == "eval":
            self.add_issue(
                node, "SEC001",
                "Avoid eval(). It can execute untrusted input."
            )

        # Detect exec()
        elif function_name == "exec":
            self.add_issue(
                node, "SEC002",
                "Avoid exec(). It can execute arbitrary code."
            )

        # Detect os.system()
        elif function_name == "system":
            self.add_issue(
                node, "SEC003",
                "Review system command execution for security risks."
            )

        # Detect subprocess calls using shell=True
        elif function_name in ("run", "Popen", "call"):
            for keyword in node.keywords:
                if (
                    keyword.arg == "shell"
                    and isinstance(keyword.value, ast.Constant)
                    and keyword.value.value is True
                ):
                    self.add_issue(
                        node, "SEC004",
                        "subprocess with shell=True can create command injection risks."
                    )

        # Detect unsafe pickle loading
        elif function_name in ("loads", "load"):
            if isinstance(node.func, ast.Attribute):
                if node.func.value.id if isinstance(
                    node.func.value, ast.Name
                ) else False:
                    module_name = node.func.value.id

                    if module_name == "pickle":
                        self.add_issue(
                            node, "SEC005",
                            "Untrusted pickle data can execute malicious code."
                        )

        self.generic_visit(node)


def check_security(source_code):

    if not isinstance(source_code, str) or not source_code.strip():
        return {
            "success": False,
            "total_issues": 0,
            "issues": [],
            "message": "Please enter Python code."
        }

    try:
        tree = ast.parse(source_code)

        analyzer = SecurityAnalyzer()
        analyzer.visit(tree)

        return {
            "success": True,
            "total_issues": len(analyzer.issues),
            "issues": analyzer.issues,
            "message": (
                "No selected security patterns detected."
                if not analyzer.issues
                else "Potential security risks detected."
            )
        }

    except SyntaxError as error:
        return {
            "success": False,
            "total_issues": 0,
            "issues": [],
            "message": f"Syntax error on line {error.lineno}: {error.msg}"
        }