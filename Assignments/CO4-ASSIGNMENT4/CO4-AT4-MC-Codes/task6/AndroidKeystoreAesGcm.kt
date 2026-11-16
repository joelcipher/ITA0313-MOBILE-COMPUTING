// Android example: AES-GCM key held in Android Keystore.
// Store ciphertext + IV; never store the key in source code or preferences.
fun getOrCreateAesKey(alias: String): SecretKey {
    val ks = KeyStore.getInstance("AndroidKeyStore").apply { load(null) }
    val existing = ks.getKey(alias, null) as? SecretKey
    if (existing != null) return existing

    val generator = KeyGenerator.getInstance(
        KeyProperties.KEY_ALGORITHM_AES, "AndroidKeyStore"
    )
    val spec = KeyGenParameterSpec.Builder(
        alias,
        KeyProperties.PURPOSE_ENCRYPT or KeyProperties.PURPOSE_DECRYPT
    )
        .setBlockModes(KeyProperties.BLOCK_MODE_GCM)
        .setEncryptionPaddings(KeyProperties.ENCRYPTION_PADDING_NONE)
        .setRandomizedEncryptionRequired(true)
        .build()
    generator.init(spec)
    return generator.generateKey()
}

data class EncryptedRecord(val iv: ByteArray, val ciphertext: ByteArray)

fun encryptRecord(alias: String, plainText: ByteArray): EncryptedRecord {
    val cipher = Cipher.getInstance("AES/GCM/NoPadding")
    cipher.init(Cipher.ENCRYPT_MODE, getOrCreateAesKey(alias))
    return EncryptedRecord(cipher.iv, cipher.doFinal(plainText))
}
