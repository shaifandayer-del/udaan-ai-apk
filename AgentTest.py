# ==========================================
# UDAAN AI - AGENT INTEGRATION TEST
# STEP 69
# ==========================================

from AgentConnector import run_agent


TESTS = [
    (
        "Research AI",
        "AI trends par research karo"
    ),
    (
        "Content AI",
        "Motivational YouTube script banao"
    ),
    (
        "Video AI",
        "60 second YouTube video banao"
    ),
    (
        "YouTube AI",
        "YouTube video idea prepare karo"
    ),
    (
        "Social AI",
        "Instagram post idea prepare karo"
    ),
    (
        "Analytics AI",
        "Channel performance analyze karo"
    ),
    (
        "Marketing AI",
        "Udaan AI marketing campaign prepare karo"
    ),
    (
        "Developer AI",
        "Python app structure prepare karo"
    ),
    (
        "Automation AI",
        "Daily content automation prepare karo"
    ),
    (
        "Creative AI",
        "YouTube thumbnail idea prepare karo"
    ),
]


def run_tests():

    print()
    print("================================")
    print("     UDAAN AI AGENT TEST")
    print("           STEP 69")
    print("================================")
    print()

    total = len(TESTS)
    passed = 0
    failed = 0

    for number, (agent, command) in enumerate(TESTS, 1):

        print()
        print("--------------------------------")
        print("TEST", number, "/", total)
        print("AGENT:", agent)
        print("--------------------------------")
        print()

        try:

            result = run_agent(
                agent,
                command
            )

            if isinstance(result, dict):

                status = result.get(
                    "status",
                    ""
                )

                if status == "SUCCESS":

                    print("🟢 PASS")
                    passed += 1

                else:

                    print("🔴 FAIL")
                    print("Result:", result)
                    failed += 1

            else:

                print("🟢 PASS")
                print("Result:", result)
                passed += 1

        except Exception as error:

            print("🔴 FAIL")
            print("Error:", error)
            failed += 1

    print()
    print("================================")
    print("       TEST SUMMARY")
    print("================================")
    print()

    print("📊 TOTAL :", total)
    print("🟢 PASS  :", passed)
    print("🔴 FAIL  :", failed)

    print()

    if failed == 0:

        print("🎉 ALL AGENT TESTS PASSED")

    else:

        print("⚠️ SOME AGENTS NEED FIXING")

    print()


if __name__ == "__main__":

    run_tests()