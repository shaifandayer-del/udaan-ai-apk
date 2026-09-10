import json
import os


BLUEPRINT_FILE = "udaan_ui_blueprint.json"
DESIGN_FILE = "udaan_design_system.json"


def load_json(filename):

    if not os.path.exists(filename):
        print("🔴 Missing:", filename)
        return None

    try:
        with open(filename, "r", encoding="utf-8") as file:
            return json.load(file)

    except Exception as error:
        print("🔴 Read error:", filename)
        print("   ", error)
        return None


def validate():

    print()
    print("=" * 60)
    print("          UDAAN AI — UI SYSTEM VALIDATOR")
    print("=" * 60)

    blueprint = load_json(BLUEPRINT_FILE)
    design = load_json(DESIGN_FILE)

    print()

    if blueprint:
        print("🟢 UI Blueprint       : ONLINE")
    else:
        print("🔴 UI Blueprint       : MISSING")

    if design:
        print("🟢 Design System      : ONLINE")
    else:
        print("🔴 Design System      : MISSING")

    print()

    if not blueprint or not design:
        print("⚠️ UI validation incomplete.")
        return

    blueprint_agents = blueprint.get("agents", [])
    blueprint_navigation = blueprint.get("navigation", [])
    design_screens = design.get("screens", {})
    design_effects = design.get("effects", [])

    print("🤖 Agents defined     :", len(blueprint_agents))
    print("📱 Navigation items   :", len(blueprint_navigation))
    print("🎨 Design screens     :", len(design_screens))
    print("✨ Visual effects     :", len(design_effects))

    print()

    required_agents = [
        "Research AI",
        "Content AI",
        "Video AI",
        "YouTube AI",
        "Social AI",
        "Analytics AI",
        "Marketing AI",
        "Developer AI",
        "Automation AI",
        "Creative AI"
    ]

    missing_agents = [
        agent
        for agent in required_agents
        if agent not in blueprint_agents
    ]

    if not missing_agents:
        print("🟢 Agent Design Coverage: COMPLETE")
    else:
        print("🟡 Missing agents:", missing_agents)

    required_navigation = [
        "Home",
        "Command Center",
        "AI Agents",
        "Tasks",
        "Content",
        "Video Studio",
        "Social Media",
        "YouTube",
        "Analytics",
        "Developer AI",
        "Automation",
        "Settings"
    ]

    missing_navigation = [
        screen
        for screen in required_navigation
        if screen not in blueprint_navigation
    ]

    if not missing_navigation:
        print("🟢 Navigation Coverage  : COMPLETE")
    else:
        print("🟡 Missing screens:", missing_navigation)

    print()

    if (
        not missing_agents
        and not missing_navigation
        and blueprint.get("theme", {}).get("style") == "futuristic"
        and design.get("ai_core", {}).get("shape") == "orb"
    ):
        print("🚀 UDAAN UI SYSTEM: READY")
        print("🔵 3D AI CORE: DEFINED")
        print("📱 MOBILE FRONTEND: SPECIFIED")
    else:
        print("⚠️ UDAAN UI SYSTEM: NEEDS ATTENTION")

    print()
    print("=" * 60)


if __name__ == "__main__":
    validate()