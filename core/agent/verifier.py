class ResultVerifier:
    def verify(self, result):
        if not isinstance(result, dict):
            return {
                "verified": False,
                "reason": "Invalid result format."
            }

        if result.get("success") is True:
            return {
                "verified": True,
                "reason": "Execution completed successfully."
            }

        return {
            "verified": False,
            "reason": result.get(
                "error",
                "Execution result could not be verified."
            )
        }

    def needs_recovery(self, verification):
        return not verification.get("verified", False)
