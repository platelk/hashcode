"""
This is where the magic happen
"""

import parsing


def resolve(content: str) -> str:
    input_data = parsing.parse(content)
    print(input_data)
    return "nothing"
