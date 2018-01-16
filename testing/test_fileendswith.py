import os

contents = os.listdir()
print(contents)

py_files = []
for file in contents:
    if file.endswith('.py'):
        py_files.append(file)

print(py_files)
print(len(py_files))
