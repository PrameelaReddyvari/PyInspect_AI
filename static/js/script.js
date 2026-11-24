
// ========================================
// COMMON HELPER FUNCTIONS
// ========================================

function getCode() {
    return document.getElementById("codeInput").value.trim();
}

function displayMessage(element, message) {
    element.textContent = message;
}

async function sendCodeRequest(url, code) {
    const response = await fetch(url, {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({ code })
    });

    const data = await response.json();

    return { response, data };
}

function createElement(tag, text, parent, className = "") {
    const element = document.createElement(tag);
    element.textContent = text;

    if (className) {
        element.className = className;
    }

    parent.appendChild(element);
    return element;
}

// Convert strings, arrays and objects into readable text.
function formatValue(value) {
    if (value === null || value === undefined) {
        return "Not available";
    }

    if (typeof value === "string") {
        return value;
    }

    if (typeof value === "number" || typeof value === "boolean") {
        return String(value);
    }

    if (Array.isArray(value)) {
        if (value.length === 0) {
            return "None";
        }

        return value.map((item, index) => {
            return `${index + 1}. ${formatValue(item)}`;
        }).join("\n");
    }

    if (typeof value === "object") {
        return Object.entries(value)
            .map(([key, item]) => {
                const formattedKey = key
                    .replaceAll("_", " ")
                    .replace(/\b\w/g, letter => letter.toUpperCase());

                return `${formattedKey}:\n${formatValue(item)}`;
            })
            .join("\n\n");
    }

    return String(value);
}

function normalizeList(value) {
    if (Array.isArray(value)) {
        return value;
    }

    if (value && Array.isArray(value.questions)) {
        return value.questions;
    }

    if (value && Array.isArray(value.items)) {
        return value.items;
    }

    if (value && Array.isArray(value.concepts)) {
        return value.concepts;
    }

    return [];
}

function showLoading(button, message) {
    button.disabled = true;
    button.textContent = message;
}

function hideLoading(button, originalText) {
    button.disabled = false;
    button.textContent = originalText;
}


// ========================================
// FEATURE 1: PYTHON CODE ANALYSIS
// ========================================

async function analyzeCode() {
    const code = getCode();
    const results = document.getElementById("results");
    const button = document.getElementById("analyzeBtn");

    if (!code) {
        displayMessage(results, "Please enter Python code.");
        return;
    }

    showLoading(button, "Analyzing...");
    displayMessage(results, "Checking your Python code...");

    try {
        const { response, data } =
            await sendCodeRequest("/api/analyze", code);

        results.replaceChildren();

        if (!response.ok || !data.success) {
            displayMessage(
                results,
                data.message || "Code analysis failed."
            );
            return;
        }

        // app.py returns the analysis inside data.analysis
        const analysis = data.analysis || data;

        if (analysis.syntax && !analysis.syntax.success) {
            createElement("h3", "Syntax Errors", results);

            (analysis.syntax.errors || []).forEach(error => {
                createElement(
                    "p",
                    `${error.type || "Error"}: ${error.message || ""}` +
                    (error.line ? ` (Line ${error.line})` : ""),
                    results,
                    "result-item error-message"
                );
            });

            return;
        }

        const qualityIssues =
            analysis.quality?.issues ||
            analysis.quality_issues ||
            [];

        const securityIssues =
            analysis.security?.issues ||
            analysis.security_issues ||
            [];

        showIssues("Code Quality", qualityIssues, results);
        showIssues("Security", securityIssues, results);

    } catch (error) {
        console.error("Analysis error:", error);
        displayMessage(results, "Unable to connect to the backend.");
    } finally {
        hideLoading(button, "Analyze Code");
    }
}


// ========================================
// HELPER: DISPLAY ISSUES
// ========================================

function showIssues(title, issues, results) {
    issues = normalizeList(issues);

    createElement(
        "h3",
        `${title}: ${issues.length} issue(s)`,
        results
    );

    if (issues.length === 0) {
        createElement("p", "No issues found.", results);
        return;
    }

    issues.forEach(issue => {
        const message = typeof issue === "string"
            ? issue
            : formatValue(issue);

        createElement(
            "div",
            message,
            results,
            "result-item"
        );
    });
}


// ========================================
// FEATURE 2: AI CODE EXPLANATION
// ========================================

async function explainWithAI() {
    const code = getCode();
    const results = document.getElementById("aiResults");
    const button = document.getElementById("aiExplainBtn");

    if (!code) {
        displayMessage(results, "Please enter Python code first.");
        return;
    }

    showLoading(button, "Getting Explanation...");
    displayMessage(results, "Gemini AI is analyzing your code...");

    try {
        const { response, data } =
            await sendCodeRequest("/api/ai-explain", code);

        results.replaceChildren();

        if (!response.ok || !data.success) {
            displayMessage(
                results,
                data.message || "AI explanation failed."
            );
            return;
        }

        createElement(
            "h3",
            "AI Code Explanation",
            results
        );

        const explanation = data.explanation;

        let explanationText;

        if (typeof explanation === "string") {
            explanationText = explanation;
        } else if (explanation && typeof explanation === "object") {
            // Handle common AI response structures.
            explanationText =
                explanation.explanation ||
                explanation.text ||
                explanation.content ||
                explanation.answer ||
                explanation.message ||
                formatValue(explanation);
        } else {
            explanationText = "No explanation available.";
        }

        const output = createElement(
            "pre",
            explanationText,
            results
        );

        output.style.whiteSpace = "pre-wrap";
        output.style.overflowWrap = "anywhere";

    } catch (error) {
        console.error("AI explanation error:", error);
        displayMessage(results, "Unable to connect to the backend.");
    } finally {
        hideLoading(button, "Explain with AI");
    }
}


