import hashlib
import json

class Transaction:
    def __init__(self, sender, recipient, amount):
        self.sender = sender
        self.recipient = recipient
        self.amount = amount

    def to_dict(self):
        return {
            'sender': self.sender,
            'recipient': self.recipient,
            'amount': self.amount
        }

    def is_valid(self):
        # Para simplificar, vamos assumir que a transação é válida se todos os campos existirem
        return all([self.sender, self.recipient, self.amount >= 0])

    @staticmethod
    def from_dict(data):
        return Transaction(data['sender'], data['recipient'], data['amount'])
