AGENT_CAPABILITIES = {

    "Research AI": [
        "research",
        "trends",
        "information",
        "facts",
        "competitor research",
        "market research"
    ],

    "Content AI": [
        "script",
        "content",
        "caption",
        "post",
        "article",
        "copywriting"
    ],

    "Video AI": [
        "video",
        "reel",
        "short",
        "video generation",
        "video editing"
    ],

    "YouTube AI": [
        "youtube",
        "youtube video",
        "youtube channel",
        "youtube upload",
        "youtube seo"
    ],

    "Social AI": [
        "instagram",
        "social media",
        "facebook",
        "social post",
        "social upload"
    ],

    "Analytics AI": [
        "analytics",
        "analysis",
        "performance",
        "metrics",
        "report"
    ],

    "Marketing AI": [
        "marketing",
        "advertisement",
        "ads",
        "campaign",
        "promotion"
    ],

    "Developer AI": [
        "app",
        "software",
        "website",
        "code",
        "coding",
        "developer",
        "bug",
        "testing"
    ],

    "Automation AI": [
        "automation",
        "automate",
        "workflow",
        "schedule",
        "automatic"
    ],

    "Creative AI": [
        "creative",
        "idea",
        "thumbnail",
        "design",
        "concept",
        "brainstorm"
    ]
}


def get_capabilities(agent_name):

    return AGENT_CAPABILITIES.get(
        agent_name,
        []
    )


def find_agents_for_capability(keyword):

    keyword = keyword.lower()

    matches = []

    for agent, capabilities in AGENT_CAPABILITIES.items():

        for capability in capabilities:

            if keyword in capability.lower():

                matches.append(agent)
                break

    return matches


def show_capabilities():

    print()
    print("================================")
    print("     UDAAN AI CAPABILITIES")
    print("================================")
    print()

    for agent, capabilities in AGENT_CAPABILITIES.items():

        print("🤖", agent)

        for capability in capabilities:

            print("   •", capability)

        print()

    print("================================")
    print()


if __name__ == "__main__":

    show_capabilities()