import json
import os
import subprocess
import sys
import tempfile


def check_code_quality(source_code):

    if not isinstance(source_code, str) or not source_code.strip():
        return {
            "success": False,
            "issues": [],
            "message": "Please enter Python code."
        }

    temp_path = None

    try:
        # Create a temporary Python file
        with tempfile.NamedTemporaryFile(
            mode="w",
            encoding="utf-8",
            suffix=".py",
            delete=False
        ) as temp_file:

            temp_file.write(source_code)
            temp_path = temp_file.name

        # Run Ruff without executing the submitted code
        result = subprocess.run(
            [
                sys.executable,
                "-m",
                "ruff",
                "check",
                "--output-format",
                "json",
                temp_path
            ],
            capture_output=True,
            text=True,
            timeout=10
        )

        # Read Ruff results
        if result.returncode not in (0, 1):
            return {
                "success": False,
                "issues": [],
                "message": "Code quality analysis could not be completed."
            }

        findings = json.loads(result.stdout)

        issues = []

        for finding in findings:
            issues.append({
                "code": finding.get("code"),
                "message": finding.get("message"),
                "line": finding.get("location", {}).get("row"),
                "column": finding.get("location", {}).get("column"),
                "fix_available": finding.get("fix") is not None
            })

        return {
            "success": True,
            "total_issues": len(issues),
            "issues": issues,
            "message": (
                "No code quality issues found."
                if not issues
                else "Code quality issues detected."
            )
        }

    except subprocess.TimeoutExpired:
        return {
            "success": False,
            "issues": [],
            "message": "Analysis timed out."
        }

    except (OSError, json.JSONDecodeError):
        return {
            "success": False,
            "issues": [],
            "message": "Unable to complete code quality analysis."
        }

    finally:
        if temp_path and os.path.exists(temp_path):
            os.remove(temp_path)