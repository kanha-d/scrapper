string = "6–10 years"

digits = '-'.join(filter(str.isdigit, string))
print(digits.split("-"))
