
from execution_tracker import analyze_execution

code = """
x = 10
y = 20

total = x + y

for i in range(3):
    total += i

print(total)
"""

result = analyze_execution(code)

print("\nEXECUTION RESULT")
print("----------------")

print("Success:", result["success"])
print("Output:", result["output"])
print("Error:", result["error"])

print("\nEXECUTION STEPS")

for step in result["steps"]:
    print("Line:", step["line"])
    print("Variables:", step["variables"])
    print("----------------")
