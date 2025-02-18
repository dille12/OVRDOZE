import pyperclip
i = pyperclip.paste()
i = i.replace("\\", "/")
print(i)
pyperclip.copy(i)