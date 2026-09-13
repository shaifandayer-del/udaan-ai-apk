
import os
import re
import datetime
import requests


RESEARCH_OUTPUT_FILE = "udaan_research.txt"
GEMINI_MODEL = "gemini-2.5-flash"


def _search_web(query):
    try:
        response = requests.get(
            "https://html.duckduckgo.com/html/",
            params={"q": query},
            headers={
                "User-Agent": "Mozilla/5.0"
            },
            timeout=20
        )

        if response.status_code != 200:
            return []

        html = response.text

        blocks = re.findall(
            r'class="result__a"[^>]*>(.*?)</a>',
            html,
            re.S
        )

        snippets = re.findall(
            r'class="result__snippet"[^>]*>(.*?)</a>|'
            r'class="result__snippet"[^>]*>(.*?)</div>',
            html,
            re.S
        )

        results = []

        for index, title in enumerate(blocks[:8]):
            title = re.sub("<.*?>", "", title)
            title = re.sub(r"\s+", " ", title).strip()

            snippet = ""

            if index < len(snippets):
                snippet = snippets[index][0] or snippets[index][1]
                snippet = re.sub("<.*?>", "", snippet)
                snippet = re.sub(r"\s+", " ", snippet).strip()

            if title:
                results.append(
                    {
                        "title": title,
                        "snippet": snippet
                    }
                )

        return results

    except Exception as error:
        print("WEB SEARCH ERROR:", error)
        return []


def _gemini(prompt):
    try:
        try:
            from GeminiBrain import ask_gemini

            result = ask_gemini(prompt)

            if result and not result.lower().startswith(
                (
                    "gemini api error",
                    "gemini connection error",
                    "udaan ai."
                )
            ):
                return result

        except Exception:
            pass

        api_key = (
            os.getenv("GEMINI_API_KEY")
            or os.getenv("GOOGLE_API_KEY")
            or ""
        )

        if not api_key:
            return ""

        url = (
            "https://generativelanguage.googleapis.com/v1beta/"
            "models/"
            + GEMINI_MODEL
            + ":generateContent?key="
            + api_key
        )

        payload = {
            "contents": [
                {
                    "parts": [
                        {
                            "text": prompt
                        }
                    ]
                }
            ]
        }

        response = requests.post(
            url,
            json=payload,
            headers={
                "Content-Type": "application/json"
            },
            timeout=40
        )

        if response.status_code != 200:
            print(
                "GEMINI ERROR:",
                response.status_code,
                response.text
            )
            return ""

        data = response.json()

        return (
            data["candidates"][0]
            ["content"]["parts"][0]
            ["text"]
        )

    except Exception as error:
        print("GEMINI ERROR:", error)
        return ""


def research(command):
    command = str(command or "").strip()

    if not command:
        return {
            "status": "FAILED",
            "agent": "Research AI",
            "message": "Research command is empty."
        }

    print()
    print("================================")
    print("       UDAAN RESEARCH AI")
    print("================================")
    print("Research:", command)

    web_results = _search_web(command)

    sources_text = ""

    for item in web_results:
        sources_text += (
            "\nTitle: "
            + item["title"]
            + "\n"
            + "Information: "
            + item["snippet"]
            + "\n"
        )

    if not sources_text:
        return {
            "status": "FAILED",
            "agent": "Research AI",
            "query": command,
            "message": "No web research results found."
        }

    prompt = (
        "You are UDAAN AI Research Agent.\n\n"
        "Perform useful research for the founder.\n"
        "Analyze the collected web search information.\n"
        "Do not invent facts.\n"
        "Clearly separate facts, important findings, "
        "and useful conclusions.\n\n"
        "Research Query:\n"
        + command
        + "\n\n"
        "Collected Web Information:\n"
        + sources_text
    )

    answer = _gemini(prompt)

    if not answer:
        return {
            "status": "FAILED",
            "agent": "Research AI",
            "query": command,
            "message": "Research was found but AI analysis failed."
        }

    timestamp = datetime.datetime.now().strftime(
        "%Y-%m-%d %H:%M:%S"
    )

    with open(
        RESEARCH_OUTPUT_FILE,
        "a",
        encoding="utf-8"
    ) as file:

        file.write(
            "\n================================\n"
        )

        file.write(
            "UDAAN AI RESEARCH REPORT\n"
        )

        file.write(
            "================================\n"
        )

        file.write(
            "Time: "
            + timestamp
            + "\n"
        )

        file.write(
            "Query: "
            + command
            + "\n\n"
        )

        file.write(
            answer
        )

        file.write(
            "\n\nSources:\n"
        )

        for item in web_results:
            file.write(
                "- "
                + item["title"]
                + "\n"
            )

    print()
    print("✅ REAL RESEARCH COMPLETED")
    print("📄:", RESEARCH_OUTPUT_FILE)

    return {
        "status": "SUCCESS",
        "agent": "Research AI",
        "query": command,
        "created_at": timestamp,
        "message": "Real research completed successfully.",
        "output_file": RESEARCH_OUTPUT_FILE,
        "sources_found": len(web_results),
        "result": answer
    }


def run(command):
    return research(command)


def execute(command):
    return research(command)


def process(command):
    return research(command)


def handle(command):
    return research(command)


if __name__ == "__main__":
    command = input("Research command: ")
    print(research(command))
