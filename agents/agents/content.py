from Content import generate_content


def create_content():
    return {
        "name": "Content AI",
        "status": "ONLINE",
        "execute": generate_content
    }
