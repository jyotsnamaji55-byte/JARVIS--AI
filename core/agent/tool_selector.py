class ToolSelector:
    def select(self, goal, registry):
        text = goal.lower()
        selected = []

        if any(word in text for word in ["upgrade", "improve yourself", "self upgrade", "update yourself"]):
            if registry.has("self_upgrade_prepare"):
                selected.append("self_upgrade_prepare")

        if any(word in text for word in ["github", "workflow", "actions"]):
            if registry.has("github_trigger_workflow"):
                selected.append("github_trigger_workflow")

        if any(word in text for word in ["code", "python", "program", "script"]):
            if registry.has("generate_code"):
                selected.append("generate_code")

        if any(word in text for word in ["read", "open", "show file"]):
            if registry.has("read_code"):
                selected.append("read_code")

        if any(word in text for word in ["save", "write", "create file"]):
            if registry.has("save_code"):
                selected.append("save_code")

        return selected
