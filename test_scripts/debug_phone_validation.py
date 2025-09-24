#!/usr/bin/env python3
"""
Debug phone validation
"""

import re

def validate_phone(phone: str) -> bool:
    if not phone:
        return True
    cleaned = re.sub(r'[^\d+]', '', phone)
    print(f"Phone: '{phone}' -> Cleaned: '{cleaned}' -> Length: {len(cleaned)}")
    return len(cleaned) >= 10

# Test with sample phones
test_phones = [
    "+1-555-0100",
    "555.0200",
    "(555) 0300",
    "555-0400"
]

for phone in test_phones:
    result = validate_phone(phone)
    print(f"'{phone}' -> Valid: {result}")
    print()
