print("=" * 55)
print("        UDAAN AI — UI ENVIRONMENT TEST")
print("=" * 55)

print()

# Python
import sys

print("🐍 Python:", sys.version.split()[0])

print()

# Kivy
try:
    import kivy

    print("🟢 Kivy: INSTALLED")
    print("   Version:", kivy.__version__)

except Exception as error:

    print("🔴 Kivy: NOT AVAILABLE")
    print("   Reason:", error)

print()

# Tkinter
try:
    import tkinter

    print("🟢 Tkinter: AVAILABLE")

except Exception:

    print("🔴 Tkinter: NOT AVAILABLE")

print()

# Pygame
try:
    import pygame

    print("🟢 Pygame: AVAILABLE")
    print("   Version:", pygame.version.ver)

except Exception:

    print("🔴 Pygame: NOT AVAILABLE")

print()

print("=" * 55)
print("             TEST COMPLETE")
print("=" * 55)