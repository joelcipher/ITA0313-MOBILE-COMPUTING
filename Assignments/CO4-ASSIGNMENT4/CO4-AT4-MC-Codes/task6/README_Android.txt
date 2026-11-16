For an Android implementation:
1. Encrypt each record with AndroidKeystoreAesGcm.kt before inserting it into the durable queue.
2. Upload only ciphertext or an authenticated payload over HTTPS.
3. Validate the server certificate/hostname using the platform TLS stack.
4. Delete/mark records only after the server acknowledges the sequence number.
5. Use WorkManager for deferrable sync; use a bounded foreground service only for
   an active, user-visible tracking session and subject to Android background policy.
