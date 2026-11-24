
import os
import time
from pathlib import Path

from google import genai
from dotenv import load_dotenv

from local_explainer import explain_python_code


BASE_DIR = Path(__file__).resolve().parent
ENV_FILE = BASE_DIR / ".env"

load_dotenv(dotenv_path=ENV_FILE, override=True)

MODEL_NAMES = [
    "gemini-3.1-flash-lite",
    "gemini-3.8-flash"
]

MAX_RETRIES = 2


def explain_code_issues(source_code, analysis_results):

    if not source_code or not source_code.strip():
        return {
            "success": False,
            "message": "Please provide Python code."
        }

    api_key = os.getenv("GEMINI_API_KEY")

    # Try Gemini first when an API key is available
    if api_key:

        try:
            client = genai.Client(api_key=api_key)

            prompt = f"""
You are an expert Python programming teacher.

Explain this Python program in simple English for a beginner.

Use these sections:

1. PROGRAM OVERVIEW
2. LINE-BY-LINE EXPLANATION
3. EXECUTION FLOW
4. PYTHON CONCEPTS
5. INPUT AND OUTPUT
6. ERRORS AND CODE QUALITY
7. IMPROVEMENT SUGGESTIONS
8. LEARNING POINT

Explain the actual code.
Do not execute the code.
Do not invent runtime output.

PYTHON CODE:
{source_code}

STATIC ANALYSIS:
{analysis_results}
"""

            for model_name in MODEL_NAMES:

                for attempt in range(1, MAX_RETRIES + 1):

                    try:
                        print("Trying Gemini:", model_name)

                        response = client.models.generate_content(
                            model=model_name,
                            contents=prompt
                        )

                        explanation = getattr(response, "text", None)

                        if explanation and explanation.strip():
                            return {
                                "success": True,
                                "explanation": explanation,
                                "model": model_name,
                                "method": "gemini"
                            }

                        raise ValueError(
                            "Gemini returned an empty response."
                        )

                    except Exception as error:

                        print(
                            f"Gemini failed: {model_name}, "
                            f"attempt {attempt}: {error}"
                        )

                        message = str(error).upper()

                        temporary_error = any(
                            item in message
                            for item in [
                                "503",
                                "UNAVAILABLE",
                                "429",
                                "RESOURCE_EXHAUSTED",
                                "500",
                                "INTERNAL",
                                "504",
                                "DEADLINE_EXCEEDED"
                            ]
                        )

                        model_error = any(
                            item in message
                            for item in [
                                "404",
                                "NOT_FOUND",
                                "MODEL_NOT_FOUND"
                            ]
                        )

                        if model_error:
                            break

                        if temporary_error:
                            if attempt < MAX_RETRIES:
                                time.sleep(attempt * 2)
                            continue

                        # For other Gemini errors, use local fallback.
                        print("Using local explanation fallback.")
                        raise error

        except Exception as error:
            print("Gemini unavailable:", repr(error))

    else:
        print("Gemini API key missing. Using local explanation.")

    # Automatic local fallback
    try:
        print("Generating explanation using local Python analyzer.")

        result = explain_python_code(
            source_code,
            analysis_results
        )

        if result.get("success"):
            result["method"] = "local"
            result["model"] = "Local Python Explainer"
            result["message"] = (
                "Gemini was unavailable. "
                "A local explanation was generated instead."
            )

            return result

        return result

    except Exception as error:
        print("Local explanation failed:", repr(error))

        return {
            "success": False,
            "message": (
                "Both Gemini and local explanation failed. "
                f"Details: {str(error)}"
            )
        }

    # If all Gemini models fail, generate local explanation
    result = explain_python_code(source_code, analysis_results)

    result["method"] = "local"
    result["model"] = "Local Python Explainer"

    return result
