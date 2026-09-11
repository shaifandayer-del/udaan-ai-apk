package com.udaan.ai

import android.graphics.Color
import android.graphics.Typeface
import android.graphics.drawable.GradientDrawable
import android.os.Bundle
import android.view.Gravity
import android.widget.*
import androidx.appcompat.app.AppCompatActivity
import okhttp3.*
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
            text = "U D A A N"
            textSize = 32f
            setTextColor(Color.WHITE)
            typeface = Typeface.create(
                Typeface.DEFAULT,
                Typeface.BOLD
            )
            gravity = Gravity.CENTER
            letterSpacing = 0.12f
            setPadding(10, 28, 10, 4)
        }

        rootLayout.addView(hero)

        val heroSub = TextView(this).apply {
            text = "ARTIFICIAL INTELLIGENCE COMMAND SYSTEM"
            textSize = 11f
            setTextColor(Color.rgb(170, 150, 220))
            gravity = Gravity.CENTER
            letterSpacing = 0.08f
            setPadding(10, 0, 10, 22)
        }

        rootLayout.addView(heroSub)

        val coreCard = createGlowCard()

        val coreTitle = TextView(this).apply {
            text = "◉  UDAAN CORE"
            textSize = 20f
            setTextColor(Color.rgb(80, 255, 120))
            typeface = Typeface.DEFAULT_BOLD
        }

        coreCard.addView(coreTitle)

        statusText = TextView(this).apply {
            text = "CONNECTING TO UDAAN CORE..."
            textSize = 14f
            setTextColor(Color.LTGRAY)
            setPadding(0, 10, 0, 0)
        }

        coreCard.addView(statusText)

        rootLayout.addView(coreCard)

        val commandCard = createGlowCard()

        val commandTitle = TextView(this).apply {
            text = "COMMAND CENTER"
            textSize = 20f
            setTextColor(Color.WHITE)
            typeface = Typeface.DEFAULT_BOLD
        }

        commandCard.addView(commandTitle)

        val commandSub = TextView(this).apply {
            text = "Give UDAAN a command"
            textSize = 12f
            setTextColor(Color.GRAY)
            setPadding(0, 5, 0, 14)
        }

        commandCard.addView(commandSub)

        commandInput = EditText(this).apply {
            hint = "What should UDAAN do?"
            textSize = 16f
            setTextColor(Color.WHITE)
            setHintTextColor(Color.rgb(125, 125, 140))
            gravity = Gravity.TOP
            minLines = 3
            setPadding(18, 16, 18, 16)

            background = roundedBackground(
                Color.rgb(16, 16, 28),
                Color.rgb(105, 70, 170)
            )
        }

        commandCard.addView(commandInput)

        val executeButton = futuristicButton(
            "⚡  EXECUTE COMMAND"
        )

        executeButton.setOnClickListener {

            val command =
                commandInput.text.toString().trim()

            if (command.isEmpty()) {

                statusText.text =
                    "Please enter a command."

            } else {

                statusText.text =
                    "UDAAN CORE PROCESSING..."

                sendCommand(command)
            }
        }

        commandCard.addView(executeButton)

        rootLayout.addView(commandCard)

        addFeatureCard(
            "AI AGENTS",
            "10 intelligent agents • Dynamic discovery • Specialized AI",
            "OPEN AGENTS"
        ) {
            showAgents()
        }

        addFeatureCard(
            "TASK CONTROL",
            "Monitor active tasks and Founder Approval operations",
            "OPEN TASKS"
        ) {
            showTasks()
        }

        addFeatureCard(
            "CONTENT STUDIO",
            "Content • Video • YouTube • Social Media",
            "OPEN STUDIO"
        ) {
            showContent()
        }

        addFeatureCard(
            "FOUNDER CONTROL",
            "Protected actions require Founder approval",
            "OPEN APPROVALS"
        ) {
            loadPendingApprovals()
        }

        val section = TextView(this).apply {
            text = "SYSTEM MODULES"
            textSize = 13f
            setTextColor(Color.rgb(150, 130, 190))
            typeface = Typeface.DEFAULT_BOLD
            letterSpacing = 0.08f
            setPadding(5, 20, 5, 8)
        }

        rootLayout.addView(section)

        val modules = arrayOf(
            "RESEARCH AI",
            "CONTENT AI",
            "VIDEO AI",
            "YOUTUBE AI",
            "SOCIAL MEDIA AI",
            "ANALYTICS AI",
            "MARKETING AI",
            "DEVELOPER AI",
            "AUTOMATION AI",
            "CREATIVE AI"
        )

        modules.forEach { module ->

            val moduleView = TextView(this).apply {
                text = "◆  $module"
                textSize = 13f
                setTextColor(Color.LTGRAY)
                setPadding(12, 10, 12, 10)

                background = roundedBackground(
                    Color.rgb(12, 12, 22),
                    Color.rgb(45, 35, 70)
                )
            }

            val params =
                LinearLayout.LayoutParams(
                    LinearLayout.LayoutParams.MATCH_PARENT,
                    LinearLayout.LayoutParams.WRAP_CONTENT
                )

            params.setMargins(0, 4, 0, 4)

            rootLayout.addView(
                moduleView,
                params
            )
        }

        val navigation = LinearLayout(this).apply {
            orientation = LinearLayout.HORIZONTAL
            gravity = Gravity.CENTER
            setPadding(0, 22, 0, 15)
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
            navButton("STUDIO") {
                showContent()
            }
        )

        rootLayout.addView(navigation)

        setContentView(rootLayout)

        checkBackendStatus()
    }

    private fun createRoot(
        title: String
    ): LinearLayout {

        val main = LinearLayout(this).apply {
            orientation = LinearLayout.VERTICAL
            setPadding(16, 14, 16, 12)
            setBackgroundColor(
                Color.rgb(5, 5, 12)
            )
        }

        val header = LinearLayout(this).apply {
            orientation = LinearLayout.HORIZONTAL
            gravity = Gravity.CENTER_VERTICAL
        }

        val logo = ImageView(this).apply {

            setImageResource(
                R.drawable.udaan_logo
            )

            layoutParams =
                LinearLayout.LayoutParams(
                    62,
                    62
                ).apply {
                    rightMargin = 12
                }
        }

        header.addView(logo)

        val titleView = TextView(this).apply {
            text = title
            textSize = 24f
            setTextColor(Color.WHITE)
            typeface = Typeface.DEFAULT_BOLD
            letterSpacing = 0.03f
        }

        header.addView(titleView)

        main.addView(header)

        val divider = TextView(this).apply {
            text = "━━━━━━━━━━━━━━━━━━━━━━━━"
            textSize = 10f
            setTextColor(Color.rgb(65, 45, 100))
            setPadding(0, 2, 0, 3)
        }

        main.addView(divider)

        val scroll = ScrollView(this)

        val content = LinearLayout(this).apply {
            orientation = LinearLayout.VERTICAL
            setPadding(2, 0, 2, 10)
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

    private fun createGlowCard(): LinearLayout {

        return LinearLayout(this).apply {

            orientation = LinearLayout.VERTICAL

            setPadding(
                18,
                18,
                18,
                18
            )

            background = roundedBackground(
                Color.rgb(12, 12, 23),
                Color.rgb(65, 45, 105)
            )

            val params =
                LinearLayout.LayoutParams(
                    LinearLayout.LayoutParams.MATCH_PARENT,
                    LinearLayout.LayoutParams.WRAP_CONTENT
                )

            params.setMargins(
                0,
                8,
                0,
                8
            )

            layoutParams = params
        }
    }

    private fun addFeatureCard(
        title: String,
        description: String,
        buttonText: String,
        action: () -> Unit
    ) {

        val card = createGlowCard()

        val titleView = TextView(this).apply {
            text = title
            textSize = 19f
            setTextColor(Color.WHITE)
            typeface = Typeface.DEFAULT_BOLD
        }

        card.addView(titleView)

        val descriptionView = TextView(this).apply {
            text = description
            textSize = 13f
            setTextColor(Color.LTGRAY)
            setPadding(
                0,
                7,
                0,
                12
            )
        }

        card.addView(descriptionView)

        val button =
            futuristicButton(buttonText)

        button.setOnClickListener {
            action()
        }

        card.addView(button)

        rootLayout.addView(card)
    }

    private fun futuristicButton(
        textValue: String
    ): Button {

        return Button(this).apply {

            text = textValue

            textSize = 14f

            setTextColor(Color.WHITE)

            typeface = Typeface.DEFAULT_BOLD

            background = roundedBackground(
                Color.rgb(52, 20, 90),
                Color.rgb(125, 65, 210)
            )

            minHeight = 55

            stateListAnimator = null

            layoutParams =
                LinearLayout.LayoutParams(
                    LinearLayout.LayoutParams.MATCH_PARENT,
                    LinearLayout.LayoutParams.WRAP_CONTENT
                ).apply {
                    setMargins(
                        0,
                        5,
                        0,
                        3
                    )
                }
        }
    }

    private fun navButton(
        textValue: String,
        action: () -> Unit
    ): Button {

        return Button(this).apply {

            text = textValue

            textSize = 10f

            setTextColor(Color.WHITE)

            typeface = Typeface.DEFAULT_BOLD

            background = roundedBackground(
                Color.rgb(15, 13, 25),
                Color.rgb(70, 50, 100)
            )

            setOnClickListener {
                action()
            }

            layoutParams =
                LinearLayout.LayoutParams(
                    0,
                    LinearLayout.LayoutParams.WRAP_CONTENT,
                    1f
                ).apply {
                    setMargins(
                        3,
                        0,
                        3,
                        0
                    )
                }
        }
    }

    private fun roundedBackground(
        fillColor: Int,
        strokeColor: Int
    ): GradientDrawable {

        return GradientDrawable().apply {

            shape =
                GradientDrawable.RECTANGLE

            cornerRadius = 28f

            setColor(fillColor)

            setStroke(
                2,
                strokeColor
            )
        }
    }

    private fun showAgents() {

        rootLayout =
            createRoot("AI AGENTS")

        val heading = TextView(this).apply {

            text = "UDAAN AI AGENTS"

            textSize = 27f

            setTextColor(Color.WHITE)

            typeface = Typeface.DEFAULT_BOLD

            gravity = Gravity.CENTER

            setPadding(
                10,
                22,
                10,
                18
            )
        }

        rootLayout.addView(heading)

        val count = TextView(this).apply {

            text =
                "${dynamicAgents.size} AI AGENTS CONNECTED"

            textSize = 12f

            setTextColor(
                Color.rgb(100, 255, 150)
            )

            gravity = Gravity.CENTER

            setPadding(
                5,
                0,
                5,
                18
            )
        }

        rootLayout.addView(count)

        if (dynamicAgents.isEmpty()) {

            val loading = TextView(this).apply {

                text =
                    "DISCOVERING UDAAN AI AGENTS..."

                textSize = 16f

                setTextColor(Color.LTGRAY)

                gravity = Gravity.CENTER

                setPadding(
                    20,
                    60,
                    20,
                    60
                )
            }

            rootLayout.addView(loading)

        } else {

            dynamicAgents.forEach { agent ->

                val card = createGlowCard()

                val name = TextView(this).apply {

                    text =
                        "◆  ${agent.name}"

                    textSize = 18f

                    setTextColor(Color.WHITE)

                    typeface =
                        Typeface.DEFAULT_BOLD
                }

                card.addView(name)

                val status = TextView(this).apply {

                    text =
                        "● ${agent.status}"

                    textSize = 12f

                    setTextColor(
                        if (
                            agent.status
                                .equals(
                                    "ONLINE",
                                    true
                                )
                        ) {
                            Color.GREEN
                        } else {
                            Color.RED
                        }
                    )

                    setPadding(
                        0,
                        5,
                        0,
                        5
                    )
                }

                card.addView(status)

                val description =
                    TextView(this).apply {

                        text =
                            agent.description

                        textSize = 13f

                        setTextColor(
                            Color.LTGRAY
                        )

                        setPadding(
                            0,
                            3,
                            0,
                            10
                        )
                    }

                card.addView(description)

                val open =
                    futuristicButton(
                        "OPEN AGENT"
                    )

                open.setOnClickListener {
                    openAgent(agent)
                }

                card.addView(open)

                rootLayout.addView(card)
            }
        }

        rootLayout.addView(
            navButton("HOME") {
                showCommandCenter()
            }
        )

        setContentView(rootLayout)
    }

    private fun openAgent(
        agent: UdaanAgent
    ) {

        rootLayout =
            createRoot(agent.name)

        val title = TextView(this).apply {

            text = agent.name

            textSize = 28f

            setTextColor(Color.WHITE)

            typeface = Typeface.DEFAULT_BOLD

            gravity = Gravity.CENTER

            setPadding(
                10,
                25,
                10,
                18
            )
        }

        rootLayout.addView(title)

        val infoCard = createGlowCard()

        val info = TextView(this).apply {

            text =
                "MODULE\n${agent.module}\n\n" +
                "STATUS\n${agent.status}\n\n" +
                "DESCRIPTION\n${agent.description}\n\n" +
                "FUNCTIONS\n" +
                agent.functions.joinToString(
                    "\n"
                )

            textSize = 14f

            setTextColor(Color.LTGRAY)

            setLineSpacing(
                2f,
                1f
            )
        }

        infoCard.addView(info)

        rootLayout.addView(infoCard)

        val input =
            EditText(this).apply {

                hint =
                    "Command for ${agent.name}"

                textSize = 15f

                setTextColor(Color.WHITE)

                setHintTextColor(
                    Color.GRAY
                )

                setPadding(
                    18,
                    16,
                    18,
                    16
                )

                background =
                    roundedBackground(
                        Color.rgb(
                            14,
                            14,
                            25
                        ),
                        Color.rgb(
                            90,
                            60,
                            140
                        )
                    )
            }

        rootLayout.addView(input)

        val run =
            futuristicButton(
                "⚡ RUN AGENT"
            )

        run.setOnClickListener {

            val command =
                input.text.toString().trim()

            if (command.isNotEmpty()) {

                sendCommand(command)

            } else {

                statusText.text =
                    "Enter an agent command."
            }
        }

        rootLayout.addView(run)

        rootLayout.addView(
            navButton("BACK TO AGENTS") {
                showAgents()
            }
        )

        setContentView(rootLayout)
    }

    private fun showTasks() {

        rootLayout =
            createRoot("TASK CONTROL")

        val title = TextView(this).apply {

            text = "TASK CONTROL"

            textSize = 27f

            setTextColor(Color.WHITE)

            typeface = Typeface.DEFAULT_BOLD

            gravity = Gravity.CENTER

            setPadding(
                10,
                25,
                10,
                20
            )
        }

        rootLayout.addView(title)

        addFeatureCard(
            "ACTIVE TASKS",
            "UDAAN Task Manager active operations",
            "REFRESH TASKS"
        ) {
            statusText.text =
                "Task system connected."
        }

        addFeatureCard(
            "FOUNDER APPROVAL",
            "Protected commands waiting for your approval",
            "OPEN APPROVALS"
        ) {
            loadPendingApprovals()
        }

        rootLayout.addView(
            navButton("HOME") {
                showCommandCenter()
            }
        )

        setContentView(rootLayout)
    }

    private fun showContent() {

        rootLayout =
            createRoot("AI STUDIO")

        val title = TextView(this).apply {

            text = "UDAAN AI STUDIO"

            textSize = 27f

            setTextColor(Color.WHITE)

            typeface = Typeface.DEFAULT_BOLD

            gravity = Gravity.CENTER

            setPadding(
                10,
                25,
                10,
                20
            )
        }

        rootLayout.addView(title)

        addFeatureCard(
            "CONTENT AI",
            "Scripts • Captions • Ideas • Content Strategy",
            "OPEN CONTENT AI"
        ) {

            sendCommand(
                "Create content using Content AI"
            )
        }

        addFeatureCard(
            "VIDEO AI",
            "Production • Rendering • Video workflow",
            "OPEN VIDEO AI"
        ) {

            sendCommand(
                "Create a test video using Video AI"
            )
        }

        addFeatureCard(
            "YOUTUBE AI",
            "Research • Channel workflow • Publishing",
            "OPEN YOUTUBE AI"
        ) {

            sendCommand(
                "Show YouTube workflow"
            )
        }

        addFeatureCard(
            "SOCIAL MEDIA AI",
            "Instagram • Social content • Publishing",
            "OPEN SOCIAL AI"
        ) {

            sendCommand(
                "Show social media workflow"
            )
        }

        rootLayout.addView(
            navButton("HOME") {
                showCommandCenter()
            }
        )

        setContentView(rootLayout)
    }

    private fun loadDynamicAgents() {

        val request =
            Request.Builder()
                .url("$backendUrl/agents")
                .addHeader(
                    "X-Udaan-API-Key",
                    founderApiKey
                )
                .get()
                .build()

        client.newCall(request)
            .enqueue(
                object : Callback {

                    override fun onFailure(
                        call: Call,
                        e: IOException
                    ) {

                        runOnUiThread {

                            statusText.text =
                                "Agent discovery failed"
                        }
                    }

                    override fun onResponse(
                        call: Call,
                        response: Response
                    ) {

                        val body =
                            response.body?.string()

                        if (
                            !response.isSuccessful ||
                            body == null
                        ) {

                            runOnUiThread {

                                statusText.text =
                                    "Agent discovery failed: HTTP ${response.code}"
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

                            val agents =
                                mutableListOf<UdaanAgent>()

                            if (array != null) {

                                for (
                                    i in
                                    0 until array.length()
                                ) {

                                    val item =
                                        array.getJSONObject(
                                            i
                                        )

                                    val functions =
                                        mutableListOf<String>()

                                    val functionArray =
                                        item.optJSONArray(
                                            "functions"
                                        )

                                    if (
                                        functionArray != null
                                    ) {

                                        for (
                                            j in
                                            0 until functionArray.length()
                                        ) {

                                            functions.add(
                                                functionArray
                                                    .optString(j)
                                            )
                                        }
                                    }

                                    agents.add(
                                        UdaanAgent(
                                            name =
                                                item.optString(
                                                    "name"
                                                ),
                                            module =
                                                item.optString(
                                                    "module"
                                                ),
                                            description =
                                                item.optString(
                                                    "description"
                                                ),
                                            status =
                                                item.optString(
                                                    "status"
                                                ),
                                            functions =
                                                functions
                                        )
                                    )
                                }
                            }

                            runOnUiThread {

                                dynamicAgents.clear()

                                dynamicAgents.addAll(
                                    agents
                                )

                                statusText.text =
                                    "UDAAN CORE ONLINE • ${dynamicAgents.size} AI AGENTS"
                            }

                        } catch (
                            e: Exception
                        ) {

                            runOnUiThread {

                                statusText.text =
                                    "Agent data error"
                            }
                        }
                    }
                }
            )
    }

    private fun sendCommand(
        command: String
    ) {

        val json =
            JSONObject().apply {
                put(
                    "command",
                    command
                )
            }

        val requestBody =
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
                .addHeader(
                    "X-Udaan-API-Key",
                    founderApiKey
                )
                .post(requestBody)
                .build()

        client.newCall(request)
            .enqueue(
                object : Callback {

                    override fun onFailure(
                        call: Call,
                        e: IOException
                    ) {

                        runOnUiThread {

                            statusText.text =
                                "Backend connection failed"
                        }
                    }

                    override fun onResponse(
                        call: Call,
                        response: Response
                    ) {

                        val body =
                            response.body
                                ?.string()
                                ?: ""

                        runOnUiThread {

                            if (
                                response.isSuccessful
                            ) {

                                statusText.text =
                                    "UDAAN RESPONSE\n$body"

                            } else {

                                statusText.text =
                                    "COMMAND ERROR ${response.code}\n$body"
                            }
                        }
                    }
                }
            )
    }

    private fun loadPendingApprovals() {

        val request =
            Request.Builder()
                .url(
                    "$backendUrl/approvals"
                )
                .addHeader(
                    "X-Udaan-API-Key",
                    founderApiKey
                )
                .get()
                .build()

        client.newCall(request)
            .enqueue(
                object : Callback {

                    override fun onFailure(
                        call: Call,
                        e: IOException
                    ) {

                        runOnUiThread {

                            statusText.text =
                                "Approval connection failed"
                        }
                    }

                    override fun onResponse(
                        call: Call,
                        response: Response
                    ) {

                        val body =
                            response.body
                                ?.string()
                                ?: ""

                        runOnUiThread {

                            statusText.text =
                                if (
                                    response.isSuccessful
                                ) {
                                    "FOUNDER APPROVALS\n$body"
                                } else {
                                    "Approval error: HTTP ${response.code}"
                                }
                        }
                    }
                }
            )
    }

    private fun checkBackendStatus() {

        val request =
            Request.Builder()
                .url(
                    "$backendUrl/health"
                )
                .addHeader(
                    "X-Udaan-API-Key",
                    founderApiKey
                )
                .get()
                .build()

        client.newCall(request)
            .enqueue(
                object : Callback {

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

                            if (
                                response.isSuccessful
                            ) {

                                statusText.text =
                                    "● UDAAN CORE ONLINE • READY"

                            } else {

                                statusText.text =
                                    "● BACKEND ERROR: ${response.code}"
                            }
                        }
                    }
                }
            )
    }
}
