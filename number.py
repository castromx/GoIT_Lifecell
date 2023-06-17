import re

def number_check(nums):
    pattern = r'^(093|063|073)'
    match = re.match(pattern, nums)
    if match:
        return "Окей, продовжимо"
    else:
        return "Будь ласка, зареєструйте номер"
