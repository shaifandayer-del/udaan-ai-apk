from AgentConnector import execute_agent


def execute_command(command, agent=None):
    command = str(command or "").strip()

    if not command:
        return {
            "status": "FAILED",
            "message": "Command is empty."
        }

    selected_agent = agent

    if not selected_agent:
        text = command.lower()

        if any(word in text for word in [
            "research",
            "search",
            "research karo"
        ]):
            selected_agent = "Research"

        elif any(word in text for word in [
            "video",
            "movie",
            "reel"
        ]):
            selected_agent = "Video"

        elif any(word in text for word in [
            "content",
            "script",
            "article",
            "blog"
        ]):
            selected_agent = "Content"

        elif any(word in text for word in [
            "youtube"
        ]):
            selected_agent = "YouTube"

        elif any(word in text for word in [
            "instagram",
            "social",
            "post"
        ]):
            selected_agent = "Social"

        elif any(word in text for word in [
            "creative",
            "design",
            "idea"
        ]):
            selected_agent = "Creative"

        elif any(word in text for word in [
            "analytics",
            "analysis",
            "data"
        ]):
            selected_agent = "Analytics"

        elif any(word in text for word in [
            "marketing",
            "marketing plan"
        ]):
            selected_agent = "Marketing"

        elif any(word in text for word in [
            "developer",
            "code",
            "app",
            "software"
        ]):
            selected_agent = "Developer"

        elif any(word in text for word in [
            "automation",
            "automate"
        ]):
            selected_agent = "Automation"

        else:
            selected_agent = "Content"

    result = execute_agent(
        selected_agent,
        command
    )

    if not isinstance(result, dict):
        result = {
            "status": "SUCCESS",
            "agent": selected_agent,
            "result": result
        }

    result.setdefault(
        "agent",
        selected_agent
    )

    result.setdefault(
        "command",
        command
    )

    return result


def run(command, agent=None):
    return execute_command(
        command,
        agent
    )


if __name__ == "__main__":
    print(
        execute_command(
            "UDAAN AI test command"
        )
    )
