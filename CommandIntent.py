import re


INTENTS = {
    "research": [
        "research",
        "researched",
        "find information",
        "search information",
        "latest information",
        "study",
        "analyze topic"
    ],
    "content": [
        "write content",
        "create content",
        "write article",
        "write script",
        "write post",
        "content"
    ],
    "video": [
        "create video",
        "make video",
        "generate video",
        "video bana",
        "video banao",
        "video"
    ],
    "youtube": [
        "youtube",
        "upload youtube",
        "youtube video",
        "youtube channel"
    ],
    "social": [
        "instagram",
        "facebook",
        "social media",
        "social post",
        "social"
    ],
    "analytics": [
        "analytics",
        "analyze data",
        "statistics",
        "metrics",
        "performance"
    ],
    "marketing": [
        "marketing",
        "promotion",
        "campaign",
        "advertising",
        "growth strategy"
    ],
    "developer": [
        "code",
        "coding",
        "developer",
        "build app",
        "create app",
        "software",
        "debug",
        "program"
    ],
    "automation": [
        "automate",
        "automation",
        "workflow",
        "schedule task",
        "automatic"
    ],
    "creative": [
        "creative",
        "design",
        "logo",
        "thumbnail",
        "poster",
        "creative idea"
    ]
}


def _clean(command):
    return re.sub(
        r"\s+",
        " ",
        str(command or "").strip().lower()
    )


def detect_intent(command):
    text = _clean(command)

    if not text:
        return {
            "status": "FAILED",
            "intent": "unknown",
            "message": "Command is empty."
        }

    scores = {}

    for intent, keywords in INTENTS.items():
        score = 0

        for keyword in keywords:
            keyword = keyword.lower()

            if keyword in text:
                score += 3

        scores[intent] = score

    best_intent = max(
        scores,
        key=scores.get
    )

    if scores[best_intent] == 0:
        return {
            "status": "SUCCESS",
            "intent": "unknown",
            "command": command,
            "confidence": 0
        }

    total = sum(scores.values())

    confidence = round(
        scores[best_intent] / total,
        2
    ) if total else 0

    return {
        "status": "SUCCESS",
        "intent": best_intent,
        "command": command,
        "confidence": confidence,
        "scores": scores
    }


def get_intent(command):
    return detect_intent(command)


def classify(command):
    return detect_intent(command)


def run(command):
    return detect_intent(command)


def execute(command):
    return detect_intent(command)


def process(command):
    return detect_intent(command)


def handle(command):
    return detect_intent(command)


if __name__ == "__main__":
    command = input("UDAAN Command: ")
    print(detect_intent(command))
