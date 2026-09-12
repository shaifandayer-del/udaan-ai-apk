package com.udaan.ai

import org.json.JSONArray

object UdaanAgentManager {

    fun parseAgents(json: String): List<UdaanAgent> {
        val agents = mutableListOf<UdaanAgent>()

        try {
            val array = JSONArray(json)

            for (i in 0 until array.length()) {
                val item = array.optJSONObject(i) ?: continue

                agents.add(
                    UdaanAgent(
                        name = item.optString("name"),
                        description = item.optString("description"),
                        status = item.optString(
                            "status",
                            "UNKNOWN"
                        )
                    )
                )
            }
        } catch (_: Exception) {
        }

        return agents
    }

    fun findAgent(
        agents: List<UdaanAgent>,
        name: String
    ): UdaanAgent? {
        return agents.firstOrNull {
            it.name.equals(
                name,
                ignoreCase = true
            )
        }
    }

    fun activeAgents(
        agents: List<UdaanAgent>
    ): List<UdaanAgent> {
        return agents.filter {
            it.status.equals(
                "ACTIVE",
                ignoreCase = true
            ) ||
            it.status.equals(
                "READY",
                ignoreCase = true
            ) ||
            it.status.equals(
                "ONLINE",
                ignoreCase = true
            )
        }
    }
}
