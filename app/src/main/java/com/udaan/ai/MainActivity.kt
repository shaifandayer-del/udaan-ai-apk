package com.udaan.ai

import android.graphics.Color
import android.graphics.drawable.GradientDrawable
import android.net.Uri
import android.os.Bundle
import android.os.Handler
import android.os.Looper
import android.view.Gravity
import android.view.View
import android.widget.Button
import android.widget.EditText
import android.widget.ImageView
import android.widget.LinearLayout
import android.widget.ScrollView
import android.widget.TextView
import android.widget.Toast
import androidx.appcompat.app.AppCompatActivity
import okhttp3.Call
import okhttp3.Callback
import okhttp3.MediaType.Companion.toMediaType
import okhttp3.OkHttpClient
import okhttp3.Request
import okhttp3.RequestBody.Companion.toRequestBody
import okhttp3.Response
import org.json.JSONArray
import org.json.JSONObject
import java.io.IOException


class MainActivity : AppCompatActivity() {

    data class UdaanAgent(
        val name: String,
        val description: String,
        val status: String = "UNKNOWN"
    )

    private val client = OkHttpClient()
    private val handler = Handler(Looper.getMainLooper())

    private val baseUrl =
        "https://udaan-ai-apk-1.onrender.com"

    private val apiKey: String
        get() = BuildConfig.UDAAN_FOUNDER_API_KEY

    private val dynamicAgents = mutableListOf<UdaanAgent>()

    private lateinit var root: LinearLayout
    private lateinit var content: LinearLayout
    private lateinit var statusText: TextView

