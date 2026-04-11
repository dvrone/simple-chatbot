class Memory:
    def __init__(self, max_history: int = 10):
        self.history = []
        self.max_history = max_history
        self.user_data = {}

    def add(self, role: str, text: str):
        self.history.append({"role": role, "text": text})
        if len(self.history) > self.max_history:
            self.history.pop(0)

    def remember(self, key: str, value: str):
        self.user_data[key] = value

    def recall(self, key: str) -> str | None:
        return self.user_data.get(key)

    def get_context(self) -> str:
        if not self.history:
            return ""
        context = []
        for msg in self.history:
            prefix = "Foydalanuvchi" if msg["role"] == "user" else "Bot"
            context.append(f"{prefix}: {msg['text']}")
        return "\n".join(context)

    def clear(self):
        self.history = []
        self.user_data = {}