// ========================================
// FEATURE 3: COMPLETE CODE QUALITY REPORT
// ========================================

async function checkCodeQuality() {
    const code = getCode();
    const results = document.getElementById("qualityResults");
    const button = document.getElementById("qualityBtn");

    if (!code) {
        displayMessage(results, "Please enter Python code first.");
        return;
    }

    showLoading(button, "Analyzing...");
    displayMessage(results, "Generating quality report...");

    try {
        const { response, data } =
            await sendCodeRequest("/api/quality-score", code);

        results.replaceChildren();

        if (!response.ok || !data.success) {
            displayMessage(
                results,
                data.message || "Quality analysis failed."
            );
            return;
        }

        // app.py returns the report inside data.quality
        const report = data.quality || data;

        createElement(
            "h2",
            "PyInspect AI - Complete Quality Report",
            results
        );

        // Support different common score field names.
        const score =
            report.score ??
            report.quality_score ??
            report.total_score ??
            report.overall_score ??
            "N/A";

        createElement(
            "h1",
            `${score} / 100`,
            results
        );

        const rating =
            report.rating ??
            report.quality_rating ??
            report.grade ??
            "Not available";

        createElement(
            "h3",
            `Quality Rating: ${rating}`,
            results
        );

        // Category-wise analysis
        createElement(
            "h3",
            "Category-wise Analysis",
            results
        );

        const breakdown =
            report.breakdown ||
            report.category_scores ||
            report.categories ||
            report.category_analysis ||
            {};

        if (Object.keys(breakdown).length > 0) {
            Object.entries(breakdown).forEach(
                ([category, value]) => {
                    createElement(
                        "p",
                        `${category}: ${formatValue(value)}`,
                        results
                    );
                }
            );
        } else {
            createElement(
                "p",
                "Category-wise details are not available.",
                results
            );
        }

        // Code statistics
        createElement(
            "h3",
            "Code Statistics",
            results
        );

        const statistics =
            report.statistics ||
            report.code_statistics ||
            report.metrics ||
            {};

        if (Object.keys(statistics).length > 0) {
            Object.entries(statistics).forEach(
                ([name, value]) => {
                    const formattedName = name
                        .replaceAll("_", " ")
                        .replace(/\b\w/g, letter => letter.toUpperCase());

                    createElement(
                        "p",
                        `${formattedName}: ${formatValue(value)}`,
                        results
                    );
                }
            );
        } else {
            createElement(
                "p",
                "Code statistics are not available.",
                results
            );
        }

        // Improvement suggestions
        createElement(
            "h3",
            "Improvement Suggestions",
            results
        );

        const suggestions = normalizeList(
            report.suggestions ||
            report.improvements ||
            report.recommendations
        );

        if (suggestions.length > 0) {
            suggestions.forEach(suggestion => {
                createElement(
                    "p",
                    `• ${formatValue(suggestion)}`,
                    results
                );
            });
        } else {
            createElement(
                "p",
                "No suggestions available.",
                results
            );
        }

        // Final recommendation
        createElement(
            "h3",
            "Final Recommendation",
            results
        );

        const recommendation =
            report.recommendation ||
            report.final_recommendation ||
            report.summary ||
            "No recommendation available.";

        createElement(
            "p",
            formatValue(recommendation),
            results
        );

        // Show complete report in the browser console for debugging.
        console.log("Complete quality report:", report);

    } catch (error) {
        console.error("Quality report error:", error);
        displayMessage(results, "Unable to connect to the backend.");
    } finally {
        hideLoading(button, "Check Code Quality");
    }
}


// ========================================
// FEATURE 4: VISUAL EXECUTION TRACKER
// ========================================

