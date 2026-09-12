import importlib

from GeminiBrain import ask_gemini


AGENTS = {
    "Research": "Research",
    "Content": "Content",
    "Video": "Video",
    "YouTube": "YouTube",
    "Social": "Social",
    "Analytics": "Analytics",
    "Marketing": "Marketing",
    "Developer": "Developer",
    "Automation": "Automation",
    "Creative": "Creative",
}


def load_agent(agent_name):
    module_name = AGENTS.get(agent_name)

    if not module_name:
        return None, "Unknown agent."

    try:
        return importlib.import_module(module_name), None
    except Exception as error:
        return None, f"{type(error).__name__}: {error}"


def run_agent(agent_name, command=""):
    module, error = load_agent(agent_name)

    if module is None:
        return {
            "status": "FAILED",
            "agent": agent_name,
            "command": command,
            "message": "Agent module load failed.",
            "error": error
        }

    try:
        if agent_name == "Research":
            prompt = (
                "Act as UDAAN Research AI.\n"
                "Research the requested topic deeply.\n"
                "Give useful findings, key facts, trends, "
                "important points and a clear conclusion.\n\n"
                f"Research request:\n{command}"
            )

            result = ask_gemini(prompt)

        elif agent_name == "Content":
            prompt = (
                "Act as UDAAN Content AI.\n"
                "Create useful content for the founder's request.\n"
                "Include hook, main content, title, description "
                "and relevant tags when appropriate.\n\n"
                f"Content request:\n{command}"
            )

            result = ask_gemini(prompt)

        elif agent_name == "Creative":
            prompt = (
                "Act as UDAAN Creative AI.\n"
                "Create a complete creative direction for the request.\n"
                "Include visual concept, thumbnail idea, style, "
                "scene ideas and useful creative details.\n\n"
                f"Creative request:\n{command}"
            )

            result = ask_gemini(prompt)

        elif agent_name == "Developer":
            prompt = (
                "Act as UDAAN Developer AI.\n"
                "Analyze the software/app request and provide "
                "a practical implementation plan and code-level solution.\n\n"
                f"Developer request:\n{command}"
            )

            result = ask_gemini(prompt)

        elif agent_name == "Marketing":
            prompt = (
                "Act as UDAAN Marketing AI.\n"
                "Create a practical marketing strategy for the request.\n"
                "Include audience, positioning, content strategy, "
                "promotion and growth ideas.\n\n"
                f"Marketing request:\n{command}"
            )

            result = ask_gemini(prompt)

        elif agent_name == "Analytics":
            prompt = (
                "Act as UDAAN Analytics AI.\n"
                "Analyze the request and provide useful metrics, "
                "insights, possible KPIs and recommendations.\n\n"
                f"Analytics request:\n{command}"
            )

            result = ask_gemini(prompt)

        elif agent_name == "Automation":
            prompt = (
                "Act as UDAAN Automation AI.\n"
                "Design the required automation workflow step by step.\n"
                "Identify triggers, actions and expected result.\n\n"
                f"Automation request:\n{command}"
            )

            result = ask_gemini(prompt)

        elif agent_name == "YouTube":
            prompt = (
                "Act as UDAAN YouTube AI.\n"
                "Prepare the YouTube task completely.\n"
                "Include title, description, tags, upload plan "
                "and publishing requirements when relevant.\n\n"
                f"YouTube request:\n{command}"
            )

            result = ask_gemini(prompt)

        elif agent_name == "Social":
            prompt = (
                "Act as UDAAN Social Media AI.\n"
                "Prepare the requested social media content or strategy.\n"
                "Include platform-specific caption, hashtags and "
                "publishing suggestions when useful.\n\n"
                f"Social request:\n{command}"
            )

            result = ask_gemini(prompt)

        elif agent_name == "Video":
            from VideoProductionPipeline import create_video_project

            result = create_video_project(command)

        else:
            result = ask_gemini(command)

        if isinstance(result, dict):
            if result.get("status") == "FAILED":
                return result

            result.setdefault("status", "SUCCESS")
            result.setdefault("agent", f"{agent_name} AI")
            result.setdefault("command", command)

            return result

        return {
            "status": "SUCCESS",
            "agent": f"{agent_name} AI",
            "command": command,
            "message": str(result),
            "result": result
        }

    except Exception as error:
        return {
            "status": "FAILED",
            "agent": f"{agent_name} AI",
            "command": command,
            "message": "Agent execution failed.",
            "error": f"{type(error).__name__}: {error}"
        }


def execute_agent(agent_name, command=""):
    return run_agent(agent_name, command)


def run(agent_name, command=""):
    return run_agent(agent_name, command)
