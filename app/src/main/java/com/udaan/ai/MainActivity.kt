package com.udaan.ai

import android.graphics.Color
import android.graphics.Typeface
import android.graphics.drawable.GradientDrawable
import android.os.Bundle
import android.os.Handler
import android.os.Looper
import android.view.Gravity
import android.view.View
import android.widget.*
import androidx.appcompat.app.AppCompatActivity
import okhttp3.*
import okhttp3.MediaType.Companion.toMediaType
import org.json.JSONArray
import org.json.JSONObject
import java.io.IOException

class MainActivity : AppCompatActivity() {

    private val backendUrl =
        "https://udaan-ai-apk-1.onrender.com"

    private val client =
        OkHttpClient()

    private val handler =
        Handler(Looper.getMainLooper())

    private var dynamicAgents =
        mutableListOf<UdaanAgent>()

    private lateinit var root: LinearLayout
    private lateinit var content: LinearLayout
    private lateinit var title: TextView
    private lateinit var subtitle: TextView
    private lateinit var statusText: TextView

    private val purple =
        Color.rgb(138, 77, 255)

    private val violet =
        Color.rgb(72, 35, 160)

    private val cyan =
        Color.rgb(60, 220, 255)

    private val white =
        Color.WHITE

    private val muted =
        Color.rgb(170, 170, 195)

    private val dark =
        Color.rgb(5, 5, 13)

    private val surface =
        Color.rgb(12, 12, 24)

    override fun onCreate(
        savedInstanceState: Bundle?
    ) {
        super.onCreate(savedInstanceState)

        window.statusBarColor = dark
        window.navigationBarColor = Color.BLACK

        showLaunchScreen()

        handler.postDelayed({
            buildMainUI()
            loadDynamicAgents()
        }, 1400)
    }

    private fun showLaunchScreen() {

        val launch =
            FrameLayout(this).apply {
                setBackgroundColor(dark)
            }

        val glow =
            TextView(this).apply {
                text = "✦"
                textSize = 90f
                gravity = Gravity.CENTER
                setTextColor(purple)
            }

        launch.addView(
            glow,
            FrameLayout.LayoutParams(
                -1,
                180
            ).apply {
                gravity = Gravity.CENTER
            }
        )

        val logo =
            ImageView(this).apply {
                setImageResource(
                    R.drawable.udaan_logo
                )
                scaleType =
                    ImageView.ScaleType.CENTER_INSIDE
            }

        launch.addView(
            logo,
            FrameLayout.LayoutParams(
                -1,
                210
            ).apply {
                gravity = Gravity.CENTER
            }
        )

        val name =
            text(
                "UDAAN AI",
                28f,
                white,
                Typeface.BOLD
            )

        launch.addView(
            name,
            FrameLayout.LayoutParams(
                -1,
                55
            ).apply {
                gravity = Gravity.CENTER_HORIZONTAL
                topMargin = 280
            }
        )

        val loading =
            text(
                "AI COMMAND CENTER",
                11f,
                cyan,
                Typeface.BOLD
            )

        loading.gravity = Gravity.CENTER

        launch.addView(
            loading,
            FrameLayout.LayoutParams(
                -1,
                45
            ).apply {
                gravity = Gravity.CENTER_HORIZONTAL
                topMargin = 335
            }
        )

        setContentView(launch)
    }

