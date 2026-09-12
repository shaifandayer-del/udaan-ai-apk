package com.udaan.ai

import okhttp3.Call
import okhttp3.Callback
import okhttp3.OkHttpClient
import okhttp3.Request
import okhttp3.RequestBody
import okhttp3.Response
import java.io.IOException

object UdaanApiClient {

    private const val BASE_URL =
        "https://udaan-ai-apk-1.onrender.com"

    private val client =
        OkHttpClient()

    fun get(
        path: String,
        apiKey: String,
        callback: (Boolean, String) -> Unit
    ) {
        val request = Request.Builder()
            .url(BASE_URL + path)
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
                    callback(
                        false,
                        e.message ?: "Network error"
                    )
                }

                override fun onResponse(
                    call: Call,
                    response: Response
                ) {
                    response.use {

                        val body =
                            it.body?.string() ?: ""

                        callback(
                            it.isSuccessful,
                            body
                        )
                    }
                }
            })
    }

    fun post(
        path: String,
        apiKey: String,
        body: RequestBody,
        callback: (Boolean, String) -> Unit
    ) {
        val request = Request.Builder()
            .url(BASE_URL + path)
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
                    callback(
                        false,
                        e.message ?: "Network error"
                    )
                }

                override fun onResponse(
                    call: Call,
                    response: Response
                ) {
                    response.use {

                        val result =
                            it.body?.string() ?: ""

                        callback(
                            it.isSuccessful,
                            result
                        )
                    }
                }
            })
    }
}
