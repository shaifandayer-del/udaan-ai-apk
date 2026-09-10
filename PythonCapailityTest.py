# PythonCapabilityTest.py

import importlib


def check(name, module_name, function_names):
    try:
        module = importlib.import_module(module_name)

        for fn in function_names:
            if callable(getattr(module, fn, None)):
                print(f"🟢 {name:<30} PASS")
                return True

        print(f"🔴 {name:<30} FAIL")
        return False

    except Exception as e:
        print(f"🔴 {name:<30} FAIL")
        print("   →", e)
        return False


def main():

    print()
    print("=" * 60)
    print("     UDAAN AI — CAPABILITY TEST")
    print("=" * 60)

    tests = []

    tests.append(check(
        "Main AI Core",
        "UdaanCore",
        ["process_command"]
    ))

    tests.append(check(
        "Research AI",
        "Research",
        ["run", "execute", "process", "handle", "main"]
    ))

    tests.append(check(
        "Content AI",
        "Content",
        ["run", "execute", "process", "handle", "main"]
    ))

    tests.append(check(
        "Video AI",
        "Video",
        ["run", "execute", "process", "handle", "main"]
    ))

    tests.append(check(
        "YouTube AI",
        "YouTube",
        ["run", "execute", "process", "handle", "main"]
    ))

    tests.append(check(
        "Social AI",
        "Social",
        ["run", "execute", "process", "handle", "main"]
    ))

    tests.append(check(
        "Analytics AI",
        "Analytics",
        ["run", "execute", "process", "handle", "main"]
    ))

    tests.append(check(
        "Marketing AI",
        "Marketing",
        ["run", "execute", "process", "handle", "main"]
    ))

    tests.append(check(
        "Developer AI",
        "Developer",
        ["run", "execute", "process", "handle", "main"]
    ))

    tests.append(check(
        "Automation AI",
        "Automation",
        ["run", "execute", "process", "handle", "main"]
    ))

    tests.append(check(
        "Creative AI",
        "Creative",
        ["run", "execute", "process", "handle", "main"]
    ))

    tests.append(check(
        "Founder Approval",
        "FounderApproval",
        ["request_approval", "approve", "reject"]
    ))

    tests.append(check(
        "Memory",
        "UdaanMemory",
        ["save_memory"]
    ))

    tests.append(check(
        "Video Approval",
        "VideoApprovalController",
        ["create_video_preview", "approve_video"]
    ))

    tests.append(check(
        "Video Share",
        "VideoShareController",
        ["prepare_video_share"]
    ))

    tests.append(check(
        "Gemini",
        "GeminiBrain",
        ["ask_gemini"]
    ))

    passed = sum(tests)
    total = len(tests)

    score = int((passed / total) * 100)

    print()
    print("=" * 60)
    print(f"CAPABILITY RESULT: {passed}/{total}")
    print(f"SCORE: {score}%")
    print("=" * 60)

    if score == 100:
        print("🚀 ALL CAPABILITY INTERFACES PASSED")
    else:
        print("⚠️ SOME CAPABILITIES NEED ATTENTION")

    print("=" * 60)


if __name__ == "__main__":
    main()