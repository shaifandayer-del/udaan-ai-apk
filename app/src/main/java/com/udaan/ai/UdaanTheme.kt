package com.udaan.ai

import android.graphics.Color

object UdaanTheme {

    const val BACKGROUND = "#07070F"
    const val SURFACE = "#10101C"
    const val CARD = "#151526"
    const val PRIMARY = "#8A4DFF"
    const val SECONDARY = "#00D9FF"
    const val SUCCESS = "#00E676"
    const val WARNING = "#FFB300"
    const val ERROR = "#FF4D6D"
    const val TEXT_PRIMARY = "#FFFFFF"
    const val TEXT_SECONDARY = "#A9A9C2"

    fun color(hex: String): Int {
        return Color.parseColor(hex)
    }
}
