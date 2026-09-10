package com.udaan.ai

import android.app.Activity
import android.os.Bundle
import android.widget.Button
import android.widget.EditText
import android.widget.LinearLayout
import android.widget.TextView

class MainActivity : Activity() {

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)

        val layout = LinearLayout(this).apply {
            orientation = LinearLayout.VERTICAL
            setPadding(40, 60, 40, 40)
        }

        val title = TextView(this).apply {
            text = "UDAAN AI"
            textSize = 28f
        }

        val commandInput = EditText(this).apply {
            hint = "Enter UDAAN command"
            textSize = 18f
        }

        val sendButton = Button(this).apply {
            text = "SEND COMMAND"
        }

        val response = TextView(this).apply {
            text = "UDAAN AI\n\nReady for your command."
            textSize = 18f
            setPadding(0, 40, 0, 0)
        }

        layout.addView(title)
        layout.addView(commandInput)
        layout.addView(sendButton)
        layout.addView(response)

        setContentView(layout)

        sendButton.setOnClickListener {
            val command = commandInput.text.toString().trim()

            response.text = if (command.isEmpty()) {
                "Please enter a command."
            } else {
                "UDAAN AI received:\n\n$command"
            }
        }
    }
}
