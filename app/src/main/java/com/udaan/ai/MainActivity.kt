
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

    private fun setupRoot(title: String, subtitle: String) {
        root = LinearLayout(this).apply {
            orientation = LinearLayout.VERTICAL
            setBackgroundColor(Color.parseColor("#030611"))
        }

        val header = LinearLayout(this).apply {
            orientation = LinearLayout.HORIZONTAL
            gravity = Gravity.CENTER_VERTICAL
            setPadding(14, 8, 14, 4)
        }

        val logo = ImageView(this).apply {
            setImageResource(R.drawable.udaan_logo)
            scaleType = ImageView.ScaleType.CENTER_INSIDE
        }

        header.addView(logo, LinearLayout.LayoutParams(58, 58))

        val brandBox = LinearLayout(this).apply {
            orientation = LinearLayout.VERTICAL
            setPadding(7, 0, 0, 0)
        }

        brandBox.addView(TextView(this).apply {
            text = "UDAAN AI"
            textSize = 18f
            setTextColor(Color.WHITE)
            typeface = Typeface.DEFAULT_BOLD
        })

        brandBox.addView(TextView(this).apply {
            text = subtitle
            textSize = 9f
            setTextColor(Color.parseColor("#8299BB"))
        })

        header.addView(
            brandBox,
            LinearLayout.LayoutParams(0, -2, 1f)
        )

        header.addView(TextView(this).apply {
            text = "● ONLINE"
            textSize = 9f
            setTextColor(Color.parseColor("#00F5A0"))
        })

        root.addView(header, LinearLayout.LayoutParams(-1, 70))

        root.addView(TextView(this).apply {
            text = title
            textSize = 23f
            setTextColor(Color.WHITE)
            typeface = Typeface.DEFAULT_BOLD
            setPadding(18, 4, 18, 8)
        }, LinearLayout.LayoutParams(-1, 52))

        val scroll = ScrollView(this).apply {
            isFillViewport = true
            overScrollMode = View.OVER_SCROLL_NEVER
        }

        content = LinearLayout(this).apply {
            orientation = LinearLayout.VERTICAL
            setPadding(14, 4, 14, 20)
        }

        scroll.addView(content, ScrollView.LayoutParams(-1, -2)

        root.addView(
            scroll,
            LinearLayout.LayoutParams(-1, 0, 1f)
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

        private fun addCommandBox() {
    val hero = FrameLayout(this).apply {
        background = gradient("#061D42", "#020817", 28)
        setPadding(10, 10, 10, 10)
    }

    val orbParams =
        android.widget.FrameLayout.LayoutParams(
            235,
            205
        ).apply {
            gravity = Gravity.END or Gravity.CENTER_VERTICAL
        }

    hero.addView(
        UdaanOrbView(this),
        orbParams
    )

    val glowLabel = TextView(this).apply {
        text = "● AI CORE ONLINE"
        textSize = 8f
        setTextColor(Color.parseColor("#00E8FF"))
        typeface = Typeface.DEFAULT_BOLD
    }

    val glowParams =
        android.widget.FrameLayout.LayoutParams(
            -2,
            -2
        ).apply {
            gravity = Gravity.TOP or Gravity.END
            topMargin = 10
            rightMargin = 14
        }

    hero.addView(
        glowLabel,
        glowParams
    )

    val textBox = LinearLayout(this).apply {
        orientation = LinearLayout.VERTICAL
        gravity = Gravity.CENTER_VERTICAL
        setPadding(14, 4, 0, 4)
    }

    textBox.addView(
        TextView(this).apply {
            text = "WELCOME BACK"
            textSize = 9f
            setTextColor(Color.parseColor("#7FA8D8"))
            typeface = Typeface.DEFAULT_BOLD
        }
    )

    textBox.addView(
        TextView(this).apply {
            text = "Founder"
            textSize = 29f
            setTextColor(Color.WHITE)
            typeface = Typeface.DEFAULT_BOLD
        }
    )

    textBox.addView(
        TextView(this).apply {
            text = "What shall we create today?"
            textSize = 11f
            setTextColor(Color.parseColor("#A8BEDD"))
            setPadding(0, 4, 0, 10)
        }
    )

    textBox.addView(
        Button(this).apply {
            text = "⚡  TAP TO START"
            textSize = 9f
            setTextColor(Color.WHITE)
            background = gradient(
                "#008DFF",
                "#733CFF",
                18
            )

            setOnClickListener {
                showCommandCenter()
            }
        },
        LinearLayout.LayoutParams(
            145,
            45
        )
    )

    val textParams =
        android.widget.FrameLayout.LayoutParams(
            190,
            -1
        ).apply {
            gravity = Gravity.START or Gravity.CENTER_VERTICAL
        }

    hero.addView(
        textBox,
        textParams
    )

    content.addView(
        hero,
        LinearLayout.LayoutParams(
            -1,
            210
        ).apply {
            bottomMargin = 14
        }
    )
}
    
        addSection("UDAAN AI CORE")

        addInfoCard(
            "● UDAAN AI CORE",
            "All systems operational • Founder mode active"
        )

        addSection("AI COMMAND CENTER")

        addCommandBox()

        addSection("AI MODULES")

        addModuleGrid(
            listOf(
                Triple("AI AGENTS", "10 Agents", "◈"),
                Triple("TASKS", "Active Tasks", "✓"),
                Triple("CONTENT", "Create Content", "✎"),
                Triple("VIDEO STUDIO", "AI Videos", "▶"),
                Triple("YOUTUBE", "Channel", "▶"),
                Triple("SOCIAL MEDIA", "Auto Post", "◎"),
                Triple("ANALYTICS", "Reports", "▥"),
                Triple("MARKETING", "Growth", "⚑"),
                Triple("DEVELOPER", "Build Apps", "</>"),
                Triple("AUTOMATION", "Workflows", "⚙"),
                Triple("CREATIVE", "Creative AI", "✦"),
                Triple("APP BUILDER", "Software", "⌘")
            )
        ) { index ->
            when (index) {
                0 -> showAgents()
                1 -> showTasks()
                2 -> showContent()
                3 -> showVideoStudio()
                4 -> showYouTube()
                5 -> showInstagram()
                6 -> showAnalytics()
                7 -> setCommandAndExecute("Show marketing analytics")
                8 -> setCommandAndExecute("Build a test app")
                9 -> setCommandAndExecute("Create an automation workflow")
                10 -> setCommandAndExecute("Create a creative concept")
                11 -> setCommandAndExecute("Build a test app")
            }
        }

        addSection("FOUNDER CONTROL")

        moduleButton(
            "Founder Approval",
            "Publishing, uploading, deploying and other high-impact actions require your approval."
        ) {
            showApprovals()
        }

        addAgentBottomBar()
        addStatus()
    }

    private fun addFuturisticHero() {
        val hero = FrameLayout(this).apply {
            background = gradient("#061D42", "#020817", 28)
            setPadding(10, 10, 10, 10)
        }

        val orbParams =
            android.widget.FrameLayout.LayoutParams(235, 205).apply {
                gravity = Gravity.END or Gravity.CENTER_VERTICAL
            }

        hero.addView(
            UdaanOrbView(this),
            orbParams
        )

        val glowLabel = TextView(this).apply {
            text = "● AI CORE ONLINE"
            textSize = 8f
            setTextColor(Color.parseColor("#00E8FF"))
            typeface = Typeface.DEFAULT_BOLD
        }

        val glowParams =
            android.widget.FrameLayout.LayoutParams(-2, -2).apply {
                gravity = Gravity.TOP or Gravity.END
                topMargin = 10
                rightMargin = 14
            }

        hero.addView(glowLabel, glowParams)

        val textBox = LinearLayout(this).apply {
            orientation = LinearLayout.VERTICAL
            gravity = Gravity.CENTER_VERTICAL
            setPadding(14, 4, 0, 4)
        }

        textBox.addView(TextView(this).apply {
            text = "WELCOME BACK"
            textSize = 9f
            setTextColor(Color.parseColor("#7FA8D8"))
            typeface = Typeface.DEFAULT_BOLD
        })

        textBox.addView(TextView(this).apply {
            text = "Founder"
            textSize = 29f
            setTextColor(Color.WHITE)
            typeface = Typeface.DEFAULT_BOLD
        })

        textBox.addView(TextView(this).apply {
            text = "What shall we create today?"
            textSize = 11f
            setTextColor(Color.parseColor("#A8BEDD"))
            setPadding(0, 4, 0, 10)
        })

        textBox.addView(
            Button(this).apply {
                text = "⚡  TAP TO START"
                textSize = 9f
                setTextColor(Color.WHITE)
                background = gradient("#008DFF", "#733CFF", 18)
                setOnClickListener {
                    showCommandCenter()
                }
            },
            LinearLayout.LayoutParams(145, 45)
        )

        val textParams =
            android.widget.FrameLayout.LayoutParams(190, -1).apply {
                gravity = Gravity.START or Gravity.CENTER_VERTICAL
            }

        hero.addView(textBox, textParams)

        content.addView(
            hero,
            LinearLayout.LayoutParams(-1, 210).apply {
                bottomMargin = 14
            }
        )
    }

    private fun addCommandBox() {
        val card = glass()

        card.addView(TextView(this).apply {
            text = "AI COMMAND CENTER"
            textSize = 11f
            setTextColor(Color.parseColor("#00E8FF"))
            typeface = Typeface.DEFAULT_BOLD
        })

        card.addView(TextView(this).apply {
            text = "Tell UDAAN what you want to do..."
            textSize = 15f
            setTextColor(Color.WHITE)
            typeface = Typeface.DEFAULT_BOLD
            setPadding(0, 4, 0, 8)
        })

        val input = EditText(this).apply {
            hint = "e.g. Create a YouTube video on AI"
            setHintTextColor(Color.parseColor("#627895"))
            setTextColor(Color.WHITE)
            textSize = 12f
            setSingleLine(false)
            setPadding(14, 8, 14, 8)
            background = gradient("#071A35", "#040B18", 16)
        }

        card.addView(input, LinearLayout.LayoutParams(-1, 68))

        card.addView(
            Button(this).apply {
                text = "⚡  ASK UDAAN AI"
                textSize = 10f
                setTextColor(Color.WHITE)
                background = gradient("#008DFF", "#673BFF", 18)

                setOnClickListener {
                    val command = input.text.toString().trim()

                    if (command.isNotEmpty()) {
                        sendCommand(command)
                    } else {
                        Toast.makeText(
                            this@MainActivity,
                            "Command enter karo.",
                            Toast.LENGTH_SHORT
                        ).show()
                    }
                }
            },
            LinearLayout.LayoutParams(-1, 48).apply {
                topMargin = 9
            }
        )

        content.addView(
            card,
            LinearLayout.LayoutParams(-1, -2).apply {
                bottomMargin = 12
            }
        )
    }

    private fun addModuleGrid(
        items: List<Triple<String, String, String>>,
        action: (Int) -> Unit
    ) {
        var row: LinearLayout? = null

        items.forEachIndexed { index, item ->

            if (index % 3 == 0) {
                row = LinearLayout(this).apply {
                    orientation = LinearLayout.HORIZONTAL
                }

                content.addView(
                    row,
                    LinearLayout.LayoutParams(-1, 112)
                )
            }

            val card = LinearLayout(this).apply {
                orientation = LinearLayout.VERTICAL
                gravity = Gravity.CENTER
                setPadding(5, 8, 5, 8)

                background = gradient("#0A2141", "#050C1B", 18)

                setOnClickListener {
                    action(index)
                }
            }

            card.addView(TextView(this).apply {
                text = item.third
                textSize = 23f
                gravity = Gravity.CENTER
                setTextColor(Color.parseColor("#00E8FF"))
            })

            card.addView(TextView(this).apply {
                text = item.first
                textSize = 8.5f
                gravity = Gravity.CENTER
                setTextColor(Color.WHITE)
                typeface = Typeface.DEFAULT_BOLD
            })

            card.addView(TextView(this).apply {
                text = item.second
                textSize = 7.5f
                gravity = Gravity.CENTER
                setTextColor(Color.parseColor("#7891B4"))
            })

            row?.addView(
                card,
                LinearLayout.LayoutParams(0, 104, 1f).apply {
                    setMargins(4, 4, 4, 4)
                }
            )
        }
    }

    private fun showCommandCenter() {
        currentPage = "COMMAND"

        setupRoot(
            "AI Command Center",
            "Command → Plan → Execute"
        )

        addCommandBox()

        addSection("QUICK ACTIONS")

        moduleButton(
            "YouTube Video",
            "Research → Script → Video → Approval → Upload"
        ) {
            setCommandAndExecute("Create a YouTube video")
        }

        moduleButton(
            "Social Post",
            "Create social media content"
        ) {
            setCommandAndExecute("Create a social media post")
        }

        moduleButton(
            "Blog Article",
            "Research and create article"
        ) {
            setCommandAndExecute("Create a blog article")
        }

        moduleButton(
            "Create Image",
            "Create an image concept"
        ) {
            setCommandAndExecute("Create an image concept")
        }

        moduleButton(
            "Build App",
            "Developer AI builds software"
        ) {
            setCommandAndExecute("Build a test app")
        }

        addAgentBottomBar()
        addStatus()
    }

    private fun showAgents() {
        currentPage = "AGENTS"

        setupRoot(
            "AI Agents",
            "Specialized UDAAN AI Agents"
        )

        val allAgents = mutableListOf<UdaanAgent>()

        allAgents.add(
            UdaanAgent(
                "Main AI / Orchestrator",
                "Command planning, routing and complete workflow.",
                "CORE"
            )
        )

        allAgents.addAll(dynamicAgents)

        if (allAgents.size <= 1) {
            addInfoCard(
                "LOADING AGENTS",
                "Backend se specialized agents load ho rahe hain..."
            )

            loadDynamicAgents()
        } else {
            allAgents
                .distinctBy {
                    it.name.lowercase()
                }
                .forEach { agent ->
                    moduleButton(
                        agent.name,
                        "${agent.description}\n● ${agent.status}"
                    ) {
                        openAgent(agent)
                    }
                }
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
            textSize = 13f
            setPadding(14, 12, 14, 12)
            background = gradient("#07142A", "#050B16", 16)
        }

        content.addView(
            input,
            LinearLayout.LayoutParams(-1, 100).apply {
                bottomMargin = 10
            }
        )

        content.addView(
            Button(this).apply {
                text = "⚡ RUN ${agent.name.uppercase()}"
                textSize = 9f
                setTextColor(Color.WHITE)
                background = gradient("#008DFF", "#6037FF", 18)

                setOnClickListener {
                    val command = input.text.toString().trim()

                    if (command.isNotEmpty()) {
                        sendCommand("${agent.name}: $command")
                    }
                }
            },
            LinearLayout.LayoutParams(-1, 52)
        )

        addAgentBottomBar()
        addStatus()
    }

    private fun showTasks() {
        currentPage = "TASKS"

        setupRoot(
            "Tasks",
            "AI Task Center"
        )

        addSection("TASK MANAGEMENT")

        moduleButton(
            "All Tasks",
            "View all UDAAN tasks"
        ) {
            loadBackendStatus()
        }

        moduleButton(
            "Pending",
            "Tasks waiting for approval"
        ) {
            loadApprovals()
        }

        moduleButton(
            "In Progress",
            "Currently running tasks"
        ) {
            loadBackendStatus()
        }

        moduleButton(
            "Completed",
            "Completed executions"
        ) {
            loadBackendStatus()
        }

        addAgentBottomBar()
        addStatus()
    }

    private fun showContent() {
        currentPage = "CONTENT"

        setupRoot(
            "Content Studio",
            "AI Content Creation"
        )

        addSection("CREATE")

        moduleButton(
            "Script Writer",
            "AI video scripts"
        ) {
            setCommandAndExecute("Write a video script")
        }

        moduleButton(
            "Caption Generator",
            "Social media captions"
        ) {
            setCommandAndExecute("Create social media captions")
        }

        moduleButton(
            "Post Creator",
            "Social media posts"
        ) {
            setCommandAndExecute("Create a social media post")
        }

        moduleButton(
            "Blog Writer",
            "Articles and blogs"
        ) {
            setCommandAndExecute("Create a blog article")
        }

        addAgentBottomBar()
        addStatus()
    }

    private fun showVideoStudio() {
        currentPage = "VIDEO"

        setupRoot(
            "Video Studio",
            "AI Video Production"
        )

        addSection("AI VIDEO GENERATOR")

        moduleButton(
            "Create Video",
            "Research → Content → Creative → Render"
        ) {
            setCommandAndExecute("Create a complete video")
        }

        moduleButton(
            "Text to Video",
            "Turn text into video"
        ) {
            setCommandAndExecute("Create a video from this text")
        }

        moduleButton(
            "Video Editor",
            "Edit generated videos"
        ) {
            showResult(
                "Video Editor",
                "Video editing pipeline ready."
            )
        }

        moduleButton(
            "Voiceover",
            "AI voice generation"
        ) {
            showResult(
                "Voiceover",
                "Voiceover pipeline ready."
            )
        }

        moduleButton(
            "Templates",
            "AI video templates"
        ) {
            showResult(
                "Templates",
                "Video templates ready."
            )
        }

        moduleButton(
            "Final Video",
            "Founder review"
        ) {
            showFinalVideo()
        }

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
            "FINAL VIDEO",
            "Video is ready for Founder approval."
        )

        moduleButton(
            "Approve",
            "Approve video for publishing"
        ) {
            showApprovals()
        }

        moduleButton(
            "Reject",
            "Request video revision"
        ) {
            showResult(
                "Video Rejected",
                "Revision requested."
            )
        }

        moduleButton(
            "YouTube Upload",
            "Upload approved video"
        ) {
            showYouTube()
        }

        moduleButton(
            "Instagram Publish",
            "Publish approved Reel"
        ) {
            showInstagram()
        }

        addAgentBottomBar()
        addStatus()
    }

    private fun showYouTube() {
        currentPage = "YOUTUBE"

        setupRoot(
            "YouTube AI",
            "YouTube Management"
        )

        addInfoCard(
            "YOUTUBE",
            "OAuth 2.0 + YouTube Data API"
        )

        moduleButton(
            "Channel Stats",
            "Channel analytics"
        ) {
            loadBackendStatus()
        }

        moduleButton(
            "Upload Video",
            "Upload approved video"
        ) {
            setCommandAndExecute(
                "Upload approved video to YouTube"
            )
        }

        moduleButton(
            "Recent Uploads",
            "Recent channel uploads"
        ) {
            showResult(
                "YouTube",
                "Recent upload data handled by YouTube integration."
            )
        }

        moduleButton(
            "Research",
            "Find best YouTube topics"
        ) {
            setCommandAndExecute(
                "Research best YouTube topics"
            )
        }

        addAgentBottomBar()
        addStatus()
    }

    private fun showInstagram() {
        currentPage = "SOCIAL"

        setupRoot(
            "Social Media AI",
            "Multi-Channel Publishing"
        )

        addInfoCard(
            "SOCIAL MEDIA",
            "Instagram + multi-channel automation"
        )

        moduleButton(
            "Create Post",
            "Create social post"
        ) {
            setCommandAndExecute(
                "Create a social media post"
            )
        }

        moduleButton(
            "Publish Reel",
            "Publish approved video"
        ) {
            setCommandAndExecute(
                "Publish approved video to Instagram"
            )
        }

        moduleButton(
            "Social Research",
            "Research trending content"
        ) {
            setCommandAndExecute(
                "Research trending social media content"
            )
        }

        addAgentBottomBar()
        addStatus()
    }

    private fun showAnalytics() {
        currentPage = "ANALYTICS"

        setupRoot(
            "Analytics AI",
            "Performance Intelligence"
        )

        addInfoCard(
            "ANALYTICS",
            "Content, social, YouTube and system analytics."
        )

        moduleButton(
            "System Analytics",
            "Backend performance"
        ) {
            loadBackendStatus()
        }

        moduleButton(
            "Content Analytics",
            "Analyze content performance"
        ) {
            setCommandAndExecute(
                "Show content analytics"
            )
        }

        moduleButton(
            "Marketing Analytics",
            "Analyze marketing performance"
        ) {
            setCommandAndExecute(
                "Show marketing analytics"
            )
        }

        moduleButton(
            "Growth Report",
            "Generate growth report"
        ) {
            setCommandAndExecute(
                "Generate a growth report"
            )
        }

        addAgentBottomBar()
        addStatus()
    }

    private fun showApprovals() {
        currentPage = "APPROVALS"

        setupRoot(
            "Founder Approval",
            "Founder Control Center"
        )

        addInfoCard(
            "👑 FOUNDER CONTROL",
            "No publishing, uploading, deploying or high-impact action happens without Founder approval."
        )

        moduleButton(
            "Pending Approvals",
            "Open approval queue"
        ) {
            loadApprovals()
        }

        moduleButton(
            "Approve",
            "Approve selected action"
        ) {
            loadApprovals()
        }

        moduleButton(
            "Reject",
            "Reject selected action"
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
            "FOUNDER NOTIFICATIONS",
            "Approval, task, video, upload and system events."
        )

        addAgentBottomBar()
        addStatus()
    }

    private fun showSettings() {
        currentPage = "SETTINGS"

        setupRoot(
            "Settings",
            "UDAAN AI Configuration"
        )

        addInfoCard(
            "BACKEND",
            baseUrl
        )

        addInfoCard(
            "SECURITY",
            if (apiKey.isNotEmpty()) {
                "Founder API Key configured"
            } else {
                "Founder API Key missing"
            }
        )

        moduleButton(
            "Test Backend",
            "Check backend connection"
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
            "UDAAN AI Infrastructure"
        )

        addInfoCard(
            "SYSTEM",
            "Backend, agents, security and AI services."
        )

        moduleButton(
            "Backend Status",
            "Check backend"
        ) {
            loadBackendStatus()
        }

        moduleButton(
            "Reload Agents",
            "Refresh AI agents"
        ) {
            loadDynamicAgents()
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
            "AI video creation"
        ) {
            showVideoStudio()
        }

        moduleButton(
            "YouTube",
            "YouTube AI"
        ) {
            showYouTube()
        }

        moduleButton(
            "Social Media",
            "Social Media AI"
        ) {
            showInstagram()
        }

        moduleButton(
            "Analytics",
            "Analytics AI"
        ) {
            showAnalytics()
        }

        moduleButton(
            "Marketing AI",
            "Marketing automation"
        ) {
            setCommandAndExecute(
                "Show marketing analytics"
            )
        }

        moduleButton(
            "Developer AI",
            "Build software"
        ) {
            setCommandAndExecute(
                "Build a test app"
            )
        }

        moduleButton(
            "Automation AI",
            "Create automation"
        ) {
            setCommandAndExecute(
                "Create an automation workflow"
            )
        }

        moduleButton(
            "Creative AI",
            "Creative generation"
        ) {
            setCommandAndExecute(
                "Create a creative concept"
            )
        }

        moduleButton(
            "Founder Approval",
            "Approve or reject actions"
        ) {
            showApprovals()
        }

        moduleButton(
            "Notifications",
            "Founder notifications"
        ) {
            showNotifications()
        }

        moduleButton(
            "Settings",
            "System settings"
        ) {
            showSettings()
        }

        moduleButton(
            "System",
            "System status"
        ) {
            showSystem()
        }

        addAgentBottomBar()
        addStatus()
    }

    private fun addAgentBottomBar() {
        if (dynamicAgents.isEmpty()) return

        val wrapper = LinearLayout(this).apply {
            orientation = LinearLayout.VERTICAL
            background = gradient("#071A35", "#030914", 18)
            setPadding(8, 7, 8, 7)
        }

        wrapper.addView(
            TextView(this).apply {
                text = "AI AGENTS"
                textSize = 9f
                gravity = Gravity.CENTER
                setTextColor(Color.parseColor("#00E8FF"))
                typeface = Typeface.DEFAULT_BOLD
            },
            LinearLayout.LayoutParams(-1, 20)
        )

        val scroll = HorizontalScrollView(this).apply {
            isHorizontalScrollBarEnabled = false
            overScrollMode = View.OVER_SCROLL_NEVER
        }

        val row = LinearLayout(this).apply {
            orientation = LinearLayout.HORIZONTAL
        }

        dynamicAgents
            .distinctBy {
                it.name.lowercase()
            }
            .forEach { agent ->

                row.addView(
                    TextView(this).apply {
                        text = agent.name
                        textSize = 8.5f
                        gravity = Gravity.CENTER
                        setTextColor(Color.WHITE)
                        setPadding(13, 9, 13, 9)
                        background = gradient(
                            "#0B2A50",
                            "#071426",
                            15
                        )

                        setOnClickListener {
                            openAgent(agent)
                        }
                    },
                    LinearLayout.LayoutParams(-2, 42).apply {
                        setMargins(3, 2, 3, 2)
                    }
                )
            }

        scroll.addView(row)

        wrapper.addView(
            scroll,
            LinearLayout.LayoutParams(-1, 46)
        )

        content.addView(
            wrapper,
            LinearLayout.LayoutParams(-1, -2).apply {
                topMargin = 12
                bottomMargin = 10
            }
        )
    }

    private fun addBottomNavigation() {
        val nav = LinearLayout(this).apply {
            orientation = LinearLayout.HORIZONTAL
            gravity = Gravity.CENTER
            setPadding(4, 4, 4, 4)
            background = gradient("#071329", "#020711", 20)
        }

        addNavigationButton(nav, "⌂", "Home") {
            showHome()
        }

        addNavigationButton(nav, "◈", "Agents") {
            showAgents()
        }

        addNavigationButton(nav, "▣", "Tasks") {
            showTasks()
        }

        addNavigationButton(nav, "✎", "Content") {
            showContent()
        }

        addNavigationButton(nav, "⋯", "More") {
            showMore()
        }

        root.addView(
            nav,
            LinearLayout.LayoutParams(-1, 64)
        )
    }

    private fun addNavigationButton(
        parent: LinearLayout,
        icon: String,
        title: String,
        action: () -> Unit
    ) {
        parent.addView(
            Button(this).apply {
                text = "$icon\n$title"
                textSize = 8f
                setTextColor(Color.WHITE)
                setBackgroundColor(Color.TRANSPARENT)

                setOnClickListener {
                    action()
                }
            },
            LinearLayout.LayoutParams(0, -1, 1f)
        )
    }

    private fun addSection(title: String) {
        content.addView(
            TextView(this).apply {
                text = title
                textSize = 10f
                setTextColor(Color.parseColor("#00E8FF"))
                typeface = Typeface.DEFAULT_BOLD
                setPadding(4, 14, 4, 7)
            }
        )
    }

    private fun addStatus() {
        statusText = TextView(this).apply {
            text = "● UDAAN AI READY"
            textSize = 9f
            setTextColor(Color.parseColor("#00F5A0"))
            setPadding(4, 10, 4, 4)
        }

        content.addView(statusText)
    }

    private fun addInfoCard(
        title: String,
        message: String
    ) {
        val card = glass()

        card.addView(TextView(this).apply {
            text = title
            textSize = 13f
            setTextColor(Color.WHITE)
            typeface = Typeface.DEFAULT_BOLD
        })

        card.addView(TextView(this).apply {
            text = message
            textSize = 10f
            setTextColor(Color.parseColor("#8197B6"))
            setPadding(0, 5, 0, 0)
        })

        content.addView(
            card,
            LinearLayout.LayoutParams(-1, -2).apply {
                bottomMargin = 8
            }
        )
    }

    private fun moduleButton(
        title: String,
        description: String,
        action: () -> Unit
    ) {
        val card = glass()

        card.addView(TextView(this).apply {
            text = title
            textSize = 15f
            setTextColor(Color.WHITE)
            typeface = Typeface.DEFAULT_BOLD
        })

        card.addView(TextView(this).apply {
            text = description
            textSize = 10f
            setTextColor(Color.parseColor("#8197B6"))
            setPadding(0, 4, 0, 8)
        })

        card.addView(
            Button(this).apply {
                text = "OPEN  ›"
                textSize = 9f
                setTextColor(Color.WHITE)
                background = gradient("#008DFF", "#503CFF", 15)

                setOnClickListener {
                    action()
                }
            },
            LinearLayout.LayoutParams(-1, 44)
        )

        content.addView(
            card,
            LinearLayout.LayoutParams(-1, -2).apply {
                bottomMargin = 8
            }
        )
    }

    private fun glass(): LinearLayout {
        return LinearLayout(this).apply {
            orientation = LinearLayout.VERTICAL
            setPadding(13, 13, 13, 13)
            background = gradient("#0A1930", "#050B17", 20)
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
                Color.parseColor("#1A4E82")
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

        updateStatus(
            "● PROCESSING...",
            "#FFB300"
        )

        val body =
            JSONObject().apply {
                put("command", command)
            }
                .toString()
                .toRequestBody(
                    "application/json".toMediaType()
                )

        val request =
            Request.Builder()
                .url("$baseUrl/command")
                .addHeader(
                    "X-Udaan-API-Key",
                    apiKey
                )
                .post(body)
                .build()

        client.newCall(request).enqueue(
            object : Callback {

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
                    response.use {
                        val result =
                            it.body?.string() ?: ""

                        runOnUiThread {
                            if (it.isSuccessful) {
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
                }
            }
        )
    }

    private fun loadDynamicAgents() {
        if (apiKey.isEmpty()) return

        val request =
            Request.Builder()
                .url("$baseUrl/agents")
                .addHeader(
                    "X-Udaan-API-Key",
                    apiKey
                )
                .get()
                .build()

        client.newCall(request).enqueue(
            object : Callback {

                override fun onFailure(
                    call: Call,
                    e: IOException
                ) {
                    runOnUiThread {
                        if (::statusText.isInitialized) {
                            updateStatus(
                                "● AGENTS CONNECTION FAILED",
                                "#FF4D6D"
                            )
                        }
                    }
                }

                override fun onResponse(
                    call: Call,
                    response: Response
                ) {
                    response.use {
                        val body =
                            it.body?.string() ?: ""

                        if (!it.isSuccessful) return

                        val agents =
                            parseAgents(body)

                        runOnUiThread {
                            dynamicAgents.clear()
                            dynamicAgents.addAll(agents)

                            when (currentPage) {
                                "HOME" -> showHome()
                                "AGENTS" -> showAgents()
                            }
                        }
                    }
                }
            }
        )
    }

    private fun parseAgents(
        json: String
    ): List<UdaanAgent> {
        val result =
            mutableListOf<UdaanAgent>()

        try {
            val objectRoot =
                JSONObject(json)

            val array =
                objectRoot.optJSONArray("agents")

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
        }

        try {
            val array =
                JSONArray(json)

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

        return result
    }

    private fun loadBackendStatus() {
        if (apiKey.isEmpty()) return

        val request =
            Request.Builder()
                .url("$baseUrl/status")
                .addHeader(
                    "X-Udaan-API-Key",
                    apiKey
                )
                .get()
                .build()

        client.newCall(request).enqueue(
            object : Callback {

                override fun onFailure(
                    call: Call,
                    e: IOException
                ) {
                    runOnUiThread {
                        showResult(
                            "Backend Status",
                            e.message
                                ?: "Connection failed"
                        )
                    }
                }

                override fun onResponse(
                    call: Call,
                    response: Response
                ) {
                    response.use {
                        val body =
                            it.body?.string() ?: ""

                        runOnUiThread {
                            showResult(
                                "Backend Status",
                                prettyJson(body)
                            )
                        }
                    }
                }
            }
        )
    }

    private fun loadApprovals() {
        if (apiKey.isEmpty()) return

        val request =
            Request.Builder()
                .url("$baseUrl/approvals")
                .addHeader(
                    "X-Udaan-API-Key",
                    apiKey
                )
                .get()
                .build()

        client.newCall(request).enqueue(
            object : Callback {

                override fun onFailure(
                    call: Call,
                    e: IOException
                ) {
                    runOnUiThread {
                        showResult(
                            "Founder Approval",
                            e.message
                                ?: "Connection failed"
                        )
                    }
                }

                override fun onResponse(
                    call: Call,
                    response: Response
                ) {
                    response.use {
                        val body =
                            it.body?.string() ?: ""

                        runOnUiThread {
                            showResult(
                                "Founder Approval Queue",
                                prettyJson(body)
                            )
                        }
                    }
                }
            }
        )
    }

    private fun showResult(
        title: String,
        message: String
    ) {
        currentPage = "RESULT"

        setupRoot(
            title,
            "UDAAN AI"
        )

        addInfoCard(
            "RESULT",
            message
        )

        moduleButton(
            "Back to Home",
            "Return to Command Center"
        ) {
            showHome()
        }

        addAgentBottomBar()
        addStatus()
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
            when {
                value.trim().startsWith("{") ->
                    JSONObject(
                        value.trim()
                    ).toString(2)

                value.trim().startsWith("[") ->
                    JSONArray(
                        value.trim()
                    ).toString(2)

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

private class UdaanOrbView(
    context: Context
) : View(context) {

    private val paint =
        Paint(Paint.ANTI_ALIAS_FLAG)

    private val glowPaint =
        Paint(Paint.ANTI_ALIAS_FLAG)

    override fun onDraw(canvas: Canvas) {
        super.onDraw(canvas)

        val cx = width * 0.52f
        val cy = height * 0.50f

        val radius =
            minOf(width, height) * 0.36f

        glowPaint.shader =
            RadialGradient(
                cx,
                cy,
                radius * 1.65f,
                intArrayOf(
                    Color.argb(210, 0, 220, 255),
                    Color.argb(130, 20, 110, 255),
                    Color.argb(70, 110, 50, 255),
                    Color.argb(0, 0, 0, 0)
                ),
                floatArrayOf(
                    0f,
                    0.38f,
                    0.68f,
                    1f
                ),
                Shader.TileMode.CLAMP
            )

        canvas.drawCircle(
            cx,
            cy,
            radius * 1.65f,
            glowPaint
        )

        paint.shader =
            RadialGradient(
                cx - radius * 0.25f,
                cy - radius * 0.25f,
                radius,
                intArrayOf(
                    Color.WHITE,
                    Color.rgb(100, 220, 255),
                    Color.rgb(30, 100, 255),
                    Color.rgb(35, 20, 110)
                ),
                floatArrayOf(
                    0f,
                    0.25f,
                    0.65f,
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
        paint.strokeWidth = 3.5f
        paint.color = Color.argb(
            245,
            70,
            230,
            255
        )

        canvas.drawCircle(
            cx,
            cy,
            radius * 1.04f,
            paint
        )

        paint.strokeWidth = 1.7f
        paint.color = Color.argb(
            180,
            110,
            150,
            255
        )

        canvas.drawCircle(
            cx,
            cy,
            radius * 0.80f,
            paint
        )

        canvas.drawCircle(
            cx,
            cy,
            radius * 0.58f,
            paint
        )

        paint.strokeWidth = 1f

        canvas.drawOval(
            cx - radius * 0.72f,
            cy - radius * 0.30f,
            cx + radius * 0.72f,
            cy + radius * 0.30f,
            paint
        )

        canvas.drawOval(
            cx - radius * 0.30f,
            cy - radius * 0.72f,
            cx + radius * 0.30f,
            cy + radius * 0.72f,
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

        paint.color = Color.argb(
            210,
            0,
            240,
            255
        )

        canvas.drawCircle(
            cx - radius * 0.70f,
            cy - radius * 0.55f,
            5f,
            paint
        )

        canvas.drawCircle(
            cx + radius * 0.66f,
            cy - radius * 0.10f,
            4f,
            paint
        )

        canvas.drawCircle(
            cx + radius * 0.55f,
            cy + radius * 0.58f,
            5f,
            paint
        )

        paint.color = Color.argb(
            180,
            120,
            80,
            255
        )

        canvas.drawCircle(
            cx - radius * 0.58f,
            cy + radius * 0.50f,
            4f,
            paint
        )
    }
}