async function traceExecution() {
    const code = getCode();
    const results = document.getElementById("executionResults");
    const button = document.getElementById("traceBtn");

    if (!code) {
        displayMessage(results, "Please enter Python code first.");
        return;
    }

    showLoading(button, "Tracing...");
    displayMessage(results, "Tracking code execution...");

    try {
        const { response, data } =
            await sendCodeRequest("/api/trace", code);

        results.replaceChildren();

        createElement(
            "h2",
            "Visual Execution Tracker",
            results
        );

        if (!response.ok || !data.success) {
            createElement(
                "p",
                data.message || "Execution tracking failed.",
                results
            );
            return;
        }

        // Program output
        createElement("h3", "Program Output", results);

        createElement(
            "pre",
            typeof data.output === "string"
                ? data.output
                : JSON.stringify(data.output ?? "No output", null, 2),
            results
        );

        // Execution steps
        createElement("h3", "Execution Steps", results);

        const steps = data.steps || data.trace || [];

        if (Array.isArray(steps) && steps.length > 0) {
            steps.forEach((step, index) => {
                const stepBox = document.createElement("div");
                stepBox.className = "result-item";

                createElement(
                    "h4",
                    `Step ${index + 1}`,
                    stepBox
                );

                createElement(
                    "p",
                    `Line: ${step.line ?? step.line_number ?? "N/A"}`,
                    stepBox
                );

                createElement(
                    "p",
                    `Variables: ${JSON.stringify(
                        step.locals ?? step.variables ?? {}
                    )}`,
                    stepBox
                );

                results.appendChild(stepBox);
            });
        } else {
            createElement(
                "p",
                "No execution steps were returned by the backend.",
                results
            );
        }

    } catch (error) {
        console.error("Execution tracker error:", error);
        displayMessage(results, "Unable to connect to the backend.");
    } finally {
        hideLoading(button, "Visual Execution Tracker");
    }
}


// ========================================
// FEATURE 5: AI PYTHON PRACTICE GENERATOR
// ========================================

async function generatePractice() {
    const code = getCode();
    const results = document.getElementById("practiceResults");
    const button = document.getElementById("practiceBtn");

    if (!code) {
        displayMessage(results, "Please enter Python code first.");
        return;
    }

    showLoading(button, "Generating...");
    displayMessage(results, "Generating practice questions...");

    try {
        const { response, data } =
            await sendCodeRequest("/api/practice", code);

        results.replaceChildren();

        if (!response.ok || !data.success) {
            displayMessage(
                results,
                data.message || "Practice generation failed."
            );
            return;
        }

        createElement(
            "h2",
            "Your Python Practice Questions",
            results
        );

        // Detected concepts
        createElement(
            "h3",
            "Detected Concepts",
            results
        );

        const concepts = normalizeList(
            data.concepts ||
            data.detected_concepts
        );

        createElement(
            "p",
            concepts.length > 0
                ? concepts.map(formatValue).join(", ")
                : "No concepts detected in the submitted code.",
            results
        );

        // Practice questions
        createElement(
            "h3",
            "Practice Questions",
            results
        );

        const questions = normalizeList(
            data.questions ||
            data.practice_questions
        );

        if (questions.length > 0) {
            questions.forEach((question, index) => {
                const questionText = typeof question === "string"
                    ? question
                    : formatValue(question);

                createElement(
                    "div",
                    `${index + 1}. ${questionText}`,
                    results,
                    "result-item"
                );
            });
        } else {
            createElement(
                "p",
                "No practice questions were returned. Check the practice generator backend.",
                results
            );
        }

        console.log("Practice generator response:", data);

    } catch (error) {
        console.error("Practice generator error:", error);
        displayMessage(results, "Unable to connect to the backend.");
    } finally {
        hideLoading(button, "Generate Practice Questions");
    }
}


// ========================================
// FEATURE 6: SMART BUG PREDICTOR
// ========================================

async function predictBugs() {
    const code = getCode();
    const results = document.getElementById("bugResults");
    const button = document.getElementById("bugPredictBtn");

    if (!code) {
        displayMessage(results, "Please enter Python code first.");
        return;
    }

    showLoading(button, "Predicting bugs...");

    try {
        const { response, data } =
            await sendCodeRequest("/api/bug-predict", code);

        results.replaceChildren();

        if (!response.ok || !data.success) {
            displayMessage(
                results,
                data.message || "Bug prediction failed."
            );
            return;
        }

        const bugs = normalizeList(data.bugs);

        createElement(
            "h3",
            `Total Potential Bugs: ${data.total_bugs ?? bugs.length}`,
            results
        );

        if (bugs.length === 0) {
            createElement(
                "p",
                "No potential bugs detected!",
                results
            );
            return;
        }

        bugs.forEach((bug, index) => {
            const card = document.createElement("div");
            card.className = "result-item";

            createElement(
                "h4",
                `${index + 1}. ${bug.bug || "Potential Bug"}`,
                card
            );

            createElement(
                "p",
                `Line: ${bug.line ?? "N/A"}`,
                card
            );

            createElement(
                "p",
                `Severity: ${bug.severity ?? "Not specified"}`,
                card
            );

            createElement(
                "p",
                `Explanation: ${bug.explanation ?? "Not available"}`,
                card
            );

            createElement(
                "p",
                `Suggestion: ${bug.suggestion ?? "Not available"}`,
                card
            );

            results.appendChild(card);
        });

    } catch (error) {
        console.error("Bug prediction error:", error);
        displayMessage(
            results,
            "Error connecting to server: " + error.message
        );
    } finally {
        hideLoading(button, "Smart Bug Predictor");
    }
}
