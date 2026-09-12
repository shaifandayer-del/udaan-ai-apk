package com.udaan.ai

data class UdaanAgent(
    val name: String,
    val description: String,
    val status: String
)

data class UdaanTask(
    val id: String,
    val title: String,
    val status: String
)

data class UdaanApproval(
    val id: String,
    val action: String,
    val agent: String,
    val status: String
)

data class UdaanCommandResult(
    val status: String,
    val message: String,
    val agent: String = "",
    val command: String = ""
)
