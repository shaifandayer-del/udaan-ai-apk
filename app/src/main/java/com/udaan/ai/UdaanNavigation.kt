package com.udaan.ai

import android.app.Activity

object UdaanNavigation {

    fun goHome(activity: Activity) {
        if (activity is MainActivity) {
            activity.showHome()
        }
    }

    fun goAgents(activity: Activity) {
        if (activity is MainActivity) {
            activity.showAgents()
        }
    }

    fun goTasks(activity: Activity) {
        if (activity is MainActivity) {
            activity.showTasks()
        }
    }

    fun goContent(activity: Activity) {
        if (activity is MainActivity) {
            activity.showContentStudio()
        }
    }

    fun goAnalytics(activity: Activity) {
        if (activity is MainActivity) {
            activity.showAnalytics()
        }
    }

    fun goApprovals(activity: Activity) {
        if (activity is MainActivity) {
            activity.showApprovals()
        }
    }

    fun goSystem(activity: Activity) {
        if (activity is MainActivity) {
            activity.showSystem()
        }
    }
}
