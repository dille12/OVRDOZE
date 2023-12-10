import pyperclip
i = input("Path: ")
i = i.replace("\\", "/")
print(i)
pyperclip.copy(i)