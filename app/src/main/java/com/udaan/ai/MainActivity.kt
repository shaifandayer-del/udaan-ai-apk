package com.udaan.ai

import android.app.Activity
import android.graphics.Color
import android.os.Bundle
import android.view.Gravity
import android.view.ViewGroup
import android.widget.Button
import android.widget.EditText
import android.widget.LinearLayout
import android.widget.ScrollView
import android.widget.TextView
import android.widget.Toast

class MainActivity : Activity() {

    private lateinit var content: LinearLayout
    private lateinit var status: TextView

    private val white = Color.WHITE
    private val gray = Color.rgb(170, 175, 190)
    private val background = Color.rgb(7, 9, 16)

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        showCommandCenter()
    }

    private fun baseScreen(title: String): LinearLayout {

        val root = LinearLayout(this).apply {
            orientation = LinearLayout.VERTICAL
            setBackgroundColor(background)
        }

        val header = TextView(this).apply {
            text = "🦅 UDAAN AI\n$title"
            textSize = 24f
            setTextColor(white)
            gravity = Gravity.CENTER
            setPadding(20, 35, 20, 25)
        }

        root.addView(
            header,
            LinearLayout.LayoutParams(
                ViewGroup.LayoutParams.MATCH_PARENT,
                ViewGroup.LayoutParams.WRAP_CONTENT
            )
        )

        val scroll = ScrollView(this)

        content = LinearLayout(this).apply {
            orientation = LinearLayout.VERTICAL
            setPadding(25, 10, 25, 25)
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

        return root
    }

    private fun createNavigation(): LinearLayout {

        val nav = LinearLayout(this).apply {
            orientation = LinearLayout.HORIZONTAL
            setPadding(8, 8, 8, 8)
        }

        val items = listOf(
            "Home",
            "Agents",
            "Tasks",
            "Content"
        )

        items.forEach { name ->

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

        val root = baseScreen("COMMAND CENTER")

        val command = EditText(this).apply {
            hint = "Founder command..."
            hintTextColor = gray
            setTextColor(white)
            textSize = 17f
        }

        root.findContent().addView(command)

        val execute = Button(this).apply {
            text = "EXECUTE COMMAND"

            setOnClickListener {

                val value = command.text.toString().trim()

                if (value.isEmpty()) {
                    Toast.makeText(
                        this@MainActivity,
                        "Command empty hai",
                        Toast.LENGTH_SHORT
                    ).show()
                } else {
                    status.text =
                        "COMMAND RECEIVED\n\n$value\n\nWaiting for backend..."
                }
            }
        }

        root.findContent().addView(execute)

        status = TextView(this).apply {
            text = "UDAAN AI CORE\nONLINE"
            textSize = 17f
            setTextColor(white)
            setPadding(10, 30, 10, 30)
        }

        root.findContent().addView(status)

        addCard(root.findContent(), "🧠 Main AI", "Command orchestration")
        addCard(root.findContent(), "🤖 AI Agents", "10 specialized AI agents")
        addCard(root.findContent(), "🎬 Video Studio", "Create and manage videos")
        addCard(root.findContent(), "📱 Social Media", "Social content automation")
        addCard(root.findContent(), "📊 Analytics", "Performance and reports")

        setContentView(root)
    }

    private fun showAgents() {

        val root = baseScreen("AI AGENTS")

        val agents = listOf(
            "Research AI",
            "Content AI",
            "Creative AI",
            "Video AI",
            "Social AI",
            "YouTube AI",
            "Analytics AI",
            "Marketing AI",
            "Developer AI",
            "Automation AI"
        )

        agents.forEach {
            addCard(root.findContent(), "🤖 $it", "Agent ready")
        }

        setContentView(root)
    }

    private fun showTasks() {

        val root = baseScreen("TASKS")

        addCard(
            root.findContent(),
            "📋 Active Tasks",
            "Founder tasks will appear here"
        )

        addCard(
            root.findContent(),
            "⏳ Pending Approval",
            "Founder approval tasks"
        )

        addCard(
            root.findContent(),
            "✅ Completed",
            "Completed UDAAN tasks"
        )

        setContentView(root)
    }

    private fun showContent() {

        val root = baseScreen("CONTENT")

        addCard(
            root.findContent(),
            "✍️ Content AI",
            "Create scripts, captions and posts"
        )

        addCard(
            root.findContent(),
            "🎬 Video AI",
            "Video creation workflow"
        )

        addCard(
            root.findContent(),
            "▶️ YouTube AI",
            "YouTube content workflow"
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
            setTextColor(white)
            setPadding(22, 22, 22, 22)
        }

        val params = LinearLayout.LayoutParams(
            ViewGroup.LayoutParams.MATCH_PARENT,
            ViewGroup.LayoutParams.WRAP_CONTENT
        )

        params.setMargins(0, 8, 0, 8)

        parent.addView(card, params)
    }

    private fun LinearLayout.findContent(): LinearLayout {
        return content
    }
}
