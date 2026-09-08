from tools.self_upgrade.engine import SelfUpgradeEngine


def register_self_upgrade_tools(registry):
    engine = SelfUpgradeEngine()

    registry.register(
        "self_upgrade_prepare",
        "Prepare a safe JARVIS project upgrade with planning, checkpoint, and verification.",
        engine.prepare_upgrade
    )
