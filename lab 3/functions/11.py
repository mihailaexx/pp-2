def is_palindrome(stroka):
    if stroka == stroka[::-1]:
        return True
    else:
        return False
print(is_palindrome("шалаш"))