    private fun buildMainUI() {

        root =
            LinearLayout(this).apply {
                orientation =
                    LinearLayout.VERTICAL
                setBackgroundColor(dark)
            }

        val header =
            LinearLayout(this).apply {
                orientation =
                    LinearLayout.VERTICAL
                gravity =
                    Gravity.CENTER_HORIZONTAL
                setPadding(
                    18,
                    18,
                    18,
                    16
                )
                background =
                    gradient(
                        intArrayOf(
                            Color.rgb(28, 15, 55),
                            Color.rgb(8, 8, 17)
                        ),
                        0f
                    )
            }

        val logo =
            ImageView(this).apply {
                setImageResource(
                    R.drawable.udaan_logo
                )
                scaleType =
                    ImageView.ScaleType.CENTER_INSIDE
            }

        header.addView(
            logo,
            LinearLayout.LayoutParams(
                -1,
                86
            )
        )

        title =
            text(
                "UDAAN AI",
                27f,
                white,
                Typeface.BOLD
            )

        subtitle =
            text(
                "3D AI COMMAND CENTER",
                12f,
                cyan,
                Typeface.BOLD
            )

        statusText =
            text(
                "● CONNECTING TO UDAAN CORE...",
                11f,
                muted,
                Typeface.NORMAL
            )

        header.addView(title)
        header.addView(space(3))
        header.addView(subtitle)
        header.addView(space(5))
        header.addView(statusText)

        root.addView(
            header,
            LinearLayout.LayoutParams(
                -1,
                -2
            )
        )

        val scroll =
            ScrollView(this).apply {
                isFillViewport = true
            }

        content =
            LinearLayout(this).apply {
                orientation =
                    LinearLayout.VERTICAL
                setPadding(
                    14,
                    12,
                    14,
                    30
                )
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
            "UDAAN COMMAND CENTER",
            "Your personal AI operating system"
        )

        addCommandBox()

        addSection(
            "AI CORE",
            "Access every UDAAN intelligence module"
        )

        moduleButton(
            "🧠",
            "AI AGENTS",
            "${dynamicAgents.size} intelligent agents"
        ) {
            showAgents()
        }

        moduleButton(
            "🎬",
            "VIDEO STUDIO",
            "Create and manage complete video projects"
        ) {
            showVideoStudio()
        }

        moduleButton(
            "📱",
            "APP BUILDER",
            "Build software and applications with AI"
        ) {
            showAppBuilder()
        }

        moduleButton(
            "✍️",
            "CONTENT STUDIO",
            "Scripts, ideas and content automation"
        ) {
            showContentStudio()
        }

        moduleButton(
            "⚡",
            "TASK CENTER",
            "Manage AI tasks and execution"
        ) {
            showTasks()
        }

        moduleButton(
            "📊",
            "ANALYTICS",
            "Monitor performance and system data"
        ) {
            showAnalytics()
        }

        moduleButton(
            "🔐",
            "FOUNDER APPROVAL",
            "Control consequential AI actions"
        ) {
            showApprovals()
        }

        moduleButton(
            "🔔",
            "NOTIFICATIONS",
            "UDAAN alerts and activity"
        ) {
            showNotifications()
        }

        moduleButton(
            "⚙️",
            "SETTINGS",
            "Configure your UDAAN AI system"
        ) {
            showSettings()
        }

        moduleButton(
            "🖥️",
            "SYSTEM",
            "Backend, agents and security"
        ) {
            showSystem()
        }
    }

