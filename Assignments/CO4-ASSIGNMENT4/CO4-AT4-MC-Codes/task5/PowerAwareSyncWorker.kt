package com.example.mcassignment

import android.content.Context
import androidx.work.Constraints
import androidx.work.NetworkType
import androidx.work.OneTimeWorkRequestBuilder
import androidx.work.WorkManager
import androidx.work.Worker
import androidx.work.WorkerParameters
import androidx.work.Data

class PowerAwareSyncWorker(
    appContext: Context,
    params: WorkerParameters
) : Worker(appContext, params) {

    override fun doWork(): Result {
        return try {
            // 1. Read durable encrypted queue.
            // 2. Send a bounded batch over HTTPS.
            // 3. Validate server acknowledgement.
            // 4. Mark only acknowledged sequence numbers as delivered.
            // Replace this placeholder with repository/network implementation.
            Result.success(Data.Builder().putInt("uploaded_count", 0).build())
        } catch (e: java.io.IOException) {
            // WorkManager applies backoff for retryable network failures.
            Result.retry()
        } catch (e: Exception) {
            Result.failure()
        }
    }

    companion object {
        fun enqueue(context: Context) {
            val constraints = Constraints.Builder()
                .setRequiredNetworkType(NetworkType.CONNECTED)
                .build()

            val request = OneTimeWorkRequestBuilder<PowerAwareSyncWorker>()
                .setConstraints(constraints)
                .build()

            WorkManager.getInstance(context).enqueue(request)
        }
    }
}
