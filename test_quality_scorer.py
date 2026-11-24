
from quality_scorer import calculate_quality_score

sample_code = """
def calculate_total(numbers):
    total = 0
    for number in numbers:
        total += number
    return total
"""

result = calculate_quality_score(sample_code)

print("\nPYINSPECT AI - CODE QUALITY REPORT")
print("----------------------------------")

if result["success"]:
    print("Score:", result["score"], "/ 100")
    print("Rating:", result["rating"])

    print("\nCategory Scores:")
    for category, points in result["breakdown"].items():
        print(category, ":", points, "/ 20")

    print("\nSuggestions:")

    if result["suggestions"]:
        for suggestion in result["suggestions"]:
            print("-", suggestion)
    else:
        print("No suggestions. Good work!")

else:
    print(result["message"])
