class Transaction:
    def __init__(self, sender, recipient, data):
        self.sender = sender
        self.recipient = recipient
        self.data = data

    def is_valid(self):
        # Checa se todos os campos estão presentes
        return bool(self.sender and self.recipient and self.data)

    def to_dict(self):
        return {
            "sender": self.sender,
            "recipient": self.recipient,
            "data": self.data
        }

    @classmethod
    def from_dict(cls, data):
        return cls(
            sender=data["sender"],
            recipient=data["recipient"],
            data=data["data"]
        )
