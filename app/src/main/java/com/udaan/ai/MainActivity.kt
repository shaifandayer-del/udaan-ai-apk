package com.udaan.ai

import android.graphics.Color
import android.graphics.Typeface
import android.graphics.drawable.GradientDrawable
import android.os.Bundle
import android.view.Gravity
import android.view.View
import android.widget.*
import androidx.appcompat.app.AppCompatActivity
import okhttp3.*
import okhttp3.MediaType.Companion.toMediaType
import org.json.JSONArray
import org.json.JSONObject
import java.io.IOException

data class UdaanAgent(
    val name: String,
    val description: String,
    val status: String
)

class MainActivity : AppCompatActivity() {

    private val backendUrl = "https://udaan-ai-apk-1.onrender.com"
    private val client = OkHttpClient()

    private var dynamicAgents = mutableListOf<UdaanAgent>()

    private lateinit var root: LinearLayout
    private lateinit var content: LinearLayout
    private lateinit var title: TextView
    private lateinit var subtitle: TextView
    private lateinit var statusText: TextView

    private val purple = Color.rgb(138, 77, 255)
    private val violet = Color.rgb(90, 45, 180)
    private val cyan = Color.rgb(60, 220, 255)
    private val white = Color.WHITE
    private val muted = Color.rgb(170, 170, 195)
    private val dark = Color.rgb(7, 7, 15)

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)

        window.statusBarColor = dark
        window.navigationBarColor = Color.BLACK

        buildMainUI()
        loadDynamicAgents()
    }

    private fun buildMainUI() {

        root = LinearLayout(this).apply {
            orientation = LinearLayout.VERTICAL
            setBackgroundColor(dark)
        }

        val header = LinearLayout(this).apply {
            orientation = LinearLayout.VERTICAL
            gravity = Gravity.CENTER_HORIZONTAL
            setPadding(20, 24, 20, 16)
            background = gradient(
                intArrayOf(
                    Color.rgb(18, 12, 38),
                    Color.rgb(7, 7, 15)
                ),
                0f
            )
        }

        val logo = ImageView(this).apply {
            setImageResource(R.drawable.udaan_logo)
            scaleType = ImageView.ScaleType.CENTER_INSIDE
        }

        header.addView(
            logo,
            LinearLayout.LayoutParams(
                -1,
                105
            )
        )

        title = text(
            "UDAAN AI",
            27f,
            white,
            Typeface.BOLD
        )

        subtitle = text(
            "AI COMMAND CENTER",
            12f,
            cyan,
            Typeface.BOLD
        )

        statusText = text(
            "● CONNECTING TO UDAAN CORE...",
            11f,
            muted,
            Typeface.NORMAL
        )

        header.addView(title)
        header.addView(space(4))
        header.addView(subtitle)
        header.addView(space(6))
        header.addView(statusText)

        root.addView(
            header,
            LinearLayout.LayoutParams(
                -1,
                -2
            )
        )

        val scroll = ScrollView(this).apply {
            isFillViewport = true
        }

        content = LinearLayout(this).apply {
            orientation = LinearLayout.VERTICAL
            setPadding(16, 8, 16, 30)
        }

        scroll.addView(content)

        root.addView(
            scroll,
            LinearLayout.LayoutParams(
                -1,
                0,
                1f
            )
        )

        setContentView(root)

        showHome()
    }

    private fun showHome() {

        clearContent()

        addSection(
            "COMMAND CENTER",
            "Control your entire UDAAN AI system"
        )

        addCommandBox()

        addSection(
            "CORE MODULES",
            "Your AI operating system"
        )

        moduleButton(
            "🤖",
            "AI AGENTS",
            "Research, Content, Video, YouTube, Social and more"
        ) {
            showAgents()
        }

        moduleButton(
            "⚡",
            "TASKS",
            "Manage active and completed AI tasks"
        ) {
            showTasks()
        }

        moduleButton(
            "🎬",
            "CONTENT STUDIO",
            "Create scripts, videos and content pipelines"
        ) {
            showContentStudio()
        }

        moduleButton(
            "📊",
            "ANALYTICS",
            "Monitor content and system performance"
        ) {
            showAnalytics()
        }

        moduleButton(
            "🔐",
            "FOUNDER APPROVAL",
            "Review actions waiting for approval"
        ) {
            showApprovals()
        }

        moduleButton(
            "⚙️",
            "SYSTEM",
            "Backend, security and automation status"
        ) {
            showSystem()
        }
    }

    private fun addCommandBox() {

        val card = LinearLayout(this).apply {
            orientation = LinearLayout.VERTICAL
            setPadding(18, 18, 18, 18)
            background = glass()
        }

        val label = text(
            "COMMAND",
            12f,
            cyan,
            Typeface.BOLD
        )

        val input = EditText(this).apply {
            hint = "Tell UDAAN what to do..."
        
        setHintTextColor(110, 110, 130)
            setTextColor(white)
            textSize = 16f
            setSingleLine(false)
            minLines = 2
            setPadding(14, 12, 14, 12)
            background = rounded(
                Color.rgb(15, 15, 28),
                18
            )
        }

        val button = Button(this).apply {
            text = "⚡ EXECUTE COMMAND"
            setTextColor(white)
            textSize = 14f
            typeface = Typeface.DEFAULT_BOLD
            background = gradient(
                intArrayOf(
                    purple,
                    violet
                ),
                18f
            )

            setOnClickListener {
                val command = input.text.toString().trim()

                if (command.isEmpty()) {
                    toast("Command enter karo")
                    return@setOnClickListener
                }

                sendCommand(command)
            }
        }

        card.addView(label)
        card.addView(space(10))
        card.addView(input)

        card.addView(
            button,
            LinearLayout.LayoutParams(
                -1,
                52
            ).apply {
                topMargin = 12
            }
        )

        content.addView(
            card,
            LinearLayout.LayoutParams(
                -1,
                -2
            ).apply {
                bottomMargin = 18
            }
        )
    }

    private fun showAgents() {

        clearContent()

        addBackButton()

        addSection(
            "AI AGENTS",
            "${dynamicAgents.size} agents connected to UDAAN Core"
        )

        if (dynamicAgents.isEmpty()) {

            addInfoCard(
                "CONNECTING...",
                "Loading UDAAN AI agents from backend."
            )

            return
        }

        dynamicAgents.forEach { agent ->

            moduleButton(
                "🧠",
                agent.name,
                agent.description
            ) {
                openAgent(agent)
            }
        }
    }

    private fun openAgent(agent: UdaanAgent) {

        clearContent()

        addBackButton()

        addSection(
            agent.name,
            agent.description
        )

        addInfoCard(
            "STATUS",
            "● ${agent.status}"
        )

        val input = EditText(this).apply {
            hint = "Command for ${agent.name}"
            setHintTextColor = Color.GRAY
            setTextColor(white)
            textSize = 16f
            minLines = 3
            setPadding(14, 14, 14, 14)
            background = rounded(
                Color.rgb(15, 15, 28),
                18
            )
        }

        content.addView(
            input,
            LinearLayout.LayoutParams(
                -1,
                130
            ).apply {
                bottomMargin = 12
            }
        )

        val execute = Button(this).apply {
            text = "⚡ RUN ${agent.name.uppercase()}"
            setTextColor(white)
            typeface = Typeface.DEFAULT_BOLD
            background = gradient(
                intArrayOf(
                    purple,
                    violet
                ),
                18f
            )

            setOnClickListener {

                val command = input.text.toString().trim()

                if (command.isEmpty()) {
                    toast("Command enter karo")
                    return@setOnClickListener
                }

                sendCommand(command)
            }
        }

        content.addView(
            execute,
            LinearLayout.LayoutParams(
                -1,
                54
            )
        )
    }

    private fun showTasks() {

        clearContent()
        addBackButton()

        addSection(
            "TASKS",
            "UDAAN task management"
        )

        addInfoCard(
            "ACTIVE TASKS",
            "Tasks created by UDAAN AI will appear here."
        )

        addInfoCard(
            "EXECUTION",
            "AI agents execute commands through the Python backend."
        )
    }

    private fun showContentStudio() {

        clearContent()
        addBackButton()

        addSection(
            "CONTENT STUDIO",
            "Create and manage AI content"
        )

        moduleButton(
            "✍️",
            "SCRIPT CREATOR",
            "Generate video scripts and ideas"
        ) {
            sendCommand("create a video script")
        }

        moduleButton(
            "🎥",
            "VIDEO STUDIO",
            "Create video production projects"
        ) {
            sendCommand("create a video project")
        }

        moduleButton(
            "▶️",
            "YOUTUBE",
            "YouTube research, publishing and management"
        ) {
            sendCommand("open YouTube AI")
        }

        moduleButton(
            "📱",
            "SOCIAL MEDIA",
            "Social content and publishing"
        ) {
            sendCommand("open Social Media AI")
        }
    }

    private fun showAnalytics() {

        clearContent()
        addBackButton()

        addSection(
            "ANALYTICS",
            "UDAAN performance center"
        )

        addInfoCard(
            "CONTENT ANALYTICS",
            "Track views, engagement and content performance."
        )

        addInfoCard(
            "SYSTEM ANALYTICS",
            "Monitor AI agents and backend execution."
        )
    }

    private fun showApprovals() {

        clearContent()
        addBackButton()

        addSection(
            "FOUNDER APPROVAL",
            "No external action should execute without approval."
        )

        addInfoCard(
            "APPROVAL CONTROL",
            "You remain the final authority for publish, upload and other consequential actions."
        )

        val refresh = Button(this).apply {
            text = "🔄 CHECK APPROVALS"
            setTextColor(white)
            background = gradient(
                intArrayOf(
                    purple,
                    violet
                ),
                18f
            )

            setOnClickListener {
                loadApprovals()
            }
        }

        content.addView(
            refresh,
            LinearLayout.LayoutParams(
                -1,
                54
            )
        )
    }

    private fun showSystem() {

        clearContent()
        addBackButton()

        addSection(
            "UDAAN SYSTEM",
            "Core infrastructure"
        )

        addInfoCard(
            "BACKEND",
            backendUrl
        )

        addInfoCard(
            "SECURITY",
            "Founder API Key authentication enabled."
        )

        addInfoCard(
            "AGENTS",
            "${dynamicAgents.size} dynamic agents loaded."
        )

        val refresh = Button(this).apply {
            text = "🔄 REFRESH SYSTEM"
            setTextColor(white)
            background = gradient(
                intArrayOf(
                    purple,
                    violet
                ),
                18f
            )

            setOnClickListener {
                loadDynamicAgents()
                toast("System refreshed")
            }
        }

        content.addView(
            refresh,
            LinearLayout.LayoutParams(
                -1,
                54
            )
        )
    }

    private fun loadDynamicAgents() {

        val request = Request.Builder()
            .url("$backendUrl/agents")
            .get()
            .addHeader(
                "X-Udaan-API-Key",
                BuildConfig.UDAAN_FOUNDER_API_KEY
            )
            .build()

        client.newCall(request).enqueue(
            object : Callback {

                override fun onFailure(
                    call: Call,
                    e: IOException
                ) {
                    runOnUiThread {
                        statusText.text =
                            "● BACKEND OFFLINE"
                        statusText.setTextColor(
                            Color.rgb(255, 90, 90)
                        )
                    }
                }

                override fun onResponse(
                    call: Call,
                    response: Response
                ) {

                    val body = response.body?.string()

                    if (!response.isSuccessful || body == null) {
                        runOnUiThread {
                            statusText.text =
                                "● BACKEND ERROR"
                        }
                        return
                    }

                    try {

                        val json = JSONObject(body)
                        val array = json.optJSONArray("agents")
                            ?: JSONArray()

                        val loaded =
                            mutableListOf<UdaanAgent>()

                        for (i in 0 until array.length()) {

                            val item =
                                array.getJSONObject(i)

                            loaded.add(
                                UdaanAgent(
                                    item.optString(
                                        "name",
                                        "Unknown Agent"
                                    ),
                                    item.optString(
                                        "description",
                                        "UDAAN AI Agent"
                                    ),
                                    item.optString(
                                        "status",
                                        "READY"
                                    )
                                )
                            )
                        }

                        dynamicAgents = loaded

                        runOnUiThread {

                            statusText.text =
                                "● UDAAN CORE ONLINE • ${dynamicAgents.size} AGENTS"

                            statusText.setTextColor(cyan)

                            showHome()
                        }

                    } catch (e: Exception) {

                        runOnUiThread {
                            statusText.text =
                                "● AGENT DATA ERROR"
                        }
                    }
                }
            }
        )
    }

    private fun sendCommand(command: String) {

        statusText.text = "● EXECUTING..."
        statusText.setTextColor(cyan)

        val json = JSONObject().apply {
            put("command", command)
        }

        val body = RequestBody.create(
            "application/json".toMediaType(),
            json.toString()
        )

        val request = Request.Builder()
            .url("$backendUrl/command")
            .post(body)
            .addHeader(
                "Content-Type",
                "application/json"
            )
            .addHeader(
                "X-Udaan-API-Key",
                BuildConfig.UDAAN_FOUNDER_API_KEY
            )
            .build()

        client.newCall(request).enqueue(
            object : Callback {

                override fun onFailure(
                    call: Call,
                    e: IOException
                ) {

                    runOnUiThread {

                        statusText.text =
                            "● COMMAND FAILED"

                        toast(
                            "Backend connection failed"
                        )
                    }
                }

                override fun onResponse(
                    call: Call,
                    response: Response
                ) {

                    val result =
                        response.body?.string()
                            ?: "No response"

                    runOnUiThread {

                        statusText.text =
                            if (response.isSuccessful)
                                "● COMMAND COMPLETED"
                            else
                                "● COMMAND ERROR"

                        showResult(
                            result
                        )
                    }
                }
            }
        )
    }

    private fun loadApprovals() {

        val request = Request.Builder()
            .url("$backendUrl/approvals")
            .get()
            .addHeader(
                "X-Udaan-API-Key",
                BuildConfig.UDAAN_FOUNDER_API_KEY
            )
            .build()

        client.newCall(request).enqueue(
            object : Callback {

                override fun onFailure(
                    call: Call,
                    e: IOException
                ) {
                    runOnUiThread {
                        toast("Approval connection failed")
                    }
                }

                override fun onResponse(
                    call: Call,
                    response: Response
                ) {

                    val result =
                        response.body?.string()
                            ?: "No approval data"

                    runOnUiThread {
                        showResult(result)
                    }
                }
            }
        )
    }

    private fun showResult(result: String) {

        clearContent()
        addBackButton()

        addSection(
            "UDAAN RESPONSE",
            "Backend execution result"
        )

        val box = TextView(this).apply {
            text = result
            textSize = 14f
            setTextColor(white)
            setPadding(18, 18, 18, 18)
            background = glass()
        }

        content.addView(
            box,
            LinearLayout.LayoutParams(
                -1,
                -2
            )
        )
    }

    private fun addBackButton() {

        val button = Button(this).apply {
            text = "← BACK"
            setTextColor(white)
            background = rounded(
                Color.rgb(25, 25, 42),
                16
            )

            setOnClickListener {
                showHome()
            }
        }

        content.addView(
            button,
            LinearLayout.LayoutParams(
                -1,
                48
            ).apply {
                bottomMargin = 14
            }
        )
    }

    private fun addSection(
        heading: String,
        description: String
    ) {

        content.addView(
            text(
                heading,
                21f,
                white,
                Typeface.BOLD
            )
        )

        content.addView(
            text(
                description,
                12f,
                muted,
                Typeface.NORMAL
            )
        )

        content.addView(
            space(14)
        )
    }

    private fun moduleButton(
        icon: String,
        heading: String,
        description: String,
        action: () -> Unit
    ) {

        val card = LinearLayout(this).apply {
            orientation = LinearLayout.HORIZONTAL
            gravity = Gravity.CENTER_VERTICAL
            setPadding(16, 14, 16, 14)
            background = glass()
            isClickable = true
            setOnClickListener {
                action()
            }
        }

        val iconView = text(
            icon,
            28f,
            white,
            Typeface.NORMAL
        )

        iconView.gravity = Gravity.CENTER

        card.addView(
            iconView,
            LinearLayout.LayoutParams(
                54,
                54
            )
        )

        val textBox = LinearLayout(this).apply {
            orientation = LinearLayout.VERTICAL
            setPadding(14, 0, 0, 0)
        }

        textBox.addView(
            text(
                heading,
                15f,
                white,
                Typeface.BOLD
            )
        )

        textBox.addView(
            space(3)
        )

        textBox.addView(
            text(
                description,
                11f,
                muted,
                Typeface.NORMAL
            )
        )

        card.addView(
            textBox,
            LinearLayout.LayoutParams(
                0,
                -2,
                1f
            )
        )

        val arrow = text(
            "›",
            30f,
            purple,
            Typeface.BOLD
        )

        card.addView(arrow)

        content.addView(
            card,
            LinearLayout.LayoutParams(
                -1,
                -2
            ).apply {
                bottomMargin = 10
            }
        )
    }

    private fun addInfoCard(
        heading: String,
        message: String
    ) {

        val card = LinearLayout(this).apply {
            orientation = LinearLayout.VERTICAL
            setPadding(18, 16, 18, 16)
            background = glass()
        }

        card.addView(
            text(
                heading,
                13f,
                cyan,
                Typeface.BOLD
            )
        )

        card.addView(
            space(6)
        )

        card.addView(
            text(
                message,
                13f,
                white,
                Typeface.NORMAL
            )
        )

        content.addView(
            card,
            LinearLayout.LayoutParams(
                -1,
                -2
            ).apply {
                bottomMargin = 12
            }
        )
    }

    private fun clearContent() {
        content.removeAllViews()
    }

    private fun text(
        value: String,
        size: Float,
        color: Int,
        style: Int
    ): TextView {

        return TextView(this).apply {
            text = value
            textSize = size
            setTextColor(color)
            typeface = Typeface.create(
                Typeface.DEFAULT,
                style
            )
        }
    }

    private fun space(height: Int): Space {
        return Space(this).apply {
            layoutParams = LinearLayout.LayoutParams(
                1,
                height
            )
        }
    }

    private fun rounded(
        color: Int,
        radius: Int
    ): GradientDrawable {

        return GradientDrawable().apply {
            setColor(color)
            cornerRadius = radius.toFloat()
            setStroke(
                1,
                Color.rgb(45, 35, 75)
            )
        }
    }

    private fun glass(): GradientDrawable {

        return GradientDrawable(
            GradientDrawable.Orientation.TL_BR,
            intArrayOf(
                Color.rgb(27, 20, 48),
                Color.rgb(12, 12, 24)
            )
        ).apply {
            cornerRadius = 22f
            setStroke(
                1,
                Color.rgb(70, 45, 115)
            )
        }
    }

    private fun gradient(
        colors: IntArray,
        radius: Float
    ): GradientDrawable {

        return GradientDrawable(
            GradientDrawable.Orientation.LEFT_RIGHT,
            colors
        ).apply {
            cornerRadius = radius
        }
    }

    private fun toast(message: String) {
        Toast.makeText(
            this,
            message,
            Toast.LENGTH_SHORT
        ).show()
    }
}
