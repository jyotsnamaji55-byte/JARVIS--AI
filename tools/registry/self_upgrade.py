from tools.self_upgrade.engine import SelfUpgradeEngine


def register_self_upgrade_tools(registry):
    engine = SelfUpgradeEngine()

    def upgrade_with_approval(request):
        preview = engine.prepare_upgrade(request)

        if not preview["success"]:
            return preview

        return engine.apply_approved_upgrade(preview)

    registry.register(
        "self_upgrade_prepare",
        "Prepare and safely apply a JARVIS project upgrade with AI generation, approval, verification, and rollback.",
        upgrade_with_approval
    )
