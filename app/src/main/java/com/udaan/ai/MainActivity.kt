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
import org.json.JSONObject
import java.util.concurrent.TimeUnit

class MainActivity : Activity() {

    private val client = OkHttpClient.Builder()
        .connectTimeout(15, TimeUnit.SECONDS)
        .readTimeout(60, TimeUnit.SECONDS)
        .build()

    /*
     * Backend URL final deployment ke baad yahan set hoga.
     * Abhi placeholder hai — fake success nahi dikhaya jayega.
     */
    private val backendUrl = "BACKEND_URL"

    /*
     * Real Founder API key app mein hard-code nahi karni.
     * Secure configuration next security phase mein add hogi.
     */
    private val founderApiKey = "FOUNDER_API_KEY"

    private lateinit var statusText: TextView
    private lateinit var commandInput: EditText

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        showCommandCenter()
    }

    private fun showCommandCenter() {

        val root = LinearLayout(this).apply {
            orientation = LinearLayout.VERTICAL
            setBackgroundColor(Color.rgb(7, 9, 16))
        }

        val header = LinearLayout(this).apply {
            orientation = LinearLayout.VERTICAL
            gravity = Gravity.CENTER
            setPadding(20, 30, 20, 20)
        }

        val logo = ImageView(this).apply {
            setImageResource(com.udaan.ai.R.drawable.udaan_logo)
            adjustViewBounds = true
        }

        header.addView(
            logo,
            LinearLayout.LayoutParams(
                110,
                110
            )
        )

        val title = TextView(this).apply {
            text = "UDAAN AI"
            textSize = 28f
            setTextColor(Color.WHITE)
            gravity = Gravity.CENTER
        }

        header.addView(title)

        val subtitle = TextView(this).apply {
            text = "AI COMMAND CENTER"
            textSize = 13f
            setTextColor(Color.LTGRAY)
            gravity = Gravity.CENTER
            setPadding(0, 5, 0, 15)
        }

        header.addView(subtitle)
        root.addView(header)

        val scroll = ScrollView(this)

        val content = LinearLayout(this).apply {
            orientation = LinearLayout.VERTICAL
            setPadding(25, 10, 25, 25)
        }

        commandInput = EditText(this).apply {
            hint = "Founder command likho..."
            hintTextColor = Color.GRAY
            setTextColor(Color.WHITE)
            textSize = 17f
            setPadding(20, 20, 20, 20)
        }

        content.addView(commandInput)

        val executeButton = Button(this).apply {
            text = "EXECUTE COMMAND"
            textSize = 15f

            setOnClickListener {
                sendCommand()
            }
        }

        content.addView(
            executeButton,
            LinearLayout.LayoutParams(
                ViewGroup.LayoutParams.MATCH_PARENT,
                ViewGroup.LayoutParams.WRAP_CONTENT
            ).apply {
                setMargins(0, 15, 0, 20)
            }
        )

        statusText = TextView(this).apply {
            text = "UDAAN AI CORE\nREADY"
            textSize = 16f
            setTextColor(Color.WHITE)
            setPadding(20, 20, 20, 25)
        }

        content.addView(statusText)

        addCard(content, "🤖 AI AGENTS", "Research • Content • Video • YouTube • Social")
        addCard(content, "📋 TASKS", "Active • Pending Approval • Completed")
        addCard(content, "🎬 VIDEO STUDIO", "Video creation and workflow")
        addCard(content, "📱 SOCIAL MEDIA", "Social content and publishing workflow")
        addCard(content, "📊 ANALYTICS", "Performance and reports")
        addCard(content, "👑 FOUNDER APPROVAL", "Approval required for sensitive actions")

        scroll.addView(content)

        root.addView(
            scroll,
            LinearLayout.LayoutParams(
                ViewGroup.LayoutParams.MATCH_PARENT,
                0,
                1f
            )
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
                setMargins(0, 5, 0, 5)
            }
        )
    }

    private fun sendCommand() {

        val command = commandInput.text.toString().trim()

        if (command.isEmpty()) {
            Toast.makeText(
                this,
                "Founder command empty hai",
                Toast.LENGTH_SHORT
            ).show()
            return
        }

        if (backendUrl == "BACKEND_URL") {
            statusText.text =
                "COMMAND READY\n\nBackend deployment pending."
            return
        }

        statusText.text = "UDAAN AI\n\nProcessing command..."

        Thread {

            try {

                val json = JSONObject()
                    .put("command", command)

                val body = json.toString()
                    .toRequestBody(
                        "application/json".toMediaType()
                    )

                val request = Request.Builder()
                    .url("$backendUrl/command")
                    .addHeader(
                        "X-Udaan-API-Key",
                        founderApiKey
                    )
                    .post(body)
                    .build()

                client.newCall(request).execute().use { response ->

                    val result =
                        response.body?.string() ?: ""

                    runOnUiThread {

                        if (response.isSuccessful) {

                            statusText.text =
                                "UDAAN AI RESPONSE\n\n$result"

                        } else {

                            statusText.text =
                                "BACKEND ERROR\n\nHTTP ${response.code}\n$result"
                        }
                    }
                }

            } catch (error: Exception) {

                runOnUiThread {

                    statusText.text =
                        "BACKEND CONNECTION FAILED\n\n${error.message}"
                }
            }
        }.start()
    }
}
