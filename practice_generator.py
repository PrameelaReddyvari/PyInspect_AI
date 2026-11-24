
import ast


# ========================================
# FEATURE 1: DETECT PYTHON CONCEPTS
# ========================================

def detect_concepts(source_code):

    try:
        tree = ast.parse(source_code)

    except SyntaxError as error:
        return {
            "success": False,
            "message": f"Syntax error on line {error.lineno}: {error.msg}"
        }

    concepts = set()

    for node in ast.walk(tree):

        # Detect loops
        if isinstance(node, (ast.For, ast.AsyncFor)):
            concepts.add("For Loop")

        if isinstance(node, ast.While):
            concepts.add("While Loop")

        # Detect functions
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            concepts.add("Functions")

        # Detect lists
        if isinstance(node, (ast.List, ast.ListComp)):
            concepts.add("Lists")

        # Detect tuples
        if isinstance(node, ast.Tuple):
            concepts.add("Tuples")

        # Detect dictionaries
        if isinstance(node, ast.Dict):
            concepts.add("Dictionaries")

        # Detect conditional statements
        if isinstance(node, ast.If):
            concepts.add("If-Else")

        # Detect classes
        if isinstance(node, ast.ClassDef):
            concepts.add("Classes")

        # Detect exception handling
        if isinstance(node, ast.Try):
            concepts.add("Exception Handling")

        # Detect sets
        if isinstance(node, ast.Set):
            concepts.add("Sets")

    return {
        "success": True,
        "concepts": sorted(concepts)
    }


# ========================================
# FEATURE 2: QUESTION DATABASE
# ========================================

QUESTION_BANK = {

    "For Loop": [
        "Write a Python program to print numbers from 1 to 10 using a for loop.",
        "Write a program to calculate the sum of all numbers in a list using a for loop.",
        "Write a program to count how many even numbers are present in a list.",
        "Write a program to print the multiplication table of a given number.",
        "Write a program to find the largest number in a list using a for loop."
    ],

    "While Loop": [
        "Write a program to print numbers from 1 to 20 using a while loop.",
        "Write a program to calculate the sum of digits of a number using a while loop.",
        "Write a program to reverse a number using a while loop.",
        "Write a program to count the digits in a given number.",
        "Write a program to check whether a number is a palindrome."
    ],

    "Functions": [
        "Create a function that accepts two numbers and returns their sum.",
        "Write a function to check whether a number is even or odd.",
        "Create a function to find the factorial of a number.",
        "Write a function that returns the largest element in a list.",
        "Create a function to check whether a given string is a palindrome."
    ],

    "Lists": [
        "Write a program to find the second largest element in a list.",
        "Write a program to remove duplicate elements from a list.",
        "Write a program to find the sum of all elements in a list.",
        "Write a program to separate even and odd numbers into two lists.",
        "Write a program to reverse a list without using the reverse method."
    ],

    "Tuples": [
        "Create a tuple and find its maximum and minimum elements.",
        "Write a program to count how many times an element occurs in a tuple.",
        "Convert a tuple into a list and add a new element.",
        "Write a program to find the index of a given element in a tuple."
    ],

    "Dictionaries": [
        "Create a dictionary containing student names and marks.",
        "Write a program to find the key with the highest value in a dictionary.",
        "Write a program to count the frequency of each character in a string.",
        "Write a program to merge two dictionaries."
    ],

    "If-Else": [
        "Write a program to check whether a number is positive, negative, or zero.",
        "Write a program to find the largest among three numbers.",
        "Write a program to check whether a year is a leap year.",
        "Write a program to calculate a student's grade based on marks."
    ],

    "Classes": [
        "Create a Student class with name and marks attributes.",
        "Create a BankAccount class with deposit and withdrawal methods.",
        "Create a Rectangle class that calculates area and perimeter."
    ],

    "Exception Handling": [
        "Write a program that handles division by zero using try-except.",
        "Write a program that handles invalid integer input.",
        "Write a program that uses finally to display a completion message."
    ],

    "Sets": [
        "Write a program to find common elements between two sets.",
        "Write a program to remove duplicate values from a list using a set.",
        "Write a program to find the union and intersection of two sets."
    ]
}


# ========================================
# FEATURE 3: GENERATE PRACTICE QUESTIONS
# ========================================

def generate_practice_questions(concepts):

    questions = []

    if not concepts:
        return {
            "success": True,
            "questions": [
                "Write a Python program to check whether a number is prime.",
                "Write a program to reverse a string.",
                "Write a program to find the factorial of a number."
            ]
        }

    for concept in concepts:

        concept_questions = QUESTION_BANK.get(concept, [])

        for question in concept_questions[:3]:
            questions.append(question)

    # Remove duplicate questions while preserving order
    questions = list(dict.fromkeys(questions))

    # Fallback if no questions match the detected concepts
    if not questions:
        questions = [
            "Write a Python program to check whether a number is prime.",
            "Write a program to find the largest of three numbers.",
            "Write a program to reverse a string."
        ]

    return {
        "success": True,
        "questions": questions
    }
