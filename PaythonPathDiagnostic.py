import os

TARGET_FILES = {
    "UdaanStatus.py",
    "UdaanAPI.py",
    "VideoApprovalController.py",
    "VideoShareController.py"
}

print("=" * 60)
print("UDAAN AI - PROJECT FILE INVENTORY")
print("=" * 60)

roots = [
    os.getcwd(),
    "/data/data/com.septudio.pythoncoding",
    "/storage/emulated/0",
]

checked = set()
found = {}

for base in roots:

    if not os.path.exists(base):
        continue

    print("\nSEARCH ROOT:")
    print(base)

    try:

        for root, dirs, files in os.walk(base):

            # duplicate folders avoid
            real_root = os.path.realpath(root)

            if real_root in checked:
                continue

            checked.add(real_root)

            for filename in files:

                if filename in TARGET_FILES:

                    full_path = os.path.join(root, filename)

                    found[filename] = full_path

                    print("\n✅ FOUND:")
                    print(filename)
                    print(full_path)

    except Exception as e:

        print("⚠️ Access issue:")
        print(e)

print("\n" + "=" * 60)
print("FINAL RESULT")
print("=" * 60)

for filename in TARGET_FILES:

    if filename in found:
        print("\n🟢", filename)
        print(found[filename])
    else:
        print("\n🔴", filename)
        print("NOT FOUND")

print("\n" + "=" * 60)

if len(found) == 4:

    print("🟢 ALL 4 FILES FOUND")
    print()
    print("Ab mujhe FOUND paths ka screenshot bhejo.")

elif len(found) > 0:

    print("🟡 Kuch files mili hain.")
    print("Jo paths aaye hain unka screenshot bhejo.")

else:

    print("🔴 Ek bhi target file accessible nahi mili.")
    print("Is case me Python Coding app ke")
    print("file/project folder ko check karna padega.")