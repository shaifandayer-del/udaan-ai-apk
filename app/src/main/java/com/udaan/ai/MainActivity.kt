package com.udaan.ai

import android.app.Activity
import android.os.Bundle
import android.widget.Toast
import okhttp3.MediaType.Companion.toMediaType
import okhttp3.OkHttpClient
import okhttp3.Request
import okhttp3.RequestBody.Companion.toRequestBody
import java.util.concurrent.TimeUnit

class MainActivity : Activity() {

    private val client = OkHttpClient.Builder()
        .connectTimeout(10, TimeUnit.SECONDS)
        .readTimeout(30, TimeUnit.SECONDS)
        .build()

    private val backendUrl = "http://10.0.2.2:8080"
    private val founderApiKey = "YOUR_FOUNDER_API_KEY"

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)

        Toast.makeText(
            this,
            "UDAAN AI Starting...",
            Toast.LENGTH_LONG
        ).show()

        testBackendConnection()
    }

    private fun testBackendConnection() {
        Thread {
            try {
                val request = Request.Builder()
                    .url("$backendUrl/status")
                    .addHeader(
                        "X-Udaan-API-Key",
                        founderApiKey
                    )
                    .get()
                    .build()

                client.newCall(request).execute().use { response ->

                    runOnUiThread {

                        if (response.isSuccessful) {
                            Toast.makeText(
                                this,
                                "UDAAN Backend Connected",
                                Toast.LENGTH_LONG
                            ).show()
                        } else {
                            Toast.makeText(
                                this,
                                "Backend Error: ${response.code}",
                                Toast.LENGTH_LONG
                            ).show()
                        }
                    }
                }

            } catch (error: Exception) {

                runOnUiThread {
                    Toast.makeText(
                        this,
                        "Backend Connection Failed",
                        Toast.LENGTH_LONG
                    ).show()
                }
            }
        }.start()
    }
}
