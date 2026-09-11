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

class MainActivity : AppCompatActivity() {

    private val client = OkHttpClient()

    private val backendUrl =
        "https://udaan-ai-apk-1.onrender.com"

    private val founderApiKey =
        BuildConfig.UDAAN_FOUNDER_API_KEY

    private lateinit var rootLayout: LinearLayout
    private lateinit var statusText: TextView
    private lateinit var commandInput: EditText

    data class UdaanAgent(
        val name: String,
        val module: String,
        val description: String,
        val status: String,
        val functions: List<String>
    )

    private var dynamicAgents = mutableListOf<UdaanAgent>()

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)

        showCommandCenter()
        loadDynamicAgents()
    }

    private fun showCommandCenter() {

        rootLayout = createRoot("UDAAN AI")

        val hero = TextView(this).apply {
            text = "AI COMMAND CENTER"
            textSize = 28f
            setTextColor(Color.WHITE)
            typeface = Typeface.DEFAULT_BOLD
            gravity = Gravity.CENTER
            setPadding(20, 35, 20, 8)
        }

        rootLayout.addView(hero)

        val subtitle = TextView(this).apply {
            text = "Your personal intelligent AI operating system"
            textSize = 14f
            setTextColor(Color.LTGRAY)
            gravity = Gravity.CENTER
            setPadding(20, 0, 20, 25)
        }

        rootLayout.addView(subtitle)

        val onlineCard = createCard()

        val onlineTitle = TextView(this).apply {
            text = "●  UDAAN CORE"
            textSize = 18f
            typeface = Typeface.DEFAULT_BOLD
            setTextColor(Color.GREEN)
        }

        onlineCard.addView(onlineTitle)

        statusText = TextView(this).apply {
            text = "Checking backend..."
            textSize = 14f
            setTextColor(Color.LTGRAY)
            setPadding(0, 10, 0, 0)
        }

        onlineCard.addView(statusText)

        rootLayout.addView(onlineCard)

        val commandCard = createCard()

        val commandTitle = TextView(this).apply {
            text = "COMMAND CENTER"
            textSize = 18f
            typeface = Typeface.DEFAULT_BOLD
            setTextColor(Color.WHITE)
        }

        commandCard.addView(commandTitle)

        commandInput = EditText(this).apply {
            hint = "Tell UDAAN what to do..."
            setTextColor(Color.WHITE)
            setHintTextColor(Color.GRAY)
            textSize = 16f
            setSingleLine(false)
            minLines = 2
            setPadding(20, 15, 20, 15)
            background = roundedBackground(
                Color.rgb(25, 25, 35),
                Color.rgb(70, 70, 90)
            )
        }

        commandCard.addView(commandInput)

        val executeButton = Button(this).apply {
            text = "EXECUTE COMMAND"
            textSize = 15f
            typeface = Typeface.DEFAULT_BOLD
            setTextColor(Color.WHITE)
            background = roundedBackground(
                Color.rgb(60, 20, 110),
                Color.rgb(130, 70, 220)
            )

            setOnClickListener {
                val command = commandInput.text.toString().trim()

                if (command.isEmpty()) {
                    statusText.text = "Enter a command first."
                } else {
                    statusText.text = "UDAAN is processing..."
                    sendCommand(command)
                }
            }
        }

        commandCard.addView(executeButton)

        rootLayout.addView(commandCard)

        addCard(
            "AI AGENTS",
            "Research • Content • Video • YouTube • Social • Analytics • Marketing • Developer • Automation • Creative"
        ) {
            showAgents()
        }

        addCard(
            "TASKS",
            "View active and pending UDAAN tasks"
        ) {
            showTasks()
        }

        addCard(
            "CONTENT & VIDEO",
            "Create scripts, content and video workflows"
        ) {
            showContent()
        }

        addCard(
            "FOUNDER APPROVAL",
            "Protected actions require your approval"
        ) {
            loadPendingApprovals()
        }

        val navigation = LinearLayout(this).apply {
            orientation = LinearLayout.HORIZONTAL
            gravity = Gravity.CENTER
            setPadding(8, 20, 8, 20)
        }

        navigation.addView(
            navButton("HOME") {
                showCommandCenter()
            }
        )

        navigation.addView(
            navButton("AGENTS") {
                showAgents()
            }
        )

        navigation.addView(
            navButton("TASKS") {
                showTasks()
            }
        )

        navigation.addView(
            navButton("CONTENT") {
                showContent()
            }
        )

        rootLayout.addView(navigation)

        setContentView(rootLayout)

        checkBackendStatus()
    }

    private fun createRoot(title: String): LinearLayout {

        val main = LinearLayout(this).apply {
            orientation = LinearLayout.VERTICAL
            setPadding(18, 20, 18, 20)
            setBackgroundColor(Color.rgb(7, 7, 15))
        }

        val header = LinearLayout(this).apply {
            orientation = LinearLayout.HORIZONTAL
            gravity = Gravity.CENTER_VERTICAL
        }

        val logo = ImageView(this).apply {
            setImageResource(R.drawable.udaan_logo)
            layoutParams = LinearLayout.LayoutParams(
                58,
                58
            ).apply {
                rightMargin = 14
            }
        }

        header.addView(logo)

        val titleView = TextView(this).apply {
            text = title
            textSize = 25f
            setTextColor(Color.WHITE)
            typeface = Typeface.DEFAULT_BOLD
        }

        header.addView(titleView)

        main.addView(header)

        val scroll = ScrollView(this)

        val content = LinearLayout(this).apply {
            orientation = LinearLayout.VERTICAL
        }

        scroll.addView(content)

        main.addView(
            scroll,
            LinearLayout.LayoutParams(
                LinearLayout.LayoutParams.MATCH_PARENT,
                0,
                1f
            )
        )

        rootLayout = content

        return main
    }

    private fun createCard(): LinearLayout {

        return LinearLayout(this).apply {
            orientation = LinearLayout.VERTICAL
            setPadding(20, 20, 20, 20)
            background = roundedBackground(
                Color.rgb(15, 15, 27),
                Color.rgb(55, 45, 90)
            )

            val params = LinearLayout.LayoutParams(
                LinearLayout.LayoutParams.MATCH_PARENT,
                LinearLayout.LayoutParams.WRAP_CONTENT
            )

            params.setMargins(0, 12, 0, 12)

            layoutParams = params
        }
    }

    private fun addCard(
        title: String,
        description: String,
        action: () -> Unit
    ) {

        val card = createCard()

        val titleView = TextView(this).apply {
            text = title
            textSize = 18f
            setTextColor(Color.WHITE)
            typeface = Typeface.DEFAULT_BOLD
        }

        card.addView(titleView)

        val descriptionView = TextView(this).apply {
            text = description
            textSize = 13f
            setTextColor(Color.LTGRAY)
            setPadding(0, 8, 0, 12)
        }

        card.addView(descriptionView)

        val button = Button(this).apply {
            text = "OPEN"
            setTextColor(Color.WHITE)
            background = roundedBackground(
                Color.rgb(30, 20, 55),
                Color.rgb(90, 60, 140)
            )

            setOnClickListener {
                action()
            }
        }

        card.addView(button)

        rootLayout.addView(card)
    }

    private fun navButton(
        text: String,
        action: () -> Unit
    ): Button {

        return Button(this).apply {
            this.text = text
            textSize = 11f
            setTextColor(Color.WHITE)
            background = roundedBackground(
                Color.rgb(25, 20, 40),
                Color.rgb(65, 50, 90)
            )

            setOnClickListener {
                action()
            }

            layoutParams = LinearLayout.LayoutParams(
                0,
                LinearLayout.LayoutParams.WRAP_CONTENT,
                1f
            ).apply {
                setMargins(3, 0, 3, 0)
            }
        }
    }

    private fun roundedBackground(
        fillColor: Int,
        strokeColor: Int
    ): GradientDrawable {

        return GradientDrawable().apply {
            shape = GradientDrawable.RECTANGLE
            cornerRadius = 24f
            setColor(fillColor)
            setStroke(2, strokeColor)
        }
    }

    private fun showAgents() {

        rootLayout = createRoot("AI AGENTS")

        val heading = TextView(this).apply {
            text = "UDAAN AI AGENTS"
            textSize = 25f
            typeface = Typeface.DEFAULT_BOLD
            setTextColor(Color.WHITE)
            gravity = Gravity.CENTER
            setPadding(10, 25, 10, 20)
        }

        rootLayout.addView(heading)

        if (dynamicAgents.isEmpty()) {

            val empty = TextView(this).apply {
                text = "Loading AI Agents..."
                textSize = 16f
                setTextColor(Color.LTGRAY)
                gravity = Gravity.CENTER
                setPadding(20, 50, 20, 50)
            }

            rootLayout.addView(empty)

        } else {

            dynamicAgents.forEach { agent ->

                val card = createCard()

                val button = Button(this).apply {
                    text = "${agent.name}\n${agent.status}"
                    textSize = 16f
                    setTextColor(Color.WHITE)
                    background = roundedBackground(
                        Color.rgb(20, 18, 35),
                        Color.rgb(80, 60, 130)
                    )

                    setOnClickListener {
                        openAgent(agent)
                    }
                }

                card.addView(button)

                val description = TextView(this).apply {
                    text = agent.description
                    textSize = 13f
                    setTextColor(Color.LTGRAY)
                    setPadding(5, 10, 5, 5)
                }

                card.addView(description)

                rootLayout.addView(card)
            }
        }

        val back = navButton("HOME") {
            showCommandCenter()
        }

        rootLayout.addView(back)

        setContentView(rootLayout)
    }

    private fun openAgent(agent: UdaanAgent) {

        rootLayout = createRoot(agent.name)

        val title = TextView(this).apply {
            text = agent.name
            textSize = 28f
            setTextColor(Color.WHITE)
            typeface = Typeface.DEFAULT_BOLD
            gravity = Gravity.CENTER
            setPadding(15, 30, 15, 15)
        }

        rootLayout.addView(title)

        val card = createCard()

        val info = TextView(this).apply {
            text =
                "MODULE: ${agent.module}\n\n" +
                "STATUS: ${agent.status}\n\n" +
                "DESCRIPTION:\n${agent.description}\n\n" +
                "FUNCTIONS:\n${agent.functions.joinToString("\n")}"

            textSize = 14f
            setTextColor(Color.LTGRAY)
        }

        card.addView(info)

        rootLayout.addView(card)

        val input = EditText(this).apply {
            hint = "Command for ${agent.name}..."
            setTextColor(Color.WHITE)
            setHintTextColor(Color.GRAY)
            setPadding(20, 15, 20, 15)
            background = roundedBackground(
                Color.rgb(20, 20, 30),
                Color.rgb(70, 60, 100)
            )
        }

        rootLayout.addView(input)

        val execute = Button(this).apply {
            text = "RUN AGENT"
            setTextColor(Color.WHITE)
            background = roundedBackground(
                Color.rgb(60, 20, 110),
                Color.rgb(130, 70, 220)
            )

            setOnClickListener {

                val command = input.text.toString().trim()

                if (command.isNotEmpty()) {
                    sendCommand(command)
                }
            }
        }

        rootLayout.addView(execute)

        rootLayout.addView(
            navButton("BACK TO AGENTS") {
                showAgents()
            }
        )

        setContentView(rootLayout)
    }

    private fun showTasks() {

        rootLayout = createRoot("TASKS")

        val title = TextView(this).apply {
            text = "UDAAN TASKS"
            textSize = 25f
            setTextColor(Color.WHITE)
            typeface = Typeface.DEFAULT_BOLD
            gravity = Gravity.CENTER
            setPadding(15, 30, 15, 20)
        }

        rootLayout.addView(title)

        val card = createCard()

        val text = TextView(this).apply {
            text = "Task Manager\n\nActive tasks and Founder Approval tasks will appear here."
            textSize = 16f
            setTextColor(Color.LTGRAY)
        }

        card.addView(text)

        rootLayout.addView(card)

        rootLayout.addView(
            navButton("HOME") {
                showCommandCenter()
            }
        )

        setContentView(rootLayout)
    }

    private fun showContent() {

        rootLayout = createRoot("CONTENT")

        val title = TextView(this).apply {
            text = "CONTENT & VIDEO STUDIO"
            textSize = 24f
            setTextColor(Color.WHITE)
            typeface = Typeface.DEFAULT_BOLD
            gravity = Gravity.CENTER
            setPadding(15, 30, 15, 20)
        }

        rootLayout.addView(title)

        addCard(
            "CONTENT AI",
            "Scripts, captions, ideas and content strategy"
        ) {
            sendCommand("Create content using Content AI")
        }

        addCard(
            "VIDEO AI",
            "Video production and rendering workflow"
        ) {
            sendCommand("Create a test video using Video AI")
        }

        addCard(
            "YOUTUBE AI",
            "YouTube research, upload and publishing workflow"
        ) {
            sendCommand("Show YouTube workflow")
        }

        addCard(
            "SOCIAL MEDIA AI",
            "Instagram and social media workflow"
        ) {
            sendCommand("Show social media workflow")
        }

        rootLayout.addView(
            navButton("HOME") {
                showCommandCenter()
            }
        )

        setContentView(rootLayout)
    }

    private fun loadDynamicAgents() {

        val request = Request.Builder()
            .url("$backendUrl/agents")
            .addHeader(
                "X-Udaan-API-Key",
                founderApiKey
            )
            .get()
            .build()

        client.newCall(request).enqueue(object : Callback {

            override fun onFailure(
                call: Call,
                e: IOException
            ) {

                runOnUiThread {
                    statusText.text =
                        "Agent discovery failed: ${e.message}"
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
                            "Agent discovery failed: HTTP ${response.code}"
                    }

                    return
                }

                try {

                    val json = JSONObject(body)
                    val array = json.optJSONArray("agents")

                    val newAgents = mutableListOf<UdaanAgent>()

                    if (array != null) {

                        for (i in 0 until array.length()) {

                            val item = array.getJSONObject(i)

                            val functions =
                                mutableListOf<String>()

                            val functionArray =
                                item.optJSONArray("functions")

                            if (functionArray != null) {

                                for (j in 0 until functionArray.length()) {
                                    functions.add(
                                        functionArray.optString(j)
                                    )
                                }
                            }

                            newAgents.add(
                                UdaanAgent(
                                    name = item.optString("name"),
                                    module = item.optString("module"),
                                    description = item.optString("description"),
                                    status = item.optString("status"),
                                    functions = functions
                                )
                            )
                        }
                    }

                    runOnUiThread {

                        dynamicAgents.clear()
                        dynamicAgents.addAll(newAgents)

                        statusText.text =
                            "UDAAN CORE ONLINE • ${dynamicAgents.size} AI Agents detected"
                    }

                } catch (e: Exception) {

                    runOnUiThread {
                        statusText.text =
                            "Agent data error: ${e.message}"
                    }
                }
            }
        })
    }

    private fun sendCommand(command: String) {

        val json = JSONObject().apply {
            put("command", command)
        }

        
val requestBody =
    RequestBody.create(
        "application/json".toMediaType(),
        json.toString()
    )
        val request = Request.Builder()
            .url("$backendUrl/command")
            .addHeader(
                "X-Udaan-API-Key",
                founderApiKey
            )
            .post(requestBody)
            .build()

        client.newCall(request).enqueue(object : Callback {

            override fun onFailure(
                call: Call,
                e: IOException
            ) {

                runOnUiThread {
                    statusText.text =
                        "Backend connection failed: ${e.message}"
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

                        statusText.text =
                            "UDAAN RESPONSE:\n$body"

                    } else {

                        statusText.text =
                            "Command failed: HTTP ${response.code}\n$body"
                    }
                }
            }
        })
    }

    private fun loadPendingApprovals() {

        val request = Request.Builder()
            .url("$backendUrl/approvals")
            .addHeader(
                "X-Udaan-API-Key",
                founderApiKey
            )
            .get()
            .build()

        client.newCall(request).enqueue(object : Callback {

            override fun onFailure(
                call: Call,
                e: IOException
            ) {

                runOnUiThread {
                    statusText.text =
                        "Approval connection failed."
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

                    statusText.text =
                        if (response.isSuccessful) {
                            "FOUNDER APPROVALS:\n$body"
                        } else {
                            "Approval request failed: HTTP ${response.code}"
                        }
                }
            }
        })
    }

    private fun checkBackendStatus() {

        val request = Request.Builder()
            .url("$backendUrl/health")
            .addHeader(
                "X-Udaan-API-Key",
                founderApiKey
            )
            .get()
            .build()

        client.newCall(request).enqueue(object : Callback {

            override fun onFailure(
                call: Call,
                e: IOException
            ) {

                runOnUiThread {
                    statusText.text =
                        "● BACKEND OFFLINE"
                }
            }

            override fun onResponse(
                call: Call,
                response: Response
            ) {

                runOnUiThread {

                    if (response.isSuccessful) {
                        statusText.text =
                            "● UDAAN CORE ONLINE"
                    } else {
                        statusText.text =
                            "● BACKEND ERROR: ${response.code}"
                    }
                }
            }
        })
    }
}
