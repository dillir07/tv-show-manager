import re

pattern = '(s|season)[0-9].'
test_string = 'friends.s02e08'
result = re.search(pattern, test_string)

if result:
    print(result.group())
else:
    print("Search unsuccessful.")
