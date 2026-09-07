class RecoveryEngine:
    def __init__(self, max_retries=2):
        self.max_retries = max_retries

    def should_retry(self, result, attempt):
        if attempt >= self.max_retries:
            return False

        if not result:
            return True

        if result.get("success") is False:
            return True

        return False

    def describe_recovery(self, result, attempt):
        error = result.get("error", "Unknown error.")

        return {
            "attempt": attempt,
            "action": "retry",
            "reason": error
        }
