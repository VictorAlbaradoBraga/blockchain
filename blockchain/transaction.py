class Transaction:
    def __init__(self, title, description, file_name, file_type, creator_email, file_hash, timestamp):
        self.title = title
        self.description = description
        self.file_name = file_name
        self.file_type = file_type
        self.creator_email = creator_email
        self.file_hash = file_hash
        self.timestamp = timestamp

    def is_valid(self):
        # Simples checagem se todos os campos principais estão preenchidos
        return all([
            self.title,
            self.file_name,
            self.file_type,
            self.creator_email,
            self.file_hash,
            self.timestamp
        ])

    def to_dict(self):
        return {
            "title": self.title,
            "description": self.description,
            "file_name": self.file_name,
            "file_type": self.file_type,
            "creator_email": self.creator_email,
            "file_hash": self.file_hash,
            "timestamp": self.timestamp
        }

    @classmethod
    def from_dict(cls, data):
        return cls(
            title=data["title"],
            description=data["description"],
            file_name=data["file_name"],
            file_type=data["file_type"],
            creator_email=data["creator_email"],
            file_hash=data["file_hash"],
            timestamp=data["timestamp"]
        )
