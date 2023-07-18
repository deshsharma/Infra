import sys

while True:
    name = sys.stdin.readline().strip()
    if name == "exit":
        break
    print("Hello, {}!".format(name))