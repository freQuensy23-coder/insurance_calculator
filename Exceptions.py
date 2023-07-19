class RateDoNotEstablished(Exception):
    # Send message that u should establish rate for today
    def __init__(self, message: str = "Rate do not established for today. Use /set_rate API endpoint"):
        self.message = message
        super().__init__(self.message)
