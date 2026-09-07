from tools.registry.manager import ToolRegistry
from tools.coding_engine import generate_and_validate, save_generated_code, read_code


def create_default_registry():
    registry = ToolRegistry()

    registry.register(
        "generate_code",
        "Generate and validate Python code from a request.",
        generate_and_validate
    )

    registry.register(
        "save_code",
        "Save validated Python code inside the coding workspace.",
        save_generated_code
    )

    registry.register(
        "read_code",
        "Read a file from the coding workspace.",
        read_code
    )

    return registry
