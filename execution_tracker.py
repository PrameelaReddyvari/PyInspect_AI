
import ast
import json
import os
import subprocess
import sys
import tempfile
import textwrap


MAX_CODE_SIZE = 50 * 1024
MAX_STEPS = 100
TIMEOUT_SECONDS = 3


def analyze_execution(code):
    """
    Capture line-by-line execution, variable values,
    printed output and runtime errors.

    Intended for local development and trusted code only.
    Subprocess timeouts are not a security sandbox.
    """

    if not isinstance(code, str) or not code.strip():
        return {
            "success": False,
            "error": "Please enter Python code.",
            "steps": [],
            "output": ""
        }

    if len(code.encode("utf-8")) > MAX_CODE_SIZE:
        return {
            "success": False,
            "error": "Code exceeds the 50 KB limit.",
            "steps": [],
            "output": ""
        }

    runner = textwrap.dedent("""
        import sys
        import json
        import traceback
        import contextlib
        import io

        source_path = sys.argv[1]
        result_path = sys.argv[2]

        steps = []
        output_buffer = io.StringIO()
        error = None
        truncated = False

        def safe_value(value):
            try:
                result = repr(value)
                return result[:300]
            except Exception:
                return "<Unable to display>"

        def trace_function(frame, event, arg):
            global truncated

            if frame.f_code.co_filename != source_path:
                return trace_function

            if event == "line":
                if len(steps) >= 100:
                    truncated = True
                    raise RuntimeError("Execution step limit reached.")

                variables = {}

                for name, value in frame.f_locals.items():
                    if not name.startswith("__"):
                        variables[name] = safe_value(value)

                steps.append({
                    "line": frame.f_lineno,
                    "event": "line",
                    "variables": variables
                })

            return trace_function

        try:
            with open(source_path, "r", encoding="utf-8") as file:
                code = file.read()

            compiled_code = compile(code, source_path, "exec")

            execution_globals = {
                "__name__": "__main__"
            }

            with contextlib.redirect_stdout(output_buffer):
                sys.settrace(trace_function)

                try:
                    exec(compiled_code, execution_globals)
                finally:
                    sys.settrace(None)

        except Exception as exc:
            sys.settrace(None)
            error = str(exc)

        result = {
            "success": error is None,
            "steps": steps,
            "output": output_buffer.getvalue()[:10000],
            "error": error,
            "truncated": truncated
        }

        with open(result_path, "w", encoding="utf-8") as file:
            json.dump(result, file)
    """)

    try:
        with tempfile.TemporaryDirectory() as temp_dir:

            source_path = os.path.join(temp_dir, "user_code.py")
            result_path = os.path.join(temp_dir, "result.json")

            with open(source_path, "w", encoding="utf-8") as file:
                file.write(code)

            try:
                subprocess.run(
                    [
                        sys.executable,
                        "-I",
                        "-c",
                        runner,
                        source_path,
                        result_path
                    ],
                    capture_output=True,
                    text=True,
                    timeout=TIMEOUT_SECONDS
                )

            except subprocess.TimeoutExpired:
                return {
                    "success": False,
                    "error": "Execution timed out after 3 seconds.",
                    "steps": [],
                    "output": ""
                }

            if not os.path.exists(result_path):
                return {
                    "success": False,
                    "error": "Unable to retrieve execution results.",
                    "steps": [],
                    "output": ""
                }

            with open(result_path, "r", encoding="utf-8") as file:
                return json.load(file)

    except Exception as exc:
        return {
            "success": False,
            "error": str(exc),
            "steps": [],
            "output": ""
        }
