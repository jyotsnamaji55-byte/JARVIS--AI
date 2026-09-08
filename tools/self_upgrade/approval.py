def request_approval(target_file):
    print()
    print("===== JARVIS UPGRADE APPROVAL =====")
    print(f"Target: {target_file}")
    print("AI has prepared a proposed upgrade.")
    print("No changes have been applied yet.")
    print()

    answer = input("Apply this upgrade? (yes/no): ").strip().lower()

    if answer == "yes":
        return True

    return False
