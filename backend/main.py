from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import ast
import re

from database import (
    create_table,
    save_analysis,
    get_history,
    delete_history
)


app = FastAPI(title="CodeMate API")


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


create_table()


class CodeRequest(BaseModel):
    language: str
    code: str


# ---------------------------------------------------
# CODE EXPLANATION FUNCTION
# ---------------------------------------------------

def explain_python_code(code):

    explanations = []
    overall = []

    try:
        tree = ast.parse(code)

        for node in ast.walk(tree):

            # Function
            if isinstance(
                node,
                (ast.FunctionDef, ast.AsyncFunctionDef)
            ):

                explanations.append(
                    f"Line {node.lineno}: "
                    f"Creates a function named '{node.name}'."
                )

                overall.append(
                    f"The program defines a function called '{node.name}'."
                )

            # For loop
            elif isinstance(node, ast.For):

                explanations.append(
                    f"Line {node.lineno}: "
                    f"Creates a for loop that repeats through a sequence."
                )

                overall.append(
                    "The program contains a for loop."
                )

            # While loop
            elif isinstance(node, ast.While):

                explanations.append(
                    f"Line {node.lineno}: "
                    f"Creates a while loop that continues while a condition is true."
                )

                overall.append(
                    "The program contains a while loop."
                )

            # If condition
            elif isinstance(node, ast.If):

                explanations.append(
                    f"Line {node.lineno}: "
                    f"Checks a condition using an if statement."
                )

                overall.append(
                    "The program uses a condition to make a decision."
                )

            # Variable assignment
            elif isinstance(node, ast.Assign):

                for target in node.targets:

                    if isinstance(target, ast.Name):

                        explanations.append(
                            f"Line {node.lineno}: "
                            f"Creates or changes the variable '{target.id}'."
                        )

                        overall.append(
                            f"The program uses a variable called '{target.id}'."
                        )

            # Print statement
            elif isinstance(node, ast.Call):

                if (
                    isinstance(node.func, ast.Name)
                    and node.func.id == "print"
                ):

                    explanations.append(
                        f"Line {node.lineno}: "
                        f"Uses print() to display information on the screen."
                    )

                    overall.append(
                        "The program displays information using print()."
                    )

            # Return
            elif isinstance(node, ast.Return):

                explanations.append(
                    f"Line {node.lineno}: "
                    f"Returns a value from a function."
                )

                overall.append(
                    "A function returns a value."
                )

        if not explanations:

            explanations.append(
                "The code was successfully analyzed, "
                "but no common Python structures were detected."
            )

        overall_text = " ".join(dict.fromkeys(overall))

        if not overall_text:

            overall_text = (
                "This Python program contains basic Python statements."
            )

        return explanations, overall_text

    except SyntaxError:
        return [], "The code contains a syntax error, so a complete explanation cannot be generated."


# ---------------------------------------------------
# BASIC EXPLANATION FOR OTHER LANGUAGES
# ---------------------------------------------------

def explain_other_code(language, code):

    explanations = []
    overall = []

    lines = code.splitlines()

    for number, line in enumerate(lines, start=1):

        text = line.strip()

        if not text:
            continue

        # Function
        if re.search(
            r"\b(function|def|void|int|float|double|string|String)\s+\w+\s*\(",
            text
        ):

            explanations.append(
                f"Line {number}: This line appears to define or declare a function."
            )

        # Loop
        elif re.search(
            r"\b(for|while)\b",
            text
        ):

            explanations.append(
                f"Line {number}: This line contains a loop."
            )

        # If
        elif re.search(
            r"\b(if|else|elif)\b",
            text
        ):

            explanations.append(
                f"Line {number}: This line checks a condition."
            )

        # Variable
        elif re.search(
            r"\b(let|const|var|int|float|double|String|string)\b",
            text
        ):

            explanations.append(
                f"Line {number}: This line declares or uses a variable."
            )

        # Print
        elif re.search(
            r"\b(print|console\.log|System\.out\.println)\b",
            text
        ):

            explanations.append(
                f"Line {number}: This line displays output."
            )

    if not explanations:

        explanations.append(
            "Basic code analysis completed. "
            "No common code structures were detected."
        )

    overall.append(
        f"This {language} program was analyzed using basic code rules."
    )

    return explanations, " ".join(overall)


# ---------------------------------------------------
# ANALYZE CODE
# ---------------------------------------------------

@app.post("/analyze")
def analyze_code(request: CodeRequest):

    language = request.language.lower()
    code = request.code

    if not code.strip():

        return {
            "success": False,
            "message": "Please enter some code."
        }

    # Count non-empty lines
    lines = len([
        line
        for line in code.splitlines()
        if line.strip()
    ])

    functions = 0
    loops = 0
    variables = 0
    errors = []

    # ------------------------------------------------
    # PYTHON ANALYSIS
    # ------------------------------------------------

    if language == "python":

        try:

            tree = ast.parse(code)

            for node in ast.walk(tree):

                if isinstance(
                    node,
                    (ast.FunctionDef, ast.AsyncFunctionDef)
                ):
                    functions += 1

                if isinstance(
                    node,
                    (ast.For, ast.While)
                ):
                    loops += 1

                if isinstance(node, ast.Assign):
                    variables += len(node.targets)

            syntax_status = "✅ No syntax errors detected."

            explanation, overall_explanation = \
                explain_python_code(code)

        except SyntaxError as error:

            errors.append(
                f"Line {error.lineno}: {error.msg}"
            )

            syntax_status = "❌ Syntax error detected."

            explanation = [
                f"Python could not understand the code because "
                f"there is a syntax error on line {error.lineno}."
            ]

            overall_explanation = (
                "Fix the syntax error first, then CodeMate "
                "can provide a complete explanation."
            )

    # ------------------------------------------------
    # OTHER LANGUAGES
    # ------------------------------------------------

    else:

        functions = len(
            re.findall(
                r"\b(function|def|void|int|float|string|String)\s+\w+\s*\(",
                code
            )
        )

        loops = len(
            re.findall(
                r"\b(for|while)\b",
                code
            )
        )

        variables = len(
            re.findall(
                r"\b(let|const|var|int|float|double|string|String)\b",
                code
            )
        )

        syntax_status = "ℹ️ Basic analysis completed."

        explanation, overall_explanation = \
            explain_other_code(language, code)

    # ------------------------------------------------
    # SAVE TO DATABASE
    # ------------------------------------------------

    save_analysis(
        language,
        code,
        lines,
        functions,
        loops,
        variables
    )

    # ------------------------------------------------
    # SEND RESULT TO FRONTEND
    # ------------------------------------------------

    return {
        "success": True,
        "language": language,
        "lines": lines,
        "functions": functions,
        "loops": loops,
        "variables": variables,
        "syntax_status": syntax_status,
        "errors": errors,
        "explanation": explanation,
        "overall_explanation": overall_explanation
    }


# ---------------------------------------------------
# HISTORY
# ---------------------------------------------------

@app.get("/history")
def history():

    return {
        "success": True,
        "history": get_history()
    }


# ---------------------------------------------------
# DELETE HISTORY
# ---------------------------------------------------

@app.delete("/history/{history_id}")
def delete(history_id: int):

    delete_history(history_id)

    return {
        "success": True,
        "message": "History deleted."
    }