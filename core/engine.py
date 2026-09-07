class JarvisEngine:
    def __init__(self):
        self.name = "JARVIS"

    def respond(self, text):
        command = text.strip().lower()

        if command == "hello":
            return "Hello! JARVIS is ready."
        elif command == "help":
            return "Commands: hello, help, status, exit"
        elif command == "status":
            return "JARVIS system is online."
        elif command == "exit":
            return "JARVIS shutting down."
        else:
            return f"I received your command — {text}"


if __name__ == "__main__":
    jarvis = JarvisEngine()
    print(jarvis.respond("status"))
