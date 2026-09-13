def select_agent(command):
    command = str(command or "").strip().lower()

    if any(x in command for x in ["research", "search", "research karo"]):
        return "Research"

    if any(x in command for x in ["video", "movie", "reel"]):
        return "Video"

    if any(x in command for x in ["content", "script", "article", "blog"]):
        return "Content"

    if "youtube" in command:
        return "YouTube"

    if any(x in command for x in ["instagram", "social", "post"]):
        return "Social"

    if any(x in command for x in ["creative", "design", "idea"]):
        return "Creative"

    if any(x in command for x in ["analytics", "analysis", "data"]):
        return "Analytics"

    if "marketing" in command:
        return "Marketing"

    if any(x in command for x in ["developer", "code", "app", "software"]):
        return "Developer"

    if any(x in command for x in ["automation", "automate"]):
        return "Automation"

    return "Content"


def route_command(command):
    return select_agent(command)


def get_route(command):
    return select_agent(command)


def route(command):
    return select_agent(command)
