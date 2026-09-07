from tools.github.actions import trigger_workflow


def register_github_tools(registry):
    registry.register(
        "github_trigger_workflow",
        "Trigger a GitHub Actions workflow.",
        trigger_workflow
    )
