from practice_generator import detect_concepts

sample_code = """
numbers = [10, 20, 30]

for num in numbers:
    if num > 10:
        print(num)
"""

result = detect_concepts(sample_code)

print(result)