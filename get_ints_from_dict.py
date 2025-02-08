data = [
    {"name": "Alice", "age": 25, "score": 90},
    {"name": "Bob", "age": 30, "score": 85},
    {"name": "Charlie", "age": 22, "score": 88},
]

# Extract all numeric values from the list of dictionaries
numeric_values = [value for item in data for value in item.values() if isinstance(value, (int, float))]

print(numeric_values)  # Output: [25, 90, 30, 85, 22, 88]
