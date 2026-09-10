import sys
import importlib.util

print("===== UDAAN AI ENVIRONMENT CHECK =====")
print()
print("Python version:")
print(sys.version)
print()

modules = [
    "kivy",
    "tkinter",
    "pygame",
    "flask",
    "requests"
]

print("Available modules:")
print()

for module in modules:
    if importlib.util.find_spec(module):
        print("✅", module, "AVAILABLE")
    else:
        print("❌", module, "NOT AVAILABLE")

print()
print("===== CHECK COMPLETE =====")