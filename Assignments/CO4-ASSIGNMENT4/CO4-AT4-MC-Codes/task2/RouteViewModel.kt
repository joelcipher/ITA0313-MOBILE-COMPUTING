// Android/Kotlin pattern for a bounded background computation.
// Dependencies: lifecycle-viewmodel-ktx and Kotlin coroutines.
class RouteViewModel : ViewModel() {
    private val _result = MutableStateFlow<String>("Idle")
    val result: StateFlow<String> = _result

    fun parseRoute(input: ByteArray) {
        viewModelScope.launch {
            _result.value = "Working"
            val parsed = withContext(Dispatchers.Default) {
                // Replace with deterministic route parsing.
                input.sumOf { it.toInt() and 0xFF }.toString()
            }
            _result.value = parsed
        }
    }
}

// For a tiny workload, do not create a new thread per call.
// Reuse a bounded dispatcher/executor and measure whether hand-off overhead is justified.
