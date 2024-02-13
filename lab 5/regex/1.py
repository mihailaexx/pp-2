import re
check_string = input()
print(re.search("ab*", check_string)) # 1
print(re.search("ab{2,3}", check_string)) # 2
print(re.findall("[a-z]+_", check_string)) # 3
print(re.findall("[A-Z][a-z]+", check_string)) # 4
print(re.search("a.*b", check_string)) # 5
print(re.sub("[ ,.]", ":", check_string)) # 6
# snake "asasf_adasd_asdasd"
# camel "asasfAdasdAsdasd", frist always lower
print(re.sub("(_)([a-z])", lambda x: x.group(2).upper(), check_string))# 7
print(re.split("(?=[A-Z])", check_string)) # 8
print(re.sub("(.)([A-Z])", r"\1 \2", check_string)) # 9
print(re.sub("([A-Z])", lambda x: "_" + x.group(1).lower(), check_string)) # 10