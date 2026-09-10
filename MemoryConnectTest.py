print("================================")
print("   UDAAN MEMORY CONNECTION TEST")
print("================================")

try:

    from UdaanMemory import get_memories

    print("✅ UdaanMemory imported")

    memories = get_memories()

    print("📊 Memory count:", len(memories))

    if len(memories) == 0:

        print("📭 Memory empty hai.")

    else:

        print()
        print("🧠 SAVED MEMORIES")

        for memory in memories:

            print()
            print("🆔 ID:", memory[0])
            print("🏷️ Type:", memory[1])
            print("📝 Content:", memory[2])
            print("🕒 Created:", memory[3])

    print()
    print("✅ MEMORY CONNECTION WORKING")

except Exception as error:

    print()
    print("❌ ERROR:")
    print(error)

print()
print("================================")
print("TEST END")
print("================================")