    private var currentPage = "HOME"


    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)

        showHome()
        loadDynamicAgents()
    }


    private fun setupRoot(title: String, subtitle: String = "") {

        root = LinearLayout(this).apply {
            orientation = LinearLayout.VERTICAL
            setBackgroundColor(Color.parseColor("#07070F"))
        }

        val header = LinearLayout(this).apply {
            orientation = LinearLayout.VERTICAL
            setPadding(22, 20, 22, 14)
        }

        val logo = ImageView(this).apply {
            setImageResource(R.drawable.udaan_logo)
            scaleType = ImageView.ScaleType.CENTER_INSIDE
        }

        header.addView(
            logo,
            LinearLayout.LayoutParams(
                -1,
                95
            )
        )

        val titleView = TextView(this).apply {
            text = title
            textSize = 25f
            setTextColor(Color.WHITE)
            gravity = Gravity.CENTER_HORIZONTAL
        }

        header.addView(
            titleView,
            LinearLayout.LayoutParams(
                -1,
                -2
            )
        )

        if (subtitle.isNotEmpty()) {

            val subtitleView = TextView(this).apply {
                text = subtitle
                textSize = 13f
                setTextColor(Color.parseColor("#A9A9C2"))
                gravity = Gravity.CENTER_HORIZONTAL
                setPadding(0, 5, 0, 0)
            }

            header.addView(
                subtitleView,
                LinearLayout.LayoutParams(
                    -1,
                    -2
                )
            )
        }

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
            setPadding(16, 8, 16, 90)
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

        addBottomNavigation()

        setContentView(root)
    }


    private fun addBottomNavigation() {

        val navigation = LinearLayout(this).apply {
            orientation = LinearLayout.HORIZONTAL
            gravity = Gravity.CENTER
            setPadding(8, 8, 8, 8)
            setBackgroundColor(Color.parseColor("#10101C"))
        }

        addNavigationButton(
            navigation,
            "⌂",
            "Home"
        ) {
            showHome()
        }

        addNavigationButton(
            navigation,
            "◈",
            "Agents"
        ) {
            showAgents()
        }

        addNavigationButton(
            navigation,
            "✓",
            "Tasks"
        ) {
            showTasks()
        }

        addNavigationButton(
            navigation,
            "▣",
            "Content"
        ) {
            showContent()
        }

        addNavigationButton(
            navigation,
            "⋮",
            "More"
        ) {
            showMore()
        }

        root.addView(
            navigation,
            LinearLayout.LayoutParams(
                -1,
                70
            )
        )
    }


    private fun addNavigationButton(
        parent: LinearLayout,
        icon: String,
        title: String,
        action: () -> Unit
    ) {

        val button = Button(this).apply {
            text = "$icon\n$title"
            textSize = 10f
            setTextColor(Color.WHITE)
            setBackgroundColor(Color.TRANSPARENT)
            setOnClickListener {
                action()
            }
        }

        parent.addView(
            button,
            LinearLayout.LayoutParams(
                0,
                -1,
                1f
            )
        )
    }


    private fun showHome() {

        currentPage = "HOME"

        setupRoot(
            "UDAAN AI",
            "AI COMMAND CENTER"
        )

        val greeting = TextView(this).apply {
            text = "Good Morning, Founder!"
            textSize = 20f
            setTextColor(Color.WHITE)
            gravity = Gravity.CENTER
            setPadding(0, 8, 0, 4)
        }

        content.addView(greeting)

        val subtitle = TextView(this).apply {
            text = "What shall we create today?"
            textSize = 13f
            setTextColor(Color.parseColor("#A9A9C2"))
            gravity = Gravity.CENTER
            setPadding(0, 0, 0, 16)
        }

        content.addView(subtitle)

        addCommandBox()

        addSection("AI COMMAND CENTER")

        addInfoCard(
            "Main AI / Orchestrator",
            "Your central AI that understands commands and routes work."
        ) {
            showCommandCenter()
        }

        addSection("CORE MODULES")

        moduleButton(
            "AI Agents",
            "Research, Content, Video, YouTube, Social, Analytics and more."
        ) {
            showAgents()
        }

        moduleButton(
            "Video Studio",
            "Create, render and manage AI-generated videos."
        ) {
            showVideoStudio()
        }

        moduleButton(
            "Content Studio",
            "Scripts, posts, captions, titles and creative content."
        ) {
            showContent()
        }

        moduleButton(
            "Task Center",
            "Track pending, running and completed tasks."
        ) {
            showTasks()
        }

        moduleButton(
            "Founder Approval",
            "Review and approve high-impact AI actions."
        ) {
            showApprovals()
        }

        moduleButton(
            "Analytics",
            "Monitor UDAAN AI performance and content analytics."
        ) {
            showAnalytics()
        }

        addSection("QUICK ACTIONS")

        moduleButton(
            "YouTube Video",
            "Research → Script → Video → Approval → Upload."
        ) {
            setCommandAndExecute("Create a YouTube video")
        }

        moduleButton(
            "Social Post",
            "Create an Instagram/social media post."
        ) {
            setCommandAndExecute("Create a social media post")
        }

        moduleButton(
            "App Builder",
            "Build software through Developer AI."
        ) {
            setCommandAndExecute("Build a test app")
        }

        addStatus()
    }


    private fun addCommandBox() {

        val card = glass()

        val title = TextView(this).apply {
            text = "Tell UDAAN what to do..."
            textSize = 17f
            setTextColor(Color.WHITE)
        }

        card.addView(title)

        val input = EditText(this).apply {
            hint = "e.g. Create a YouTube video on AI"
            setHintTextColor(Color.parseColor("#77778F"))
            setTextColor(Color.WHITE)
            textSize = 14f
            setPadding(16, 16, 16, 16)
            background = gradient(
                "#151526",
                "#151526",
                18
            )
        }

        card.addView(
            input,
            LinearLayout.LayoutParams(
                -1,
                120
            ).apply {
                topMargin = 12
            }
        )

        val button = Button(this).apply {
            text = "⚡ EXECUTE COMMAND"
            textSize = 13f
            setTextColor(Color.WHITE)
            background = gradient(
                "#8A4DFF",
                "#5D32B8",
                18
            )

            setOnClickListener {
                val command = input.text.toString().trim()

                if (command.isEmpty()) {
                    Toast.makeText(
                        this@MainActivity,
                        "Command enter karo.",
                        Toast.LENGTH_SHORT
                    ).show()
                    return@setOnClickListener
                }

                sendCommand(command)
            }
        }

        card.addView(
            button,
            LinearLayout.LayoutParams(
                -1,
                58
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
                bottomMargin = 16
            }
        )
    }


    private fun showCommandCenter() {

        currentPage = "COMMAND"

        setupRoot(
            "AI Command Center",
            "Tell UDAAN what you want to do..."
        )

        addCommandBox()

        addSection("QUICK ACTIONS")

        moduleButton(
            "YouTube Video",
            "Create a complete video workflow."
        ) {
            setCommandAndExecute(
                "Create a YouTube video"
            )
        }

        moduleButton(
            "Social Post",
            "Create social media content."
        ) {
            setCommandAndExecute(
                "Create a social media post"
            )
        }

        moduleButton(
            "Blog Article",
            "Research and create a complete article."
        ) {
            setCommandAndExecute(
                "Create a blog article"
            )
        }

        moduleButton(
            "Create Image",
            "Generate creative direction and graphics."
        ) {
            setCommandAndExecute(
                "Create an image concept"
            )
        }

        addStatus()
    }


    private fun showAgents() {

        currentPage = "AGENTS"

        setupRoot(
            "AI Agents",
            "UDAAN AI Agent Network"
        )

        if (dynamicAgents.isEmpty()) {

            addInfoCard(
                "Loading Agents",
                "Backend se agents load ho rahe hain..."
            )

            loadDynamicAgents()

            return
        }

        dynamicAgents.forEach { agent ->

            moduleButton(
                agent.name,
                "${agent.description}\nStatus: ${agent.status}"
            ) {
                openAgent(agent)
            }
        }

        addSection("CORE AI")

        moduleButton(
            "Main AI / Orchestrator",
            "Command planning, routing and complete workflow."
        ) {
            setCommandAndExecute(
                "Plan and execute my command"
            )
        }
    }


    private fun openAgent(agent: UdaanAgent) {

        currentPage = "AGENT"

        setupRoot(
            agent.name,
            agent.description
        )

        addInfoCard(
            "Agent Status",
            agent.status
        )

        val input = EditText(this).apply {
            hint = "Is agent ko command do..."
            setHintTextColor(Color.parseColor("#77778F"))
            setTextColor(Color.WHITE)
            setPadding(16, 16, 16, 16)
            background = gradient(
                "#151526",
                "#151526",
                18
            )
        }

        content.addView(
            input,
            LinearLayout.LayoutParams(
                -1,
                120
            ).apply {
                bottomMargin = 12
            }
        )

        val button = Button(this).apply {
            text = "RUN ${agent.name.uppercase()}"
            setTextColor(Color.WHITE)
            background = gradient(
                "#8A4DFF",
                "#5D32B8",
                18
            )

            setOnClickListener {

                val command = input.text.toString().trim()

                if (command.isEmpty()) {
                    Toast.makeText(
                        this@MainActivity,
                        "Command enter karo.",
                        Toast.LENGTH_SHORT
                    ).show()
                    return@setOnClickListener
                }

                sendCommand(
                    "${agent.name}: $command"
                )
            }
        }

        content.addView(
            button,
            LinearLayout.LayoutParams(
                -1,
                58
            )
        )

        addStatus()
    }


    private fun showTasks() {

        currentPage = "TASKS"

        setupRoot(
            "Task Center",
            "Track UDAAN AI execution"
        )

        addSection("TASK STATUS")

        moduleButton(
            "All Tasks",
            "All UDAAN AI tasks."
        ) {
            loadTasks()
        }

        moduleButton(
            "Pending",
            "Tasks waiting for approval."
        ) {
            loadApprovals()
        }

        moduleButton(
            "In Progress",
            "Currently running tasks."
        ) {
            loadBackendStatus()
        }

        moduleButton(
            "Completed",
            "Completed execution results."
        ) {
            loadBackendStatus()
        }

        addStatus()
    }


    private fun showContent() {

        currentPage = "CONTENT"

        setupRoot(
            "Content Center",
            "Manage your AI-generated content"
        )

        addSection("CONTENT")

        moduleButton(
            "All Content",
            "All generated content."
        ) {
            showResult(
                "Content Center",
                "Generated content backend se connected hai."
            )
        }

        moduleButton(
            "Videos",
            "Generated videos and final MP4 files."
        ) {
            showVideoStudio()
        }

        moduleButton(
            "Posts",
            "Instagram and social posts."
        ) {
            setCommandAndExecute(
                "Create a social media post"
            )
        }

        moduleButton(
            "Articles",
            "Research-based articles and blogs."
        ) {
            setCommandAndExecute(
                "Create a blog article"
            )
        }

        moduleButton(
            "Final Video",
            "Review final video before Founder Approval."
        ) {
            showFinalVideo()
        }
    }


    private fun showVideoStudio() {

        currentPage = "VIDEO"

        setupRoot(
            "Video Studio",
            "AI Video Production Pipeline"
        )

        addSection("VIDEO CREATION")

        moduleButton(
            "Create Video",
            "Research → Content → Creative → Video → Render."
        ) {
            setCommandAndExecute(
                "Create a complete video"
            )
        }

        moduleButton(
            "Text to Video",
            "Create a video from a text command."
        ) {
            setCommandAndExecute(
                "Create a video from this text"
            )
        }

        moduleButton(
            "Video Editor",
            "Prepare video for final rendering."
        ) {
            showResult(
                "Video Editor",
                "Video editing pipeline ready."
            )
        }

        moduleButton(
            "Voiceover",
            "Voiceover stage of the video pipeline."
        ) {
            showResult(
                "Voiceover",
                "Voiceover pipeline ready."
            )
        }

        moduleButton(
            "Templates",
            "Use UDAAN AI video templates."
        ) {
            showResult(
                "Templates",
                "Video templates ready."
            )
        }

        addSection("FINAL VIDEO")

        moduleButton(
            "Final Video",
            "Preview and approve final output."
        ) {
            showFinalVideo()
        }
    }


    private fun showFinalVideo() {

        currentPage = "FINAL_VIDEO"

        setupRoot(
            "Final Video",
            "Founder Review"
        )

        addInfoCard(
            "Final Video",
            "Rendered video approval workflow."
        )

        moduleButton(
            "Approve Video",
            "Approve video for publishing."
        ) {
            showApprovals()
        }

        moduleButton(
            "Reject Video",
            "Reject and send back for revision."
        ) {
            showResult(
                "Video Rejected",
                "Video revision requested."
            )
        }

        moduleButton(
            "YouTube Upload",
            "Upload approved video to YouTube."
        ) {
            showYouTube()
        }

        moduleButton(
            "Instagram Publish",
            "Publish approved video to Instagram."
        ) {
            showInstagram()
        }
    }


    private fun showMore() {

        currentPage = "MORE"

        setupRoot(
            "More",
            "UDAAN AI Control Center"
        )

        moduleButton(
            "Video Studio",
            "AI video creation and rendering."
        ) {
            showVideoStudio()
        }

        moduleButton(
            "YouTube",
            "YouTube connection, upload and channel."
        ) {
            showYouTube()
        }

        moduleButton(
            "Instagram",
            "Instagram connection and publishing."
        ) {
            showInstagram()
        }

        moduleButton(
            "App Builder",
            "Developer AI software building."
        ) {
            setCommandAndExecute(
                "Build a test app"
            )
        }

        moduleButton(
            "Analytics",
            "Performance and content analytics."
        ) {
            showAnalytics()
        }

        moduleButton(
            "Founder Approval",
            "Approve or reject AI actions."
        ) {
            showApprovals()
        }

        moduleButton(
            "Notifications",
            "UDAAN AI notifications."
        ) {
            showNotifications()
        }

        moduleButton(
            "Settings",
            "System and connection settings."
        ) {
            showSettings()
        }

        moduleButton(
            "System",
            "Backend and AI system status."
        ) {
            showSystem()
        }
    }


    private fun showYouTube() {

        currentPage = "YOUTUBE"

        setupRoot(
            "YouTube AI",
            "YouTube Connection Center"
        )

        addInfoCard(
            "YouTube",
            "OAuth 2.0 + YouTube Data API"
        )

        moduleButton(
            "Channel Stats",
            "Load YouTube channel information."
        ) {
            loadBackendStatus()
        }

        moduleButton(
            "Upload Video",
            "Upload approved final video."
        ) {
            setCommandAndExecute(
                "Upload approved video to YouTube"
            )
        }

        moduleButton(
            "Recent Uploads",
            "View recent YouTube uploads."
        ) {
            showResult(
                "YouTube",
                "Recent upload data is handled by the YouTube integration."
            )
        }
    }


    private fun showInstagram() {

        currentPage = "INSTAGRAM"

        setupRoot(
            "Instagram AI",
            "Instagram Publishing Center"
        )

        addInfoCard(
            "Instagram",
            "Instagram Graph API + Professional Account"
        )

        moduleButton(
            "Connection",
            "Check Instagram connection."
        ) {
            setCommandAndExecute(
                "Check Instagram connection"
            )
        }

        moduleButton(
            "Publish Reel",
            "Publish approved video as Reel."
        ) {
            setCommandAndExecute(
                "Publish approved video to Instagram"
            )
        }

        moduleButton(
            "Create Post",
            "Create an Instagram post."
        ) {
            setCommandAndExecute(
                "Create an Instagram post"
            )
        }
    }


    private fun showAnalytics() {

        currentPage = "ANALYTICS"

        setupRoot(
            "Analytics AI",
            "UDAAN Performance Center"
        )

        addInfoCard(
            "Analytics",
            "Monitor tasks, content, publishing and AI performance."
        )

        moduleButton(
            "System Analytics",
            "Check backend status."
        ) {
            loadBackendStatus()
        }

        moduleButton(
            "Content Analytics",
            "Analyze generated content."
        ) {
            setCommandAndExecute(
                "Show content analytics"
            )
        }

        moduleButton(
            "Marketing Analytics",
            "Analyze marketing performance."
        ) {
            setCommandAndExecute(
                "Show marketing analytics"
            )
        }
    }


    private fun showApprovals() {

        currentPage = "APPROVAL"

        setupRoot(
            "Founder Approval",
            "Nothing publishes without Founder approval"
        )

        addInfoCard(
            "Approval Engine",
            "High-impact actions require Founder approval."
        )

        moduleButton(
            "Pending Approvals",
            "View current approval queue."
        ) {
            loadApprovals()
        }

        moduleButton(
            "Approve",
            "Approve selected action."
        ) {
            showResult(
                "Approval",
                "Select an approval from the backend queue."
            )
        }

        moduleButton(
            "Reject",
            "Reject selected action."
        ) {
            showResult(
                "Rejection",
                "Select an approval from the backend queue."
            )
        }
    }


    private fun showNotifications() {

        currentPage = "NOTIFICATIONS"

        setupRoot(
            "Notifications",
            "UDAAN AI Updates"
        )

        addInfoCard(
            "Founder Notifications",
            "Approval, video, upload and system events appear here."
        )

        loadBackendStatus()
    }


    private fun showSettings() {

        currentPage = "SETTINGS"

        setupRoot(
            "Settings",
            "UDAAN AI Configuration"
        )

        addInfoCard(
            "Backend",
            baseUrl
        )

        addInfoCard(
            "Security",
            if (apiKey.isNotEmpty()) {
                "Founder API Key configured"
            } else {
                "Founder API Key missing"
            }
        )

        moduleButton(
            "Test Backend",
            "Check UDAAN backend connection."
        ) {
            loadBackendStatus()
        }
    }


    private fun showSystem() {

        currentPage = "SYSTEM"

        setupRoot(
            "System",
            "UDAAN AI System Status"
        )

        addInfoCard(
            "Backend",
            "Checking..."
        )

        loadBackendStatus()

        moduleButton(
            "Reload Agents",
            "Refresh dynamic AI agents."
        ) {
            loadDynamicAgents()
        }
    }


    private fun addStatus() {

        statusText = TextView(this).apply {
            text = "● UDAAN AI READY"
            textSize = 12f
            setTextColor(Color.parseColor("#00E676"))
            setPadding(4, 18, 4, 8)
        }

        content.addView(statusText)
    }


    private fun addSection(title: String) {

        val text = TextView(this).apply {
            this.text = title
            textSize = 14f
            setTextColor(Color.parseColor("#00D9FF"))
            setPadding(4, 18, 4, 10)
        }

        content.addView(text)
    }


    private fun moduleButton(
        title: String,
        description: String,
        action: () -> Unit
    ) {

        val card = glass()

        val titleView = TextView(this).apply {
            text = title
            textSize = 17f
            setTextColor(Color.WHITE)
        }

        card.addView(titleView)

        val descriptionView = TextView(this).apply {
            text = description
            textSize = 12f
            setTextColor(Color.parseColor("#A9A9C2"))
            setPadding(0, 6, 0, 10)
        }

        card.addView(descriptionView)

        val button = Button(this).apply {
            text = "OPEN"
            textSize = 11f
            setTextColor(Color.WHITE)
            background = gradient(
                "#8A4DFF",
                "#5D32B8",
                16
            )

            setOnClickListener {
                action()
            }
        }

        card.addView(
            button,
            LinearLayout.LayoutParams(
                -1,
                50
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


    private fun addInfoCard(
        title: String,
        message: String,
        action: (() -> Unit)? = null
    ) {

        val card = glass()

        val titleView = TextView(this).apply {
            text = title
            textSize = 17f
            setTextColor(Color.WHITE)
        }

        card.addView(titleView)

        val messageView = TextView(this).apply {
            text = message
            textSize = 12f
            setTextColor(Color.parseColor("#A9A9C2"))
            setPadding(0, 7, 0, 0)
        }

        card.addView(messageView)

        if (action != null) {

            card.setOnClickListener {
                action()
            }
        }

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


    private fun glass(): LinearLayout {

        return LinearLayout(this).apply {
            orientation = LinearLayout.VERTICAL
            setPadding(16, 16, 16, 16)
            background = gradient(
                "#151526",
                "#10101C",
                22
            )
        }
    }


    private fun gradient(
        start: String,
        end: String,
        radius: Int
    ): GradientDrawable {

        return GradientDrawable(
            GradientDrawable.Orientation.TL_BR,
            intArrayOf(
                Color.parseColor(start),
                Color.parseColor(end)
            )
        ).apply {
            cornerRadius = radius.toFloat()
            setStroke(
                1,
                Color.parseColor("#29294A")
            )
        }
    }


    private fun setCommandAndExecute(command: String) {
        sendCommand(command)
    }


    private fun sendCommand(command: String) {

        if (apiKey.isEmpty()) {
            showResult(
                "UDAAN Security",
                "Founder API Key configured nahi hai."
            )
            return
        }

        updateStatus("● PROCESSING...", "#FFB300")

        val json = JSONObject().apply {
            put("command", command)
        }

        val body = json.toString()
            .toRequestBody(
                "application/json".toMediaType()
            )

        val request = Request.Builder()
            .url("$baseUrl/command")
            .addHeader(
                "X-Udaan-API-Key",
                apiKey
            )
            .post(body)
            .build()

        client.newCall(request)
            .enqueue(object : Callback {

                override fun onFailure(
                    call: Call,
                    e: IOException
                ) {
                    runOnUiThread {
                        updateStatus(
                            "● BACKEND FAILED",
                            "#FF4D6D"
                        )

                        showResult(
                            "Backend Connection Failed",
                            e.message ?: "Network error"
                        )
                    }
                }

                override fun onResponse(
                    call: Call,
                    response: Response
                ) {

                    val result =
                        response.body?.string() ?: ""

                    runOnUiThread {

                        if (response.isSuccessful) {

                            updateStatus(
                                "● COMMAND COMPLETED",
                                "#00E676"
                            )

                            showResult(
                                "UDAAN AI Result",
                                prettyJson(result)
                            )

                        } else {

                            updateStatus(
                                "● COMMAND FAILED",
                                "#FF4D6D"
                            )

                            showResult(
                                "UDAAN AI Error",
                                prettyJson(result)
                            )
                        }
                    }
                }
            })
    }


    private fun loadDynamicAgents() {

        if (apiKey.isEmpty()) {
            return
        }

        val request = Request.Builder()
            .url("$baseUrl/agents")
            .addHeader(
                "X-Udaan-API-Key",
                apiKey
            )
            .get()
            .build()

        client.newCall(request)
            .enqueue(object : Callback {

                override fun onFailure(
                    call: Call,
                    e: IOException
                ) {
                    runOnUiThread {
                        updateStatus(
                            "● AGENTS CONNECTION FAILED",
                            "#FF4D6D"
                        )
                    }
                }

                override fun onResponse(
                    call: Call,
                    response: Response
                ) {

                    val body =
                        response.body?.string() ?: ""

                    if (!response.isSuccessful) {
                        return
                    }

                    val agents =
                        parseAgents(body)

                    runOnUiThread {

                        dynamicAgents.clear()
                        dynamicAgents.addAll(agents)

                        if (currentPage == "AGENTS") {
                            showAgents()
                        }

                        updateStatus(
                            "● ${agents.size} AGENTS READY",
                            "#00E676"
                        )
                    }
                }
            })
    }


    private fun parseAgents(
        json: String
    ): List<UdaanAgent> {

        val result = mutableListOf<UdaanAgent>()

        try {

            val rootObject =
                JSONObject(json)

            val array =
                rootObject.optJSONArray("agents")

            if (array != null) {

                for (i in 0 until array.length()) {

                    val item =
                        array.optJSONObject(i)
                            ?: continue

                    result.add(
                        UdaanAgent(
                            name = item.optString(
                                "name",
                                "Unknown Agent"
                            ),
                            description = item.optString(
                                "description",
                                "UDAAN AI Agent"
                            ),
                            status = item.optString(
                                "status",
                                "UNKNOWN"
                            )
                        )
                    )
                }

                return result
            }

            val directArray =
                rootObject.optJSONArray("data")

            if (directArray != null) {

                for (i in 0 until directArray.length()) {

                    val item =
                        directArray.optJSONObject(i)
                            ?: continue

                    result.add(
                        UdaanAgent(
                            name = item.optString(
                                "name",
                                "Unknown Agent"
                            ),
                            description = item.optString(
                                "description",
                                "UDAAN AI Agent"
                            ),
                            status = item.optString(
                                "status",
                                "UNKNOWN"
                            )
                        )
                    )
                }
            }

        } catch (_: Exception) {

            try {

                val array =
                    JSONArray(json)

                for (i in 0 until array.length()) {

                    val item =
                        array.optJSONObject(i)
                            ?: continue

                    result.add(
                        UdaanAgent(
                            name = item.optString(
                                "name",
                                "Unknown Agent"
                            ),
                            description = item.optString(
                                "description",
                                "UDAAN AI Agent"
                            ),
                            status = item.optString(
                                "status",
                                "UNKNOWN"
                            )
                        )
                    )
                }

            } catch (_: Exception) {
            }
        }

        return result
    }


    private fun loadBackendStatus() {

        if (apiKey.isEmpty()) {
            showResult(
                "Backend",
                "Founder API Key configured nahi hai."
            )
            return
        }

        val request = Request.Builder()
            .url("$baseUrl/status")
            .addHeader(
                "X-Udaan-API-Key",
                apiKey
            )
            .get()
            .build()

        client.newCall(request)
            .enqueue(object : Callback {

                override fun onFailure(
                    call: Call,
                    e: IOException
                ) {

                    runOnUiThread {

                        updateStatus(
                            "● BACKEND OFFLINE",
                            "#FF4D6D"
                        )

                        showResult(
                            "Backend Status",
                            e.message ?: "Connection failed"
                        )
                    }
                }

                override fun onResponse(
                    call: Call,
                    response: Response
                ) {

                    val body =
                        response.body?.string()
                            ?: ""

                    runOnUiThread {

                        if (response.isSuccessful) {

                            updateStatus(
                                "● BACKEND ONLINE",
                                "#00E676"
                            )

                            showResult(
                                "Backend Status",
                                prettyJson(body)
                            )

                        } else {

                            updateStatus(
                                "● BACKEND ERROR",
                                "#FF4D6D"
                            )

                            showResult(
                                "Backend Status",
                                prettyJson(body)
                            )
                        }
                    }
                }
            })
    }


    private fun loadTasks() {

        if (apiKey.isEmpty()) {
            return
        }

        val request = Request.Builder()
            .url("$baseUrl/status")
            .addHeader(
                "X-Udaan-API-Key",
                apiKey
            )
            .get()
            .build()

        client.newCall(request)
            .enqueue(object : Callback {

                override fun onFailure(
                    call: Call,
                    e: IOException
                ) {

                    runOnUiThread {
                        showResult(
                            "Tasks",
                            e.message ?: "Task data unavailable"
                        )
                    }
                }

                override fun onResponse(
                    call: Call,
                    response: Response
                ) {

                    val body =
                        response.body?.string()
                            ?: ""

                    runOnUiThread {

                        showResult(
                            "Task Center",
                            prettyJson(body)
                        )
                    }
                }
            })
    }


    private fun loadApprovals() {

        if (apiKey.isEmpty()) {
            showResult(
                "Approvals",
                "Founder API Key configured nahi hai."
            )
            return
        }

        val request = Request.Builder()
            .url("$baseUrl/approvals")
            .addHeader(
                "X-Udaan-API-Key",
                apiKey
            )
            .get()
            .build()

        client.newCall(request)
            .enqueue(object : Callback {

                override fun onFailure(
                    call: Call,
                    e: IOException
                ) {

                    runOnUiThread {
                        showResult(
                            "Founder Approval",
                            e.message
                                ?: "Approval connection failed"
                        )
                    }
                }

                override fun onResponse(
                    call: Call,
                    response: Response
                ) {

                    val body =
                        response.body?.string()
                            ?: ""

                    runOnUiThread {

                        showResult(
                            "Founder Approval Queue",
                            prettyJson(body)
                        )
                    }
                }
            })
    }


    private fun updateStatus(
        message: String,
        color: String
    ) {

        if (!::statusText.isInitialized) {
            return
        }

        statusText.text = message
        statusText.setTextColor(
            Color.parseColor(color)
        )
    }


    private fun showResult(
        title: String,
        message: String
    ) {

        setupRoot(
            title,
            "UDAAN AI"
        )

        val card = glass()

        val text = TextView(this).apply {
            this.text = message
            textSize = 13f
            setTextColor(Color.WHITE)
            setPadding(4, 4, 4, 4)
        }

        card.addView(text)

        content.addView(
            card,
            LinearLayout.LayoutParams(
                -1,
                -2
            )
        )

        addInfoCard(
            "Back to Home",
            "Return to UDAAN AI Command Center."
        ) {
            showHome()
        }
    }


    private fun prettyJson(
        value: String
    ): String {

        if (value.isBlank()) {
            return "Empty response."
        }

        return try {

            val trimmed = value.trim()

            when {
                trimmed.startsWith("{") ->
                    JSONObject(trimmed)
                        .toString(2)

                trimmed.startsWith("[") ->
                    JSONArray(trimmed)
                        .toString(2)

                else ->
                    value
            }

        } catch (_: Exception) {
            value
        }
    }


    override fun onDestroy() {
        handler.removeCallbacksAndMessages(null)
        client.dispatcher.cancelAll()
        super.onDestroy()
    }
}
```0
