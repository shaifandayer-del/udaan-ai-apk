# SmartAgentMatcher.py

AGENT_KEYWORDS = {

    "Research": [
        "research",
        "researcher",
        "trend",
        "trends",
        "news",
        "information",
        "find",
        "search",
        "study"
    ],

    "Content": [
        "content",
        "script",
        "caption",
        "article",
        "post",
        "write"
    ],

    "Video": [
        "video",
        "reel",
        "short",
        "movie",
        "edit",
        "create video"
    ],

    "YouTube": [
        "youtube",
        "channel",
        "thumbnail",
        "upload youtube",
        "youtube video"
    ],

    "Social": [
        "instagram",
        "facebook",
        "social",
        "twitter",
        "x post",
        "social media"
    ],

    "Analytics": [
        "analytics",
        "statistics",
        "stats",
        "performance",
        "report",
        "data"
    ],

    "Marketing": [
        "marketing",
        "campaign",
        "promotion",
        "advertising",
        "ads",
        "brand"
    ],

    "Developer": [
        "code",
        "coding",
        "developer",
        "software",
        "app",
        "website",
        "program",
        "debug",
        "build"
    ],

    "Automation": [
        "automation",
        "automate",
        "schedule",
        "workflow",
        "automatic"
    ],

    "Creative": [
        "creative",
        "idea",
        "design",
        "creative idea",
        "concept"
    ]
}


def normalize_command(command):

    if not command:
        return ""

    return str(command).strip().lower()


def match_agent(command):

    text = normalize_command(command)

    if not text:
        return None

    scores = {}

    for agent, keywords in AGENT_KEYWORDS.items():

        score = 0

        for keyword in keywords:

            if keyword.lower() in text:
                score += 1

        scores[agent] = score

    best_agent = None
    best_score = 0

    for agent, score in scores.items():

        if score > best_score:

            best_agent = agent
            best_score = score

    return best_agent


def find_agent(command):

    return match_agent(command)


def smart_match(command):

    return match_agent(command)


def select_agent(command):

    return match_agent(command)


def get_selected_agent(command):

    return match_agent(command)


def get_agent_scores(command):

    text = normalize_command(command)

    scores = {}

    for agent, keywords in AGENT_KEYWORDS.items():

        score = 0

        for keyword in keywords:

            if keyword.lower() in text:
                score += 1

        scores[agent] = score

    return scores


def explain_match(command):

    agent = match_agent(command)
    scores = get_agent_scores(command)

    return {
        "command": command,
        "agent": agent,
        "scores": scores
    }


if __name__ == "__main__":

    print()
    print("=" * 60)
    print("       UDAAN AI — SMART AGENT MATCHER")
    print("=" * 60)

    test_commands = [

        "research latest AI trends",

        "create a YouTube video",

        "make an Instagram post",

        "build a mobile app",

        "check analytics",

        "automate my workflow",

        "give me creative ideas"
    ]

    for command in test_commands:

        agent = match_agent(command)

        print()
        print("🗣️ Command :", command)
        print("🤖 Agent   :", agent)

    print()
    print("=" * 60)
    print("✅ SMART AGENT MATCHER READY")
    print("=" * 60)