    private fun addCommandBox() {

        val card =
            LinearLayout(this).apply {
                orientation =
                    LinearLayout.VERTICAL
                setPadding(
                    18,
                    18,
                    18,
                    18
                )
                background = glass()
                elevation = 14f
            }

        card.addView(
            text(
                "COMMAND",
                12f,
                cyan,
                Typeface.BOLD
            )
        )

        val input =
            EditText(this).apply {
                hint =
                    "Tell UDAAN what to do..."
                setHintTextColor(
                    Color.rgb(
                        110,
                        110,
                        130
                    )
                )
                setTextColor(white)
                textSize = 16f
                minLines = 2
                setPadding(
                    14,
                    12,
                    14,
                    12
                )
                background =
                    rounded(
                        Color.rgb(
                            15,
                            15,
                            28
                        ),
                        18
                    )
            }

        val button =
            Button(this).apply {
                text =
                    "⚡ EXECUTE COMMAND"
                setTextColor(white)
                typeface =
                    Typeface.DEFAULT_BOLD
                background =
                    gradient(
                        intArrayOf(
                            purple,
                            violet
                        ),
                        20f
                    )

                setOnClickListener {

                    val command =
                        input.text
                            .toString()
                            .trim()

                    if (command.isEmpty()) {
                        toast(
                            "Command enter karo"
                        )
                        return@setOnClickListener
                    }

                    sendCommand(command)
                }
            }

        card.addView(
            input,
            LinearLayout.LayoutParams(
                -1,
                115
            ).apply {
                topMargin = 10
            }
        )

        card.addView(
            button,
            LinearLayout.LayoutParams(
                -1,
                54
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
            "All intelligence modules connected to UDAAN Core"
        )

        if (dynamicAgents.isEmpty()) {

            addInfoCard(
                "AGENTS LOADING",
                "UDAAN is connecting to the Python backend."
            )

            return
        }

        dynamicAgents.forEach { agent ->

            val active =
                agent.status.equals(
                    "ACTIVE",
                    true
                ) ||
                agent.status.equals(
                    "READY",
                    true
                ) ||
                agent.status.equals(
                    "ONLINE",
                    true
                )

            moduleButton(
                if (active) "🟢"
                else "🔴",
                agent.name,
                "${agent.description} • ${agent.status}"
            ) {
                openAgent(agent)
            }
        }
    }

    private fun openAgent(
        agent: UdaanAgent
    ) {

        clearContent()
        addBackButton()

        addSection(
            agent.name,
            agent.description
        )

        addInfoCard(
            "AGENT STATUS",
            "● ${agent.status}"
        )

        val input =
            EditText(this).apply {
                hint =
                    "Command for ${agent.name}"
                setHintTextColor(
                    Color.rgb(
                        110,
                        110,
                        130
                    )
                )
                setTextColor(white)
                textSize = 16f
                minLines = 4
                setPadding(
                    14,
                    14,
                    14,
                    14
                )
                background =
                    rounded(
                        Color.rgb(
                            15,
                            15,
                            28
                        ),
                        18
                    )
            }

        content.addView(
            input,
            LinearLayout.LayoutParams(
                -1,
                145
            ).apply {
                bottomMargin = 12
            }
        )

        val execute =
            Button(this).apply {
                text =
                    "⚡ RUN ${agent.name.uppercase()}"
                setTextColor(white)
                typeface =
                    Typeface.DEFAULT_BOLD
                background =
                    gradient(
                        intArrayOf(
                            purple,
                            violet
                        ),
                        18f
                    )

                setOnClickListener {

                    val command =
                        input.text
                            .toString()
                            .trim()

                    if (command.isEmpty()) {
                        toast(
                            "Command enter karo"
                        )
                        return@setOnClickListener
                    }

                    sendCommand(
                        "${agent.name}: $command"
                    )
                }
            }

        content.addView(
            execute,
            LinearLayout.LayoutParams(
                -1,
                56
            )
        )
    }

    private fun showVideoStudio() {

        clearContent()
        addBackButton()

        addSection(
            "VIDEO STUDIO",
            "Complete AI video production center"
        )

        moduleButton(
            "💡",
            "VIDEO IDEA",
            "Generate a video concept"
        ) {
            sendCommand(
                "create a video idea"
            )
        }

        moduleButton(
            "📝",
            "VIDEO SCRIPT",
            "Create a complete video script"
        ) {
            sendCommand(
                "create a video script"
            )
        }

        moduleButton(
            "🎞️",
            "VIDEO PROJECT",
            "Start a complete video production"
        ) {
            sendCommand(
                "create a video project"
            )
        }

        moduleButton(
            "🎥",
            "VIDEO RENDER",
            "Run the AI video production pipeline"
        ) {
            sendCommand(
                "render the approved video"
            )
        }

        moduleButton(
            "▶️",
            "YOUTUBE PUBLISH",
            "Prepare an approved YouTube upload"
        ) {
            sendCommand(
                "prepare YouTube upload"
            )
        }

        addInfoCard(
            "FOUNDER CONTROL",
            "Publishing and consequential external actions require Founder Approval."
        )
    }

    private fun showAppBuilder() {

        clearContent()
        addBackButton()

        addSection(
            "APP BUILDER",
            "Build applications and software through UDAAN AI"
        )

        val input =
            EditText(this).apply {
                hint =
                    "Describe the app you want to build..."
                setHintTextColor(
                    Color.rgb(
                        110,
                        110,
                        130
                    )
                )
                setTextColor(white)
                textSize = 15f
                minLines = 5
                setPadding(
                    15,
                    15,
                    15,
                    15
                )
                background =
                    rounded(
                        Color.rgb(
                            15,
                            15,
                            28
                        ),
                        18
                    )
            }

        content.addView(
            input,
            LinearLayout.LayoutParams(
                -1,
                170
            ).apply {
                bottomMargin = 12
            }
        )

        val build =
            Button(this).apply {
                text =
                    "🚀 BUILD APP"
                setTextColor(white)
                typeface =
                    Typeface.DEFAULT_BOLD
                background =
                    gradient(
                        intArrayOf(
                            purple,
                            violet
                        ),
                        18f
                    )

                setOnClickListener {

                    val request =
                        input.text
                            .toString()
                            .trim()

                    if (request.isEmpty()) {
                        toast(
                            "App description enter karo"
                        )
                        return@setOnClickListener
                    }

                    sendCommand(
                        "build an app: $request"
                    )
                }
            }

        content.addView(
            build,
            LinearLayout.LayoutParams(
                -1,
                56
            )
        )

        addInfoCard(
            "FOUNDER APPROVAL",
            "Final build, deployment or external publication remains under Founder control."
        )
    }

    private fun showContentStudio() {

        clearContent()
        addBackButton()

        addSection(
            "CONTENT STUDIO",
            "AI-powered content creation"
        )

        moduleButton(
            "💡",
            "CONTENT IDEA",
            "Generate content ideas"
        ) {
            sendCommand(
                "generate content ideas"
            )
        }

        moduleButton(
            "✍️",
            "SCRIPT CREATOR",
            "Create a complete script"
        ) {
            sendCommand(
                "create a content script"
            )
        }

        moduleButton(
            "🔎",
            "CONTENT RESEARCH",
            "Research current content opportunities"
        ) {
            sendCommand(
                "research latest content trends"
            )
        }

        moduleButton(
            "📺",
            "YOUTUBE AI",
            "YouTube research and publishing"
        ) {
            sendCommand(
                "open YouTube AI"
            )
        }

        moduleButton(
            "📱",
            "SOCIAL AI",
            "Social media content and publishing"
        ) {
            sendCommand(
                "open Social Media AI"
            )
        }
    }

    private fun showTasks() {

        clearContent()
        addBackButton()

        addSection(
            "TASK CENTER",
            "UDAAN AI task management"
        )

        addInfoCard(
            "ACTIVE TASKS",
            "Tasks created through UDAAN will appear here."
        )

        addInfoCard(
            "EXECUTION",
            "Commands are routed through the Python backend and AI agent system."
        )

        moduleButton(
            "🔄",
            "REFRESH TASK SYSTEM",
            "Refresh UDAAN execution state"
        ) {
            loadDynamicAgents()
            toast(
                "Task system refreshed"
            )
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
            "AI PERFORMANCE",
            "Monitor agent execution and system activity."
        )

        addInfoCard(
            "CONTENT PERFORMANCE",
            "Track content, video and publishing performance."
        )

        addInfoCard(
            "SYSTEM HEALTH",
            "Backend and agent availability."
        )
    }

    private fun showApprovals() {

        clearContent()
        addBackButton()

        addSection(
            "FOUNDER APPROVAL",
            "You remain the final authority."
        )

        addInfoCard(
            "APPROVAL POLICY",
            "Publish, upload, deployment and other consequential actions require Founder approval."
        )

        val refresh =
            Button(this).apply {
                text =
                    "🔄 CHECK APPROVALS"
                setTextColor(white)
                typeface =
                    Typeface.DEFAULT_BOLD
                background =
                    gradient(
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
                55
            )
        )
    }

    private fun showNotifications() {

        clearContent()
        addBackButton()

        addSection(
            "NOTIFICATIONS",
            "UDAAN activity and alerts"
        )

        addInfoCard(
            "CURRENT STATUS",
            "Notifications are controlled from UDAAN Settings."
        )

        moduleButton(
            "🔕",
            "NOTIFICATION CONTROL",
            "Manage UDAAN notification behavior"
        ) {
            showSettings()
        }
    }

    private fun showSettings() {

        clearContent()
        addBackButton()

        addSection(
            "SETTINGS",
            "Configure your UDAAN AI Command Center"
        )

        addInfoCard(
            "FOUNDER MODE",
            "Founder approval remains enabled for consequential actions."
        )

        addInfoCard(
            "BACKEND",
            backendUrl
        )

        addInfoCard(
            "AGENT CONNECTION",
            "${dynamicAgents.size} agents currently loaded."
        )

        val notificationSwitch =
            Switch(this).apply {
                text =
                    "UDAAN Notifications"
                textSize = 15f
                setTextColor(white)
                isChecked = false
                setPadding(
                    5,
                    12,
                    5,
                    12
                )
            }

        content.addView(
            notificationSwitch,
            LinearLayout.LayoutParams(
                -1,
                60
            )
        )

        addInfoCard(
            "NOTIFICATION POLICY",
            "No automatic external action is performed merely because a notification is shown."
        )

        moduleButton(
            "🔄",
            "REFRESH CONNECTION",
            "Reconnect to UDAAN Core"
        ) {
            loadDynamicAgents()
        }
    }

    private fun showSystem() {

        clearContent()
        addBackButton()

        addSection(
            "UDAAN SYSTEM",
            "Core infrastructure and security"
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

        val refresh =
            Button(this).apply {
                text =
                    "🔄 REFRESH UDAAN CORE"
                setTextColor(white)
                typeface =
                    Typeface.DEFAULT_BOLD
                background =
                    gradient(
                        intArrayOf(
                            purple,
                            violet
                        ),
                        18f
                    )

                setOnClickListener {
                    loadDynamicAgents()
                    toast(
                        "UDAAN Core refreshed"
                    )
                }
            }

        content.addView(
            refresh,
            LinearLayout.LayoutParams(
                -1,
                56
            )
        )
    }

    private fun loadDynamicAgents() {

        val request =
            Request.Builder()
                .url(
                    "$backendUrl/agents"
                )
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
                            Color.rgb(
                                255,
                                80,
                                90
                            )
                        )
                    }
                }

