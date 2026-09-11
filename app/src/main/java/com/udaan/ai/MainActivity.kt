package com.udaan.ai

import android.graphics.Color
import android.os.Bundle
import android.view.Gravity
import android.view.ViewGroup
import android.widget.Button
import android.widget.EditText
import android.widget.LinearLayout
import android.widget.TextView
import android.widget.Toast

class MainActivity : android.app.Activity() {

    private lateinit var statusText: TextView

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)

        buildUdaanUI()
    }

    private fun buildUdaanUI() {

        val root = LinearLayout(this).apply {
            orientation = LinearLayout.VERTICAL
            setPadding(32, 40, 32, 32)
            setBackgroundColor(Color.rgb(8, 10, 18))
        }

        val logo = TextView(this).apply {
            text = "🦅  UDAAN AI"
            textSize = 30f
            setTextColor(Color.WHITE)
            gravity = Gravity.CENTER
        }

        root.addView(
            logo,
            LinearLayout.LayoutParams(
                ViewGroup.LayoutParams.MATCH_PARENT,
                ViewGroup.LayoutParams.WRAP_CONTENT
            )
        )

        val subtitle = TextView(this).apply {
            text = "AI COMMAND CENTER"
            textSize = 13f
            setTextColor(Color.LTGRAY)
            gravity = Gravity.CENTER
            setPadding(0, 8, 0, 35)
        }

        root.addView(subtitle)

        val commandInput = EditText(this).apply {
            hint = "Founder command likho..."
            hintTextColor = Color.GRAY
            setTextColor(Color.WHITE)
            textSize = 17f
            setPadding(24, 20, 24, 20)
        }

        root.addView(
            commandInput,
            LinearLayout.LayoutParams(
                ViewGroup.LayoutParams.MATCH_PARENT,
                ViewGroup.LayoutParams.WRAP_CONTENT
            )
        )

        val executeButton = Button(this).apply {
            text = "EXECUTE COMMAND"
            textSize = 16f
            setOnClickListener {

                val command = commandInput.text.toString().trim()

                if (command.isEmpty()) {
                    Toast.makeText(
                        this@MainActivity,
                        "Founder command empty hai",
                        Toast.LENGTH_SHORT
                    ).show()
                } else {
                    statusText.text =
                        "COMMAND RECEIVED\n\n$command\n\nBackend connection next phase mein connect hoga."
                }
            }
        }

        val buttonParams = LinearLayout.LayoutParams(
            ViewGroup.LayoutParams.MATCH_PARENT,
            ViewGroup.LayoutParams.WRAP_CONTENT
        )

        buttonParams.setMargins(0, 24, 0, 30)

        root.addView(executeButton, buttonParams)

        statusText = TextView(this).apply {
            text = "UDAAN AI READY\n\nSystem UI Online"
            textSize = 16f
            setTextColor(Color.WHITE)
            setPadding(20, 25, 20, 25)
        }

        root.addView(
            statusText,
            LinearLayout.LayoutParams(
                ViewGroup.LayoutParams.MATCH_PARENT,
                ViewGroup.LayoutParams.WRAP_CONTENT
            )
        )

        addSection(root, "🤖  AI AGENTS")
        addSection(root, "📋  TASKS")
        addSection(root, "🎬  VIDEO STUDIO")
        addSection(root, "📱  SOCIAL MEDIA")
        addSection(root, "📊  ANALYTICS")

        setContentView(root)
    }

    private fun addSection(root: LinearLayout, title: String) {

        val card = TextView(this).apply {
            text = title
            textSize = 17f
            setTextColor(Color.WHITE)
            setPadding(22, 22, 22, 22)
        }

        val params = LinearLayout.LayoutParams(
            ViewGroup.LayoutParams.MATCH_PARENT,
            ViewGroup.LayoutParams.WRAP_CONTENT
        )

        params.setMargins(0, 6, 0, 6)

        root.addView(card, params)
    }
}
