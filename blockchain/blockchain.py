import json
from block import *
from transaction import *
import time


class Blockchain():
    def __init__(self):
        self.blockchain = []
        self.transactions = []
        self.can_add_txn = False
        self.can_create_block = True
        self.transactions_for_block = []
        self.pending_transaction = []

    def create_block(self, txn):
        self.can_add_txn = True
        self.can_create_block = False
        time.sleep(1)
        self.can_add_txn = False
        self.can_create_block = True
        self.transactions_for_block.append(txn)
        prev_block = self.json_get_last_block()
        block = Block(prev_block["block_number"]+1, prev_block["hash"],
                      self.transactions_for_block)

        self.minePendingTransactions("", block)
        self.transactions_for_block = []
        self.json_encode(block)
        self.can_create_block = True

    def minePendingTransactions(self, miner, newBlock):
        newBlock.mineBlock()
        newBlock.is_valid = True
        return True

    def txn(self, sender, reciver, amt):
        txn = Transaction(sender, reciver, amt, len(self.transactions) + 1)
        if self.can_create_block and self.can_add_txn == False and txn.is_valid:
            self.create_block(txn)
            return

    def create_genesis(self):
        block = Block(1, '', [])
        block.nonce
        self.minePendingTransactions("", block)
        self.json_encode(block)

    def json_encode(self, block):
        blocks = {}
        txn = {}

        blocks['block'] = {
            'hash': block.hash,
            'prev_hash': block.prev_hash,
            'nonce': block.nonce,
            'time_stamp': block.time,
            'block_number': block.block_location,
            'is_valid': block.is_valid
        }

        for transactions in block.transactions:

            txn['transaction'] = {
                'sender': transactions.sender,
                'reciver': transactions.reciver,
                'amount': transactions.amt,
                'hash': transactions.hash,
                'time_stamp': transactions.time,
                'is_valid': transactions.is_valid,
                'block_number': block.block_location
            }
            with open('data.json', mode='r+', encoding='utf-8') as data:
                txn_data = json.load(data)
                txn_data["transactions"].append(txn)
                data.seek(0)
                json.dump(txn_data, data, indent=4)
            transactions = 0

        with open('data.json', mode='r+', encoding='utf-8') as data:
            block_data = json.load(data)
            block_data["blocks"].append(blocks)
            data.seek(0)
            json.dump(block_data, data, indent=4)

    def json_get_last_block(self):
        with open('data.json', mode='r', encoding='utf-8') as data:
            blocks = json.load(data)
            return blocks['blocks'][-1]['block']


b = Blockchain()
# b.create_genesis()
b.txn("1Byp3v4DFybN7DdWxwwHvYLj4chArRbm4f",
      "1J8kRAgf3G4DoDAtkfKk2ZPxPwpERCvCBj", 15)
b.txn("1J8kRAgf3G4DoDAtkfKk2ZPxPwpERCvCBj",
      "1Byp3v4DFybN7DdWxwwHvYLj4chArRbm4f", 15)
b.json_get_last_block()
