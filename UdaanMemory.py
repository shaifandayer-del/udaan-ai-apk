import sqlite3

DB_NAME = "udaan_ai.db"


def save_memory(memory_type, content):

    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS memories (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            memory_type TEXT NOT NULL,
            content TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    cursor.execute(
        """
        INSERT INTO memories (memory_type, content)
        VALUES (?, ?)
        """,
        (memory_type, content)
    )

    memory_id = cursor.lastrowid

    conn.commit()
    conn.close()

    print("🧠 Memory saved:", memory_id)

    return memory_id


def get_memories():

    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("""
        SELECT id, memory_type, content, created_at
        FROM memories
        ORDER BY id DESC
    """)

    memories = cursor.fetchall()

    conn.close()

    return memories


def show_memories():

    print()
    print("================================")
    print("       UDAAN AI MEMORY")
    print("================================")

    memories = get_memories()

    if not memories:

        print("📭 Memory empty hai.")
        return

    for memory in memories:

        memory_id = memory[0]
        memory_type = memory[1]
        content = memory[2]
        created_at = memory[3]

        print()
        print("🆔 ID:", memory_id)
        print("🏷️ Type:", memory_type)
        print("📝 Content:", content)
        print("🕒 Created:", created_at)


if __name__ == "__main__":

    print("================================")
    print("       UDAAN AI")
    print("      MEMORY SYSTEM")
    print("================================")

    save_memory(
        "FOUNDER_COMMAND",
        "Udaan AI ko powerful multi-agent platform banana hai."
    )

    save_memory(
        "SYSTEM",
        "Founder approval protected actions ke liye required hai."
    )

    show_memories()