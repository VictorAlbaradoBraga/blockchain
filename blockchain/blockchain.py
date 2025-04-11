import json
import time
from pathlib import Path
from threading import Lock
from .block import Block
from .transaction import Transaction

class Blockchain:
    def __init__(self, difficulty=2):
        self.difficulty = difficulty
        self.blocks = []
        self.pending_transactions = []
        self.lock = Lock()

        base_dir = Path(__file__).resolve().parent.parent
        data_dir = base_dir / 'data'
        data_dir.mkdir(exist_ok=True)
        self.file_path = data_dir / 'blockchain.json'

        self.load_or_create()

    def create_genesis_block(self):
        genesis_block = Block(0, time.time(), None, [])
        genesis_block.proof_of_work(self.difficulty)
        self.blocks.append(genesis_block)
        self.save()

    def latest_block(self):
        return self.blocks[-1]

    def add_transaction(self, transaction: Transaction):
        if transaction.is_valid():
            self.pending_transactions.append(transaction)
            return True
        return False

    def mine_block(self):
        with self.lock:
            if not self.pending_transactions:
                return False
            new_block = Block(
                index=len(self.blocks),
                timestamp=time.time(),
                previous_hash=self.latest_block().hash,
                transactions=self.pending_transactions[:]
            )
            new_block.proof_of_work(self.difficulty)
            self.blocks.append(new_block)
            self.pending_transactions = []
            self.save()
            return True

    def is_chain_valid(self):
        for i in range(1, len(self.blocks)):
            curr = self.blocks[i]
            prev = self.blocks[i - 1]
            if curr.hash != curr.calculate_hash():
                return False
            if curr.previous_hash != prev.hash:
                return False
        return True

    def save(self):
        with self.file_path.open('w') as f:
            json.dump([block.to_dict() for block in self.blocks], f, indent=2)

    def load_or_create(self):
        if self.file_path.exists():
            with self.file_path.open() as f:
                data = json.load(f)
                self.blocks = [Block.from_dict(b) for b in data]
        else:
            self.create_genesis_block()

    def tamper_block(self, index, fake_data):
        if 0 <= index < len(self.blocks):
            self.blocks[index].transactions = [Transaction(**fake_data)]
            self.blocks[index].hash = self.blocks[index].calculate_hash()
            self.save()
