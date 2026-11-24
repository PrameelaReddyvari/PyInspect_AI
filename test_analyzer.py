from code_checker import analyze_code

sample_code = """
import os

x = 10
y = 20

def calculate():
    unused_variable = 100
    return eval("x + y")

print(calculate())
"""

print("===== PyInspect AI ANALYSIS =====")

result = analyze_code(sample_code)

print("\nOVERALL STATUS:")
print(result["message"])

print("\nSYNTAX ANALYSIS:")
print(result["syntax"])

print("\nQUALITY ANALYSIS:")
print(result["quality"])

print("\nSECURITY ANALYSIS:")
print(result["security"])