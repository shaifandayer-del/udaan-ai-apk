from FounderApproval import (
    request_approval,
    get_approval,
    approve,
    reject
)


def print_section(title):

    print()
    print("-" * 60)
    print(title)
    print("-" * 60)


if __name__ == "__main__":

    print()
    print("=" * 60)
    print("     UDAAN AI — APPROVAL PERSISTENCE TEST")
    print("=" * 60)

    # --------------------------------------------------
    # 1. CREATE
    # --------------------------------------------------

    print_section("1️⃣ CREATE APPROVAL")

    request = request_approval(
        action="UPLOAD_VIDEO",
        platform="YouTube",
        file_path="udaan_videos/test_video.mp4",
        title="Udaan AI Test Video",
        description="Persistence test"
    )

    approval_id = request["approval_id"]

    print("🆔 ID:", approval_id)
    print("📊 Status:", request["status"])

    # --------------------------------------------------
    # 2. READ FROM DATABASE
    # --------------------------------------------------

    print_section("2️⃣ READ FROM DATABASE")

    saved = get_approval(
        approval_id
    )

    print(saved)

    # --------------------------------------------------
    # 3. VERIFY PENDING
    # --------------------------------------------------

    if saved and saved["status"] == "PENDING":

        print()
        print("✅ PENDING STATE VERIFIED")

    else:

        print()
        print("❌ PENDING STATE FAILED")

    # --------------------------------------------------
    # 4. FOUNDER APPROVES
    # --------------------------------------------------

    print_section("3️⃣ FOUNDER APPROVAL")

    approval_result = approve(
        approval_id
    )

    print(approval_result)

    # --------------------------------------------------
    # 5. READ AGAIN
    # --------------------------------------------------

    print_section("4️⃣ VERIFY DATABASE UPDATE")

    updated = get_approval(
        approval_id
    )

    print(updated)

    # --------------------------------------------------
    # 6. FINAL RESULT
    # --------------------------------------------------

    print()

    if (
        updated
        and updated["status"] == "APPROVED"
    ):

        print("🎉 APPROVAL PERSISTENCE TEST PASSED")

    else:

        print("❌ APPROVAL PERSISTENCE TEST FAILED")

    print()
    print("=" * 60)
    print("✅ STEP 99 TEST COMPLETE")
    print("=" * 60)