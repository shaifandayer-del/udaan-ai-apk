# ==========================================
# UDAAN AI - CORE INTEGRATION TEST
# STEP 70
# ==========================================

from UdaanCore import process_command


TEST_COMMANDS = [
    "AI trends par research karo",
    "YouTube ke liye motivational content banao",
    "Instagram ke liye post idea banao",
    "60 second video banao",
    "Udaan AI ke marketing ideas do",
]


def run_core_tests():

    print()
    print("================================")
    print("      UDAAN AI CORE TEST")
    print("           STEP 70")
    print("================================")
    print()

    passed = 0
    failed = 0

    for number, command in enumerate(
        TEST_COMMANDS,
        1
    ):

        print()
        print("--------------------------------")
        print("TEST", number)
        print("COMMAND:", command)
        print("--------------------------------")
        print()

        try:

            result = process_command(command)

            if isinstance(result, dict):

                status = result.get(
                    "status",
                    "UNKNOWN"
                )

                print()
                print("STATUS:", status)

                if status in [
                    "SUCCESS",
                    "PENDING_APPROVAL"
                ]:

                    print("🟢 CORE TEST PASSED")
                    passed += 1

                else:

                    print("🔴 CORE TEST FAILED")
                    failed += 1

            else:

                print("🟢 CORE TEST PASSED")
                print("Result:", result)
                passed += 1

        except Exception as error:

            print("🔴 CORE ERROR")
            print(error)

            failed += 1

    print()
    print("================================")
    print("        CORE TEST SUMMARY")
    print("================================")
    print()

    print("📊 TOTAL :", len(TEST_COMMANDS))
    print("🟢 PASS  :", passed)
    print("🔴 FAIL  :", failed)

    print()

    if failed == 0:

        print("🎉 UDAAN CORE IS WORKING")

    else:

        print("⚠️ CORE NEEDS ATTENTION")

    print()


if __name__ == "__main__":

    run_core_tests()