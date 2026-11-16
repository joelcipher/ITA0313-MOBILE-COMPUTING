package com.example.mcassignment

import android.os.Bundle
import android.os.Process
import android.util.Log
import androidx.appcompat.app.AppCompatActivity

class LifecycleLoggerActivity : AppCompatActivity() {
    private val tag = "LifeTrace"

    private fun trace(event: String, savedState: Bundle?) {
        Log.i(
            tag,
            "event=$event pid=${Process.myPid()} " +
            "savedStatePresent=${savedState != null} time=${System.currentTimeMillis()}"
        )
    }

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        trace("onCreate", savedInstanceState)
    }

    override fun onStart() {
        super.onStart()
        trace("onStart", null)
    }

    override fun onResume() {
        super.onResume()
        trace("onResume", null)
    }

    override fun onPause() {
        trace("onPause", null)
        super.onPause()
    }

    override fun onStop() {
        trace("onStop", null)
        super.onStop()
    }

    override fun onDestroy() {
        trace("onDestroy", null)
        super.onDestroy()
    }

    override fun onSaveInstanceState(outState: Bundle) {
        outState.putString("sample_state", "saved")
        trace("onSaveInstanceState", outState)
        super.onSaveInstanceState(outState)
    }
}
