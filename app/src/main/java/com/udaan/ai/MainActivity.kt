package com.udaan.ai

import android.app.Activity
import android.os.Bundle
import android.widget.TextView

class MainActivity : Activity() {

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)

        val text = TextView(this).apply {
            text = "UDAAN AI\n\nSystem Ready ✅"
            textSize = 28f
            setPadding(40, 80, 40, 40)
        }

        setContentView(text)
    }
}
