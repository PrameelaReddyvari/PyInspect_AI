
from flask import Flask, request, jsonify, render_template

from code_checker import analyze_code
from ai_service import explain_code_issues
from execution_tracker import analyze_execution
from practice_generator import detect_concepts, generate_practice_questions
from quality_scorer import calculate_quality_score
from bug_predictor import predict_bugs

app = Flask(__name__)

app.config["MAX_CONTENT_LENGTH"] = 50 * 1024


# ========================================
# COMMON CODE VALIDATION
# ========================================

def get_source_code():

    data = request.get_json(silent=True)

    if not isinstance(data, dict):
        return None, jsonify({
            "success": False,
            "message": "Invalid request."
        }), 400

    source_code = data.get("code", "")

    if not isinstance(source_code, str):
        return None, jsonify({
            "success": False,
            "message": "Code must be text."
        }), 400

    source_code = source_code.strip()

    if not source_code:
        return None, jsonify({
            "success": False,
            "message": "Please enter Python code."
        }), 400

    if len(source_code) > 50000:
        return None, jsonify({
            "success": False,
            "message": "Code exceeds the 50 KB limit."
        }), 413

    return source_code, None, None


# ========================================
# HOME PAGE
# ========================================

@app.route("/")
def home():
    return render_template("index.html")


# ========================================
# HEALTH CHECK
# ========================================

@app.route("/health")
def health():
    return jsonify({
        "success": True,
        "message": "PyInspect AI is running."
    })


# ========================================
# FEATURE 1: PYTHON CODE ANALYSIS
# ========================================

@app.route("/api/analyze", methods=["POST"])
def analyze():

    source_code, error_response, status_code = get_source_code()

    if error_response:
        return error_response, status_code

    try:
        result = analyze_code(source_code)

        return jsonify({
            "success": True,
            "analysis": result
        })

    except Exception:
        app.logger.exception("Code analysis failed")

        return jsonify({
            "success": False,
            "message": "Code analysis failed."
        }), 500


# ========================================
# FEATURE 2: AI CODE EXPLANATION
# ========================================

@app.route("/api/ai-explain", methods=["POST"])
def ai_explain():

    source_code, error_response, status_code = get_source_code()

    if error_response:
        return error_response, status_code

    try:
        analysis_results = analyze_code(source_code)

        explanation = explain_code_issues(
            source_code,
            analysis_results
        )

        return jsonify({
            "success": True,
            "explanation": explanation
        })

    except Exception:
        app.logger.exception("AI explanation failed")

        return jsonify({
            "success": False,
            "message": "AI explanation failed. Check the terminal."
        }), 500


# ========================================
# FEATURE 3: CODE QUALITY SCORE
# ========================================

@app.route("/api/quality-score", methods=["POST"])
def quality_score():

    source_code, error_response, status_code = get_source_code()

    if error_response:
        return error_response, status_code

    try:
        result = calculate_quality_score(source_code)

        return jsonify({
            "success": True,
            "quality": result
        })

    except Exception:
        app.logger.exception("Quality scoring failed")

        return jsonify({
            "success": False,
            "message": "Quality scoring failed. Check the terminal."
        }), 500


# ========================================
# FEATURE 4: VISUAL EXECUTION TRACKER
# ========================================

@app.route("/api/trace", methods=["POST"])
def trace():

    source_code, error_response, status_code = get_source_code()

    if error_response:
        return error_response, status_code

    try:
        result = analyze_execution(source_code)

        if not isinstance(result, dict):
            return jsonify({
                "success": False,
                "message": "Invalid execution tracker response."
            }), 500

        return jsonify(result), 200 if result.get("success") else 422

    except Exception:
        app.logger.exception("Execution tracking failed")

        return jsonify({
            "success": False,
            "message": "Execution tracking failed. Check the terminal."
        }), 500


# ========================================
# FEATURE 5: AI PYTHON PRACTICE GENERATOR
# ========================================

@app.route("/api/practice", methods=["POST"])
def practice():

    source_code, error_response, status_code = get_source_code()

    if error_response:
        return error_response, status_code

    try:
        # Detect concepts from the submitted code
        detected = detect_concepts(source_code)

        # Extract the actual concepts list
        if isinstance(detected, dict):
            concepts = detected.get("concepts", [])
        else:
            concepts = detected

        # Generate questions using the concepts list
        questions = generate_practice_questions(concepts)

        return jsonify({
            "success": True,
            "concepts": concepts,
            "questions": questions
        })

    except Exception:
        app.logger.exception("Practice generation failed")

        return jsonify({
            "success": False,
            "message": "Practice generation failed. Check the terminal."
        }), 500


# ========================================
# FEATURE 6: SMART BUG PREDICTOR
# ========================================

@app.route("/api/bug-predict", methods=["POST"])
def bug_predict():

    source_code, error_response, status_code = get_source_code()

    if error_response:
        return error_response, status_code

    try:
        result = predict_bugs(source_code)

        if not isinstance(result, dict):
            return jsonify({
                "success": False,
                "message": "Invalid bug predictor response."
            }), 500

        if not result.get("success"):
            return jsonify(result), 422

        return jsonify(result)

    except Exception:
        app.logger.exception("Bug prediction failed")

        return jsonify({
            "success": False,
            "message": "Bug prediction failed. Check the terminal."
        }), 500


# ========================================
# ERROR HANDLERS
# ========================================

@app.errorhandler(404)
def page_not_found(error):

    if request.path.startswith("/api/"):
        return jsonify({
            "success": False,
            "message": "API endpoint not found."
        }), 404

    return "Page not found.", 404


@app.errorhandler(413)
def request_too_large(error):

    return jsonify({
        "success": False,
        "message": "Request is too large. Maximum size is 50 KB."
    }), 413


# ========================================
# RUN APPLICATION
# ========================================

if __name__ == "__main__":
    app.run(debug=True)