                override fun onResponse(
                    call: Call,
                    response: Response
                ) {

                    response.use {

                        val body =
                            it.body?.string()

                        if (
                            !it.isSuccessful ||
                            body == null
                        ) {

                            runOnUiThread {
                                statusText.text =
                                    "● BACKEND ERROR"
                            }

                            return
                        }

                        try {

                            val json =
                                JSONObject(body)

                            val array =
                                json.optJSONArray(
                                    "agents"
                                )
                                    ?: JSONArray()

                            val loaded =
                                mutableListOf<UdaanAgent>()

                            for (
                                i in 0 until
                                    array.length()
                            ) {

                                val item =
                                    array.getJSONObject(
                                        i
                                    )

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

                            dynamicAgents =
                                loaded

                            runOnUiThread {

                                statusText.text =
                                    "● UDAAN CORE ONLINE • ${dynamicAgents.size} AGENTS"

                                statusText.setTextColor(
                                    cyan
                                )

                                if (
                                    content.childCount == 0
                                ) {
                                    showHome()
                                }
                            }

                        } catch (
                            _: Exception
                        ) {

                            runOnUiThread {
                                statusText.text =
                                    "● AGENT DATA ERROR"
                            }
                        }
                    }
                }
            }
        )
    }

    private fun sendCommand(
        command: String
    ) {

        statusText.text =
            "● UDAAN EXECUTING..."

        statusText.setTextColor(cyan)

        val json =
            JSONObject().apply {
                put(
                    "command",
                    command
                )
            }

        val body =
            RequestBody.create(
                "application/json"
                    .toMediaType(),
                json.toString()
            )

        val request =
            Request.Builder()
                .url(
                    "$backendUrl/command"
                )
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

                        statusText.setTextColor(
                            Color.rgb(
                                255,
                                80,
                                90
                            )
                        )

                        toast(
                            "Backend connection failed"
                        )
                    }
                }

                override fun onResponse(
                    call: Call,
                    response: Response
                ) {

                    response.use {

                        val result =
                            it.body?.string()
                                ?: "No response"

                        runOnUiThread {

                            statusText.text =
                                if (
                                    it.isSuccessful
                                )
                                    "● COMMAND COMPLETED"
                                else
                                    "● COMMAND ERROR"

                            showResult(result)
                        }
                    }
                }
            }
        )
    }

    private fun loadApprovals() {

        val request =
            Request.Builder()
                .url(
                    "$backendUrl/approvals"
                )
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
                        toast(
                            "Approval connection failed"
                        )
                    }
                }

                override fun onResponse(
                    call: Call,
                    response: Response
                ) {

                    response.use {

                        val result =
                            it.body?.string()
                                ?: "No approval data"

                        runOnUiThread {
                            showResult(result)
                        }
                    }
                }
            }
        )
    }

    private fun showResult(
        result: String
    ) {

        clearContent()
        addBackButton()

        addSection(
            "UDAAN RESPONSE",
            "Live backend execution result"
        )

        val box =
            TextView(this).apply {
                text = result
                textSize = 14f
                setTextColor(white)
                setPadding(
                    18,
                    18,
                    18,
                    18
                )
                background = glass()
                elevation = 10f
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

        val button =
            Button(this).apply {
                text = "← BACK"
                setTextColor(white)
                background =
                    rounded(
                        Color.rgb(
                            24,
                            24,
                            42
                        ),
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
                22f,
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

        val card =
            LinearLayout(this).apply {
                orientation =
                    LinearLayout.HORIZONTAL
                gravity =
                    Gravity.CENTER_VERTICAL
                setPadding(
                    15,
                    14,
                    15,
                    14
                )
                background = glass()
                elevation = 12f
                isClickable = true

                setOnClickListener {
                    action()
                }
            }

        val iconView =
            text(
                icon,
                28f,
                white,
                Typeface.NORMAL
            )

        iconView.gravity =
            Gravity.CENTER

        card.addView(
            iconView,
            LinearLayout.LayoutParams(
                55,
                55
            )
        )

        val textBox =
            LinearLayout(this).apply {
                orientation =
                    LinearLayout.VERTICAL
                setPadding(
                    14,
                    0,
                    8,
                    0
                )
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
            space(4)
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

        val arrow =
            text(
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
                bottomMargin = 11
            }
        )
    }

    private fun addInfoCard(
        heading: String,
        message: String
    ) {

        val card =
            LinearLayout(this).apply {
                orientation =
                    LinearLayout.VERTICAL
                setPadding(
                    18,
                    16,
                    18,
                    16
                )
                background = glass()
                elevation = 8f
            }

        card.addView(
            text(
                heading,
                13f,
                cyan,
                Typeface.BOLD
            )
        )

        card.addView(space(6))

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
            typeface =
                Typeface.create(
                    Typeface.DEFAULT,
                    style
                )
        }
    }

    private fun space(
        height: Int
    ): Space {

        return Space(this).apply {
            layoutParams =
                LinearLayout.LayoutParams(
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
            cornerRadius =
                radius.toFloat()
            setStroke(
                1,
                Color.rgb(
                    55,
                    40,
                    90
                )
            )
        }
    }

    private fun glass():
        GradientDrawable {

        return GradientDrawable(
            GradientDrawable.Orientation.TL_BR,
            intArrayOf(
                Color.rgb(
                    30,
                    21,
                    52
                ),
                Color.rgb(
                    10,
                    10,
                    22
                )
            )
        ).apply {
            cornerRadius = 24f
            setStroke(
                1,
                Color.rgb(
                    75,
                    48,
                    125
                )
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

    private fun toast(
        message: String
    ) {

        Toast.makeText(
            this,
            message,
            Toast.LENGTH_SHORT
        ).show()
    }
}
