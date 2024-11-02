import re

def is_swedish_mobile_number(phone_number: str) -> bool:
    pattern = r'^(07|7|467|\+467)\d{8}$'
    return bool(re.match(pattern, phone_number))

# 示例
print(is_swedish_mobile_number("0701234567"))  # True
print(is_swedish_mobile_number("+46701234567"))  # True
print(is_swedish_mobile_number("46712345678"))  # False
