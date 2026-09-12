Step 243 — MainActivity.kt

package com.udaan.ai

import android.content.Context
import android.graphics.*
import android.graphics.drawable.GradientDrawable
import android.os.Bundle
import android.view.Gravity
import android.view.View
import android.widget.*
import androidx.appcompat.app.AppCompatActivity
import okhttp3.*
import okhttp3.MediaType.Companion.toMediaType
import okhttp3.RequestBody.Companion.toRequestBody
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
    private val baseUrl = "https://udaan-ai-apk-1.onrender.com"

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

    private fun setupRoot(
        title: String,
        subtitle: String = ""
    ) {
        root = LinearLayout(this).apply {
            orientation = LinearLayout.VERTICAL
            setBackgroundColor(Color.parseColor("#030711"))
        }

        val header = LinearLayout(this).apply {
            orientation = LinearLayout.HORIZONTAL
            gravity = Gravity.CENTER_VERTICAL
            setPadding(18, 12, 18, 8)
        }

        val logo = ImageView(this).apply {
            setImageResource(R.drawable.udaan_logo)
            scaleType = ImageView.ScaleType.CENTER_INSIDE
        }

        header.addView(
            logo,
            LinearLayout.LayoutParams(58, 58)
        )

        val headerText = LinearLayout(this).apply {
            orientation = LinearLayout.VERTICAL
            setPadding(10, 0, 0, 0)
        }

        val brand = TextView(this).apply {
            text = "UDAAN AI"
            textSize = 18f
            setTextColor(Color.WHITE)
            typeface = Typeface.DEFAULT_BOLD
        }

        headerText.addView(brand)

        val sub = TextView(this).apply {
            text = if (subtitle.isEmpty()) "Your Personal AI Command Center" else subtitle
            textSize = 10f
            setTextColor(Color.parseColor("#8FA7C7"))
        }

        headerText.addView(sub)

        header.addView(
            headerText,
            LinearLayout.LayoutParams(
                0,
                -2,
                1f
            )
        )

        val online = TextView(this).apply {
            text = "● Online"
            textSize = 10f
            setTextColor(Color.parseColor("#00F5A0"))
            gravity = Gravity.CENTER
        }

        header.addView(
            online,
            LinearLayout.LayoutParams(
                -2,
                -2
            )
        )

        root.addView(
            header,
            LinearLayout.LayoutParams(-1, 78)
        )

        val titleBar = LinearLayout(this).apply {
            orientation = LinearLayout.VERTICAL
            setPadding(18, 4, 18, 10)
        }

        val titleView = TextView(this).apply {
            text = title
            textSize = 24f
            setTextColor(Color.WHITE)
            typeface = Typeface.DEFAULT_BOLD
        }

        titleBar.addView(titleView)

        root.addView(
            titleBar,
            LinearLayout.LayoutParams(-1, -2)
        )

        val scroll = ScrollView(this).apply {
            isFillViewport = true
            overScrollMode = View.OVER_SCROLL_NEVER
        }

        content = LinearLayout(this).apply {
            orientation = LinearLayout.VERTICAL
            setPadding(14, 4, 14, 18)
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

    private fun showHome() {
        currentPage = "HOME"

        setupRoot(
            "Home",
            "Your Personal AI Command Center"
        )

        addHeroCard()

        addSection("UDAAN AI CORE")

        addInfoCard(
            "●  UDAAN AI CORE     ONLINE",
            "All systems operational • Founder mode active"
        )

        addSection("AI COMMAND CENTER")

        addCommandBox()

        addSection("AI MODULES")

        val grid = LinearLayout(this).apply {
            orientation = LinearLayout.VERTICAL
        }

        addGridRow(
            grid,
            listOf(
                Triple(
                    "AI AGENTS",
                    "10 Agents",
                    "◈"
                ),
                Triple(
                    "TASKS",
                    "3 Active",
                    "✓"
                ),
                Triple(
                    "CONTENT",
                    "Create",
                    "✎"
                )
            ),
            listOf(
                { showAgents() },
                { showTasks() },
                { showContent() }
            )
        )

        addGridRow(
            grid,
            listOf(
                Triple(
                    "VIDEO STUDIO",
                    "Create Videos",
                    "▶"
                ),
                Triple(
                    "YOUTUBE",
                    "Manage Channel",
                    "▶"
                ),
                Triple(
                    "SOCIAL MEDIA",
                    "Auto Post",
                    "◎"
                )
            ),
            listOf(
                { showVideoStudio() },
                { showYouTube() },
                { showInstagram() }
            )
        )

        addGridRow(
            grid,
            listOf(
                Triple(
                    "ANALYTICS",
                    "View Reports",
                    "▥"
                ),
                Triple(
                    "MARKETING",
                    "Grow Brand",
                    "⚑"
                ),
                Triple(
                    "DEVELOPER",
                    "Build Apps",
                    "</>"
                )
            ),
            listOf(
                { showAnalytics() },
                {
                    setCommandAndExecute(
                        "Show marketing analytics"
                    )
                },
                {
                    setCommandAndExecute(
                        "Build a test app"
                    )
                }
            )
        )

        content.addView(
            grid,
            LinearLayout.LayoutParams(-1, -2)
        )

        addSection("FOUNDER CONTROL")

        moduleButton(
            "Founder Approval",
            "Nothing publishes or deploys without your approval."
        ) {
            showApprovals()
        }

        addAgentBottomBar()
        addStatus()
    }

    private fun addHeroCard() {
        val hero = FrameLayout(this).apply {
            background = gradient(
                "#06142C",
                "#030914",
                26
            )
            setPadding(18, 12, 18, 12)
        }

        val glow = GlowOrbView(this)

        hero.addView(
            glow,
            FrameLayout.LayoutParams(
                250,
                180,
                Gravity.END or Gravity.CENTER_VERTICAL
            )
        )

        val textBox = LinearLayout(this).apply {
            orientation = LinearLayout.VERTICAL
            gravity = Gravity.CENTER_VERTICAL
        }

        val welcome = TextView(this).apply {
            text = "Welcome Back, Founder"
            textSize = 21f
            setTextColor(Color.WHITE)
            typeface = Typeface.DEFAULT_BOLD
        }

        textBox.addView(welcome)

        val message = TextView(this).apply {
            text = "Turn your ideas into reality with the power of AI."
            textSize = 12f
            setTextColor(Color.parseColor("#A9B8D0"))
            setPadding(0, 6, 0, 10)
        }

        textBox.addView(message)

        val command = Button(this).apply {
            text = "🚀  Give Command"
            textSize = 12f
            setTextColor(Color.WHITE)
            background = gradient(
                "#087CFF",
                "#5140FF",
                20
            )

            setOnClickListener {
                showCommandCenter()
            }
        }

        textBox.addView(
            command,
            LinearLayout.LayoutParams(
                170,
                48
            )
        )

        hero.addView(
            textBox,
            FrameLayout.LayoutParams(
                0,
                -1,
                Gravity.START,
                1f
            )
        )

        content.addView(
            hero,
            LinearLayout.LayoutParams(
                -1,
                190
            ).apply {
                bottomMargin = 14
            }
        )
    }

    private fun addGridRow(
        parent: LinearLayout,
        items: List<Triple<String, String, String>>,
        actions: List<() -> Unit>
    ) {
        val row = LinearLayout(this).apply {
            orientation = LinearLayout.HORIZONTAL
            gravity = Gravity.CENTER
        }

        items.forEachIndexed { index, item ->

            val card = LinearLayout(this).apply {
                orientation = LinearLayout.VERTICAL
                gravity = Gravity.CENTER
                setPadding(8, 12, 8, 10)
                background = gradient(
                    "#08182F",
                    "#07101F",
                    18
                )
                setOnClickListener {
                    actions[index]()
                }
            }

            val icon = TextView(this).apply {
                text = item.third
                textSize = 25f
                setTextColor(Color.parseColor("#00CFFF"))
                gravity = Gravity.CENTER
            }

            card.addView(icon)

            val title = TextView(this).apply {
                text = item.first
                textSize = 10f
                setTextColor(Color.WHITE)
                gravity = Gravity.CENTER
                typeface = Typeface.DEFAULT_BOLD
                setPadding(0, 6, 0, 2)
            }

            card.addView(title)

            val desc = TextView(this).apply {
                text = item.second
                textSize = 9f
                setTextColor(Color.parseColor("#7F9BBC"))
                gravity = Gravity.CENTER
            }

            card.addView(desc)

            row.addView(
                card,
                LinearLayout.LayoutParams(
                    0,
                    112,
                    1f
                ).apply {
                    setMargins(4, 4, 4, 4)
                }
            )
        }

        parent.addView(
            row,
            LinearLayout.LayoutParams(
                -1,
                120
            )
        )
    }

    private fun addAgentBottomBar() {
        if (dynamicAgents.isEmpty()) return

        val wrapper = LinearLayout(this).apply {
            orientation = LinearLayout.VERTICAL
            background = gradient(
                "#071329",
                "#040A16",
                18
            )
            setPadding(8, 8, 8, 8)
        }

        val title = TextView(this).apply {
            text = "AI AGENTS"
            textSize = 11f
            setTextColor(Color.parseColor("#00D9FF"))
            gravity = Gravity.CENTER
            typeface = Typeface.DEFAULT_BOLD
            setPadding(0, 2, 0, 6)
        }

        wrapper.addView(title)

        val scroll = HorizontalScrollView(this).apply {
            isHorizontalScrollBarEnabled = false
            overScrollMode = View.OVER_SCROLL_NEVER
        }

        val row = LinearLayout(this).apply {
            orientation = LinearLayout.HORIZONTAL
        }

        dynamicAgents.forEach { agent ->

            val button = TextView(this).apply {
                text = agent.name
                textSize = 10f
                setTextColor(Color.WHITE)
                gravity = Gravity.CENTER
                setPadding(15, 12, 15, 12)
                background = gradient(
                    "#0B1D3A",
                    "#071326",
                    16
                )

                setOnClickListener {
                    openAgent(agent)
                }
            }

            row.addView(
                button,
                LinearLayout.LayoutParams(
                    -2,
                    48
                ).apply {
                    setMargins(4, 0, 4, 0)
                }
            )
        }

        scroll.addView(row)

        wrapper.addView(
            scroll,
            LinearLayout.LayoutParams(-1, 54)
        )

        content.addView(
            wrapper,
            LinearLayout.LayoutParams(
                -1,
                -2
            ).apply {
                topMargin = 10
                bottomMargin = 12
            }
        )
    }

    private fun addCommandBox() {
        val card = glass()

        val title = TextView(this).apply {
            text = "Tell UDAAN what to do..."
            textSize = 16f
            setTextColor(Color.WHITE)
            typeface = Typeface.DEFAULT_BOLD
        }

        card.addView(title)

        val input = EditText(this).apply {
            hint = "e.g. Create a YouTube video on AI"
            setHintTextColor(Color.parseColor("#627895"))
            setTextColor(Color.WHITE)
            textSize = 13f
            setPadding(14, 10, 14, 10)
            background = gradient(
                "#07142A",
                "#050B16",
                16
            )
        }

        card.addView(
            input,
            LinearLayout.LayoutParams(
                -1,
                82
            ).apply {
                topMargin = 10
            }
        )

        val button = Button(this).apply {
            text = "⚡  EXECUTE COMMAND"
            textSize = 12f
            setTextColor(Color.WHITE)
            background = gradient(
                "#087CFF",
                "#6037FF",
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
                } else {
                    sendCommand(command)
                }
            }
        }

        card.addView(
            button,
            LinearLayout.LayoutParams(
                -1,
                52
            ).apply {
                topMargin = 10
            }
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

    private fun showCommandCenter() {
        currentPage = "COMMAND"

        setupRoot(
            "AI Command Center",
            "Tell UDAAN what you want to do"
        )

        addCommandBox()

        addSection("QUICK ACTIONS")

        moduleButton(
            "YouTube Video",
            "Research → Script → Video → Approval → Upload"
        ) {
            setCommandAndExecute(
                "Create a YouTube video"
            )
        }

        moduleButton(
            "Social Post",
            "Create social media content"
        ) {
            setCommandAndExecute(
                "Create a social media post"
            )
        }

        moduleButton(
            "Blog Article",
            "Research and create an article"
        ) {
            setCommandAndExecute(
                "Create a blog article"
            )
        }

        moduleButton(
            "Create Image",
            "Generate an image concept"
        ) {
            setCommandAndExecute(
                "Create an image concept"
            )
        }

        addAgentBottomBar()
        addStatus()
    }

    private fun showAgents() {
        currentPage = "AGENTS"

        setupRoot(
            "AI Agents",
            "Your 10 Specialized AI Agents"
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
                "${agent.description}\n● ${agent.status}"
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

        addAgentBottomBar()
        addStatus()
    }

    private fun openAgent(agent: UdaanAgent) {
        currentPage = "AGENT"

        setupRoot(
            agent.name,
            agent.description
        )

        addInfoCard(
            "● ${agent.status}",
            "Agent ready for Founder command."
        )

        val input = EditText(this).apply {
            hint = "Is agent ko command do..."
            setHintTextColor(Color.parseColor("#627895"))
            setTextColor(Color.WHITE)
            setPadding(14, 12, 14, 12)
            background = gradient(
                "#07142A",
                "#050B16",
                16
            )
        }

        content.addView(
            input,
            LinearLayout.LayoutParams(
                -1,
                100
            ).apply {
                bottomMargin = 12
            }
        )

        val button = Button(this).apply {
            text = "RUN ${agent.name.uppercase()}"
            setTextColor(Color.WHITE)
            background = gradient(
                "#087CFF",
                "#6037FF",
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
                } else {
                    sendCommand(
                        "${agent.name}: $command"
                    )
                }
            }
        }

        content.addView(
            button,
            LinearLayout.LayoutParams(-1, 54)
        )

        addAgentBottomBar()
        addStatus()
    }

    private fun showTasks() {
        currentPage = "TASKS"

        setupRoot(
            "Tasks",
            "Manage your AI tasks"
        )

        addSection("ACTIVE TASKS")

        moduleButton(
            "All Tasks",
            "View all UDAAN AI tasks."
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

        addAgentBottomBar()
        addStatus()
    }

    private fun showContent() {
        currentPage = "CONTENT"

        setupRoot(
            "Content",
            "Create & manage content"
        )

        addGridContentCards()

        addSection("RECENT CONTENT")

        addInfoCard(
            "AI Content",
            "Your generated scripts, posts, articles and videos appear here."
        )

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

        addAgentBottomBar()
        addStatus()
    }

    private fun addGridContentCards() {
        val grid = LinearLayout(this).apply {
            orientation = LinearLayout.VERTICAL
        }

        addGridRow(
            grid,
            listOf(
                Triple("SCRIPT WRITER", "AI scripts", "✎"),
                Triple("CAPTION", "Social captions", "☁"),
                Triple("POST CREATOR", "Social posts", "▣")
            ),
            listOf(
                { setCommandAndExecute("Write a video script") },
                { setCommandAndExecute("Create social media captions") },
                { setCommandAndExecute("Create a social media post") }
            )
        )

        content.addView(grid)
    }

    private fun showVideoStudio() {
        currentPage = "VIDEO"

        setupRoot(
            "Video Studio",
            "Create amazing videos with AI"
        )

        addSection("VIDEO CREATION")

        moduleButton(
            "Create Video",
            "Research → Content → Creative → Video → Render"
        ) {
            setCommandAndExecute(
                "Create a complete video"
            )
        }

        moduleButton(
            "Text to Video",
            "Create a video from text."
        ) {
            setCommandAndExecute(
                "Create a video from this text"
            )
        }

        moduleButton(
            "Video Editor",
            "Edit and enhance video."
        ) {
            showResult(
                "Video Editor",
                "Video editing pipeline ready."
            )
        }

        moduleButton(
            "Voiceover",
            "AI voice generation."
        ) {
            showResult(
                "Voiceover",
                "Voiceover pipeline ready."
            )
        }

        moduleButton(
            "Templates",
            "Ready-to-use video templates."
        ) {
            showResult(
                "Templates",
                "Video templates ready."
            )
        }

        addSection("RECENT VIDEOS")

        addInfoCard(
            "Video Production",
            "Rendered videos and project outputs are managed by UDAAN AI."
        )

        addAgentBottomBar()
        addStatus()
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
            "Send video back for revision."
        ) {
            showResult(
                "Video Rejected",
                "Video revision requested."
            )
        }

        moduleButton(
            "YouTube Upload",
            "Upload approved final video."
        ) {
            showYouTube()
        }

        moduleButton(
            "Instagram Publish",
            "Publish approved video."
        ) {
            showInstagram()
        }

        addAgentBottomBar()
        addStatus()
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
            "YouTube connection and upload."
        ) {
            showYouTube()
        }

        moduleButton(
            "Instagram",
            "Instagram publishing center."
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
            "Performance and growth analytics."
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
            "System configuration."
        ) {
            showSettings()
        }

        moduleButton(
            "System",
            "Backend and AI system status."
        ) {
            showSystem()
        }

        addAgentBottomBar()
        addStatus()
    }

    private fun showYouTube() {
        currentPage = "YOUTUBE"

        setupRoot(
            "YouTube AI",
            "YouTube management & upload"
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
            "View recent uploads."
        ) {
            showResult(
                "YouTube",
                "Recent upload data is handled by the YouTube integration."
            )
        }

        addAgentBottomBar()
        addStatus()
    }

    private fun showInstagram() {
        currentPage = "INSTAGRAM"

        setupRoot(
            "Social Media",
            "Multi-platform automation"
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

        addAgentBottomBar()
        addStatus()
    }

    private fun showAnalytics() {
        currentPage = "ANALYTICS"

        setupRoot(
            "Analytics AI",
            "Performance & growth analytics"
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

        addAgentBottomBar()
        addStatus()
    }

    private fun showApprovals() {
        currentPage = "APPROVAL"

        setupRoot(
            "Founder Approval",
            "Review before execution"
        )

        addInfoCard(
            "Approval Engine",
            "Nothing publishes, uploads or deploys without Founder approval."
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
            loadApprovals()
        }

        moduleButton(
            "Reject",
            "Reject selected action."
        ) {
            loadApprovals()
        }

        addAgentBottomBar()
        addStatus()
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

        addAgentBottomBar()
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

        addAgentBottomBar()
        addStatus()
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

        addAgentBottomBar()
        addStatus()
    }

    private fun addSection(title: String) {
        val text = TextView(this).apply {
            this.text = title
            textSize = 12f
            setTextColor(Color.parseColor("#00D9FF"))
            typeface = Typeface.DEFAULT_BOLD
            setPadding(4, 14, 4, 7)
        }

        content.addView(text)
    }

    private fun addStatus() {
        statusText = TextView(this).apply {
            text = "● UDAAN AI READY"
            textSize = 10f
            setTextColor(Color.parseColor("#00F5A0"))
            setPadding(4, 12, 4, 4)
        }

        content.addView(statusText)
    }

    private fun moduleButton(
        title: String,
        description: String,
        action: () -> Unit
    ) {
        val card = glass()

        val titleView = TextView(this).apply {
            text = title
            textSize = 16f
            setTextColor(Color.WHITE)
            typeface = Typeface.DEFAULT_BOLD
        }

        card.addView(titleView)

        val descriptionView = TextView(this).apply {
            text = description
            textSize = 11f
            setTextColor(Color.parseColor("#8197B6"))
            setPadding(0, 5, 0, 9)
        }

        card.addView(descriptionView)

        val button = Button(this).apply {
            text = "OPEN  ›"
            textSize = 10f
            setTextColor(Color.WHITE)
            background = gradient(
                "#087CFF",
                "#503CFF",
                15
            )

            setOnClickListener {
                action()
            }
        }

        card.addView(
            button,
            LinearLayout.LayoutParams(-1, 46)
        )

        content.addView(
            card,
            LinearLayout.LayoutParams(
                -1,
                -2
            ).apply {
                bottomMargin = 9
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
            textSize = 15f
            setTextColor(Color.WHITE)
            typeface = Typeface.DEFAULT_BOLD
        }

        card.addView(titleView)

        val messageView = TextView(this).apply {
            text = message
            textSize = 11f
            setTextColor(Color.parseColor("#8197B6"))
            setPadding(0, 6, 0, 0)
        }

        card.addView(messageView)

        action?.let {
            card.setOnClickListener {
                it()
            }
        }

        content.addView(
            card,
            LinearLayout.LayoutParams(
                -1,
                -2
            ).apply {
                bottomMargin = 9
            }
        )
    }

    private fun glass(): LinearLayout {
        return LinearLayout(this).apply {
            orientation = LinearLayout.VERTICAL
            setPadding(14, 14, 14, 14)
            background = gradient(
                "#0A1930",
                "#050C18",
                20
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
                Color.parseColor("#123D72")
            )
        }
    }

    private fun addBottomNavigation() {
        val navigation = LinearLayout(this).apply {
            orientation = LinearLayout.HORIZONTAL
            gravity = Gravity.CENTER
            setPadding(4, 4, 4, 4)
            background = gradient(
                "#071329",
                "#030914",
                20
            )
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
            "▣",
            "Tasks"
        ) {
            showTasks()
        }

        addNavigationButton(
            navigation,
            "✎",
            "Content"
        ) {
            showContent()
        }

        addNavigationButton(
            navigation,
            "⋯",
            "More"
        ) {
            showMore()
        }

        root.addView(
            navigation,
            LinearLayout.LayoutParams(
                -1,
                66
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
            textSize = 9f
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

        updateStatus(
            "● PROCESSING...",
            "#FFB300"
        )

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
                                "#00F5A0"
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
        if (apiKey.isEmpty()) return

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

                    if (!response.isSuccessful) return

                    val agents = parseAgents(body)

                    runOnUiThread {
                        dynamicAgents.clear()
                        dynamicAgents.addAll(agents)

                        if (currentPage == "AGENTS") {
                            showAgents()
                        }
                    }
                }
            })
    }

    private fun parseAgents(
        json: String
    ): List<UdaanAgent> {

        val result = mutableListOf<UdaanAgent>()

        try {
            val rootObject = JSONObject(json)

            val array =
                rootObject.optJSONArray("agents")

            if (array != null) {
                for (i in 0 until array.length()) {
                    val item =
                        array.optJSONObject(i)
                            ?: continue

                    result.add(
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
                                "UNKNOWN"
                            )
                        )
                    )
                }

                return result
            }

        } catch (_: Exception) {

            try {
                val array = JSONArray(json)

                for (i in 0 until array.length()) {
                    val item =
                        array.optJSONObject(i)
                            ?: continue

                    result.add(
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
        if (apiKey.isEmpty()) return

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
                        response.body?.string() ?: ""

                    runOnUiThread {
                        if (response.isSuccessful) {
                            updateStatus(
                                "● BACKEND ONLINE",
                                "#00F5A0"
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
        loadBackendStatus()
    }

    private fun loadApprovals() {
        if (apiKey.isEmpty()) return

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
                        response.body?.string() ?: ""

                    runOnUiThread {
                        showResult(
                            "Founder Approval Queue",
                            prettyJson(body)
                        )
                    }
                }
            })
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

        addAgentBottomBar()
    }

    private fun updateStatus(
        message: String,
        color: String
    ) {
        if (!::statusText.isInitialized) return

        statusText.text = message
        statusText.setTextColor(
            Color.parseColor(color)
        )
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
                    JSONObject(trimmed).toString(2)

                trimmed.startsWith("[") ->
                    JSONArray(trimmed).toString(2)

                else ->
                    value
            }

        } catch (_: Exception) {
            value
        }
    }

    override fun onDestroy() {
        client.dispatcher.cancelAll()
        super.onDestroy()
    }
}

private class GlowOrbView(
    context: Context
) : View(context) {

    private val paint = Paint(Paint.ANTI_ALIAS_FLAG)

    override fun onDraw(canvas: Canvas) {
        super.onDraw(canvas)

        val cx = width * 0.5f
        val cy = height * 0.5f
        val radius = minOf(width, height) * 0.42f

        paint.shader = RadialGradient(
            cx,
            cy,
            radius,
            intArrayOf(
                Color.argb(255, 20, 170, 255),
                Color.argb(180, 40, 80, 255),
                Color.argb(70, 80, 40, 255),
                Color.argb(0, 0, 0, 0)
            ),
            floatArrayOf(
                0f,
                0.35f,
                0.7f,
                1f
            ),
            Shader.TileMode.CLAMP
        )

        canvas.drawCircle(
            cx,
            cy,
            radius,
            paint
        )

        paint.shader = null
        paint.style = Paint.Style.STROKE
        paint.strokeWidth = 3f
        paint.color = Color.argb(
            230,
            40,
            210,
            255
        )

        canvas.drawCircle(
            cx,
            cy,
            radius * 0.55f,
            paint
        )

        paint.style = Paint.Style.FILL
        paint.color = Color.WHITE

        canvas.drawCircle(
            cx,
            cy,
            8f,
            paint
        )
    }
}
