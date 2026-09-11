package com.udaan.ai

import android.app.Activity
import android.graphics.Color
import android.os.Bundle
import android.view.Gravity
import android.view.ViewGroup
import android.widget.Button
import android.widget.EditText
import android.widget.ImageView
import android.widget.LinearLayout
import android.widget.ScrollView
import android.widget.TextView
import android.widget.Toast
import okhttp3.MediaType.Companion.toMediaType
import okhttp3.OkHttpClient
import okhttp3.Request
import okhttp3.RequestBody.Companion.toRequestBody
import org.json.JSONArray
import org.json.JSONObject
import java.util.concurrent.TimeUnit

class MainActivity : Activity() {

    private val client = OkHttpClient.Builder()
        .connectTimeout(15, TimeUnit.SECONDS)
        .readTimeout(60, TimeUnit.SECONDS)
        .build()

    private val backendUrl =
        "https://udaan-ai-apk-1.onrender.com"

    private val founderApiKey =
        BuildConfig.UDAAN_FOUNDER_API_KEY

    private lateinit var statusText: TextView
    private lateinit var commandInput: EditText

    private val agents = listOf(
        data class UdaanAgent(
    val name: String,
    val module: String,
    val description: String,
    val status: String,
    val functions: List<String>
)

private var dynamicAgents = mutableListOf<UdaanAgent>()
    )

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        showCommandCenter()
    }

    private fun createRoot(
        title: String
    ): Pair<LinearLayout, LinearLayout> {

        val root = LinearLayout(this).apply {
            orientation = LinearLayout.VERTICAL
            setBackgroundColor(Color.rgb(7, 9, 16))
        }

        val header = LinearLayout(this).apply {
            orientation = LinearLayout.VERTICAL
            gravity = Gravity.CENTER
            setPadding(20, 25, 20, 15)
        }

        val logo = ImageView(this).apply {
            setImageResource(R.drawable.udaan_logo)
        }

        header.addView(
            logo,
            LinearLayout.LayoutParams(90, 90)
        )

        val titleView = TextView(this).apply {
            text = "UDAAN AI\n$title"
            textSize = 24f
            setTextColor(Color.WHITE)
            gravity = Gravity.CENTER
        }

        header.addView(titleView)
        root.addView(header)

        val scroll = ScrollView(this)

        val content = LinearLayout(this).apply {
            orientation = LinearLayout.VERTICAL
            setPadding(24, 10, 24, 25)
        }

        scroll.addView(content)

        root.addView(
            scroll,
            LinearLayout.LayoutParams(
                ViewGroup.LayoutParams.MATCH_PARENT,
                0,
                1f
            )
        )

        root.addView(createNavigation())

        return Pair(root, content)
    }

    private fun createNavigation(): LinearLayout {

        val nav = LinearLayout(this).apply {
            orientation = LinearLayout.HORIZONTAL
            setPadding(5, 5, 5, 5)
        }

        val buttons = listOf(
            "Home",
            "Agents",
            "Tasks",
            "Content"
        )

        buttons.forEach { name ->

            val button = Button(this).apply {
                text = name
                textSize = 11f

                setOnClickListener {

                    when (name) {
                        "Home" -> showCommandCenter()
                        "Agents" -> showAgents()
                        "Tasks" -> showTasks()
                        "Content" -> showContent()
                    }
                }
            }

            nav.addView(
                button,
                LinearLayout.LayoutParams(
                    0,
                    ViewGroup.LayoutParams.WRAP_CONTENT,
                    1f
                )
            )
        }

        return nav
    }

    private fun showCommandCenter() {

        val pair = createRoot("COMMAND CENTER")

        val root = pair.first
        val content = pair.second

        commandInput = EditText(this).apply {
            hint = "Founder command..."
            setHintTextColor(Color.GRAY)
            setTextColor(Color.WHITE)
            textSize = 17f
        }

        content.addView(commandInput)

        val execute = Button(this).apply {
            text = "EXECUTE COMMAND"

            setOnClickListener {
                sendCommand()
            }
        }

        content.addView(execute)

        statusText = TextView(this).apply {
            text = "UDAAN AI CORE\nREADY"
            textSize = 16f
            setTextColor(Color.WHITE)
            setPadding(10, 25, 10, 25)
        }

        content.addView(statusText)

        val statusButton = Button(this).apply {

            text = "🔄 CHECK UDAAN AI STATUS"

            setOnClickListener {
                checkBackendStatus()
            }
        }

        content.addView(
            statusButton,
            LinearLayout.LayoutParams(
                ViewGroup.LayoutParams.MATCH_PARENT,
                ViewGroup.LayoutParams.WRAP_CONTENT
            ).apply {
                setMargins(0, 5, 0, 15)
            }
        )

        addCard(
            content,
            "🧠 MAIN AI",
            "Command orchestration"
        )

        addCard(
            content,
            "🤖 AI AGENTS",
            "10 specialized AI agents"
        )

        addCard(
            content,
            "🎬 VIDEO STUDIO",
            "Video creation workflow"
        )

        addCard(
            content,
            "📱 SOCIAL MEDIA",
            "Social automation"
        )

        addCard(
            content,
            "📊 ANALYTICS",
            "Performance analytics"
        )

        setContentView(root)
    }

    private fun showAgents() {

        val pair = createRoot("AI AGENTS")

        val root = pair.first
        val content = pair.second

        val info = TextView(this).apply {
            text = "SELECT AN AI AGENT"
            textSize = 17f
            setTextColor(Color.WHITE)
            setPadding(5, 10, 5, 20)
        }

        content.addView(info)

        agents.forEach { agent ->

            val button = Button(this).apply {

                text = agent

                setOnClickListener {
                    openAgent(agent)
                }
            }

            content.addView(
                button,
                LinearLayout.LayoutParams(
                    ViewGroup.LayoutParams.MATCH_PARENT,
                    ViewGroup.LayoutParams.WRAP_CONTENT
                ).apply {
                    setMargins(0, 5, 0, 5)
                }
            )
        }

        setContentView(root)
    }

    private fun openAgent(agent: String) {

        val pair = createRoot(agent)

        val root = pair.first
        val content = pair.second

        val description = TextView(this).apply {

            text =
                "$agent\n\nReady to receive Founder commands."

            textSize = 18f
            setTextColor(Color.WHITE)
            setPadding(5, 15, 5, 20)
        }

        content.addView(description)

        val input = EditText(this).apply {

            hint = "$agent command..."
            setHintTextColor(Color.GRAY)
            setTextColor(Color.WHITE)
            textSize = 16f
        }

        content.addView(input)

        val run = Button(this).apply {

            text = "RUN $agent"

            setOnClickListener {

                val command =
                    input.text.toString().trim()

                if (command.isEmpty()) {

                    Toast.makeText(
                        this@MainActivity,
                        "Command empty hai",
                        Toast.LENGTH_SHORT
                    ).show()

                } else {

                    commandInput =
                        EditText(this@MainActivity)

                    commandInput.setText(
                        "$agent: $command"
                    )

                    statusText = TextView(this@MainActivity).apply {
                        text = "🧠 UDAAN AI\n\nThinking..."
                        textSize = 16f
                        setTextColor(Color.WHITE)
                    }

                    sendCommand()
                }
            }
        }

        content.addView(run)

        setContentView(root)
    }

    private fun showTasks() {

        val pair = createRoot("TASKS")
        val root = pair.first
        val content = pair.second

        addCard(
            content,
            "📋 ACTIVE TASKS",
            "Founder tasks"
        )

        addCard(
            content,
            "⏳ PENDING APPROVAL",
            "Loading Founder Approval queue..."
        )

        addCard(
            content,
            "✅ COMPLETED",
            "Completed AI tasks"
        )

        setContentView(root)

        loadPendingApprovals()
    }

    private fun showContent() {

        val pair = createRoot("CONTENT")

        val root = pair.first
        val content = pair.second

        addCard(
            content,
            "✍️ CONTENT AI",
            "Scripts, captions and posts"
        )

        addCard(
            content,
            "🎬 VIDEO AI",
            "Video creation workflow"
        )

        addCard(
            content,
            "▶️ YOUTUBE AI",
            "YouTube workflow"
        )

        setContentView(root)
    }

    private fun addCard(
        parent: LinearLayout,
        title: String,
        description: String
    ) {

        val card = TextView(this).apply {

            text = "$title\n$description"

            textSize = 16f
            setTextColor(Color.WHITE)

            setPadding(20, 20, 20, 20)
        }

        parent.addView(
            card,
            LinearLayout.LayoutParams(
                ViewGroup.LayoutParams.MATCH_PARENT,
                ViewGroup.LayoutParams.WRAP_CONTENT
            ).apply {
                setMargins(0, 6, 0, 6)
            }
        )
    }

    private fun sendCommand() {

        val command =
            commandInput.text.toString().trim()

        if (command.isEmpty()) {

            Toast.makeText(
                this,
                "Founder command empty hai",
                Toast.LENGTH_SHORT
            ).show()

            return
        }

        statusText.text =
            "🧠 UDAAN AI\n\nThinking..."

        Thread {

            try {

                val json =
                    JSONObject()
                        .put("command", command)

                val body =
                    json.toString()
                        .toRequestBody(
                            "application/json".toMediaType()
                        )

                val request =
                    Request.Builder()
                        .url("$backendUrl/command")
                        .addHeader(
                            "X-Udaan-API-Key",
                            founderApiKey
                        )
                        .post(body)
                        .build()

                client.newCall(request)
                    .execute()
                    .use { response ->

                        val result =
                            response.body?.string() ?: ""

                        runOnUiThread {

                            if (!response.isSuccessful) {

                                statusText.text =
                                    "❌ BACKEND ERROR\n\n" +
                                    "HTTP ${response.code}\n\n" +
                                    result

                                return@runOnUiThread
                            }

                            try {

                                val jsonResult =
                                    JSONObject(result)

                                val status =
                                    jsonResult.optString(
                                        "status",
                                        "UNKNOWN"
                                    )

                                val agent =
                                    jsonResult.optString(
                                        "agent",
                                        "Main AI"
                                    )

                                val message =
                                    jsonResult.optString(
                                        "message",
                                        result
                                    )

                                when (status) {

                                    "SUCCESS" -> {

                                        statusText.text =
                                            "✅ UDAAN AI\n\n" +
                                            "STATUS: SUCCESS\n\n" +
                                            "Agent: $agent\n\n" +
                                            message
                                    }

                                    "PENDING_APPROVAL",
                                    "WAITING_APPROVAL",
                                    "READY_FOR_APPROVAL" -> {

                                        val approvalId =
                                            jsonResult.optString(
                                                "approval_id",
                                                ""
                                            )

                                        statusText.text =
                                            "👑 FOUNDER APPROVAL REQUIRED\n\n" +
                                            "Agent: $agent\n\n" +
                                            message +
                                            if (approvalId.isNotEmpty()) {
                                                "\n\nApproval ID:\n$approvalId"
                                            } else {
                                                ""
                                            }
                                    }

                                    "FAILED" -> {

                                        statusText.text =
                                            "❌ UDAAN AI\n\n" +
                                            "STATUS: FAILED\n\n" +
                                            message
                                    }

                                    else -> {

                                        statusText.text =
                                            "🤖 UDAAN AI RESPONSE\n\n" +
                                            "STATUS: $status\n\n" +
                                            "Agent: $agent\n\n" +
                                            message
                                    }
                                }

                            } catch (error: Exception) {

                                statusText.text =
                                    "🤖 UDAAN AI RESPONSE\n\n$result"
                            }
                        }
                    }

            } catch (error: Exception) {

                runOnUiThread {

                    statusText.text =
                        "❌ BACKEND CONNECTION FAILED\n\n" +
                        "${error.message}"
                }
            }
        }.start()
    }

    private fun loadPendingApprovals() {

        Toast.makeText(
            this,
            "Pending approvals loading...",
            Toast.LENGTH_SHORT
        ).show()

        Thread {

            try {

                val request =
                    Request.Builder()
                        .url("$backendUrl/approvals")
                        .addHeader(
                            "X-Udaan-API-Key",
                            founderApiKey
                        )
                        .get()
                        .build()

                client.newCall(request)
                    .execute()
                    .use { response ->

                        val result =
                            response.body?.string() ?: ""

                        runOnUiThread {

                            if (!response.isSuccessful) {

                                Toast.makeText(
                                    this@MainActivity,
                                    "Approval API Error: HTTP ${response.code}",
                                    Toast.LENGTH_LONG
                                ).show()

                                return@runOnUiThread
                            }

                            try {

                                val json =
                                    JSONObject(result)

                                val approvals =
                                    json.optJSONArray("approvals")
                                        ?: JSONArray()

                                if (approvals.length() == 0) {

                                    Toast.makeText(
                                        this@MainActivity,
                                        "No pending approvals",
                                        Toast.LENGTH_SHORT
                                    ).show()

                                } else {

                                    Toast.makeText(
                                        this@MainActivity,
                                        "${approvals.length()} pending approval(s)",
                                        Toast.LENGTH_LONG
                                    ).show()
                                }

                            } catch (error: Exception) {

                                Toast.makeText(
                                    this@MainActivity,
                                    "Approval response received",
                                    Toast.LENGTH_SHORT
                                ).show()
                            }
                        }
                    }

            } catch (error: Exception) {

                runOnUiThread {

                    Toast.makeText(
                        this@MainActivity,
                        "Approval connection failed: ${error.message}",
                        Toast.LENGTH_LONG
                    ).show()
                }
            }
        }.start()
    }

    private fun checkBackendStatus() {

        statusText.text =
            "🔄 UDAAN AI\n\nChecking backend..."

        Thread {

            try {

                val request =
                    Request.Builder()
                        .url("$backendUrl/status")
                        .addHeader(
                            "X-Udaan-API-Key",
                            founderApiKey
                        )
                        .get()
                        .build()

                client.newCall(request)
                    .execute()
                    .use { response ->

                        val result =
                            response.body?.string() ?: ""

                        runOnUiThread {

                            if (response.isSuccessful) {

                                try {

                                    val json =
                                        JSONObject(result)

                                    statusText.text =
                                        "🟢 UDAAN AI ONLINE\n\n" +
                                        "Backend: ONLINE\n" +
                                        "Core: " +
                                        json.optString(
                                            "core_state",
                                            "UNKNOWN"
                                        )

                                } catch (error: Exception) {

                                    statusText.text =
                                        "🟢 UDAAN AI ONLINE\n\n$result"
                                }

                            } else {

                                statusText.text =
                                    "❌ BACKEND ERROR\n\n" +
                                    "HTTP ${response.code}\n\n" +
                                    result
                            }
                        }
                    }

            } catch (error: Exception) {

                runOnUiThread {

                    statusText.text =
                        "❌ BACKEND CONNECTION FAILED\n\n" +
                        "${error.message}"
                }
            }
        }.start()
    }
}
