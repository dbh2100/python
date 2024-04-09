from dataclasses import dataclass
import datetime
import hashlib
import base64
import logging

@dataclass
class Block:

    data1: str
    data2: str
    data3: str
    block_number: int
    previous_block_hash: bytes

    def __post_init__(self):
        self.created_dt = datetime.datetime.now()
        self.block_hash = self.get_block_hash(self.previous_block_hash)
        self.next_block = None
        self.logger = logging.getLogger(repr(self))

    def __repr__(self):
        return f'Block{self.block_number}'

    def get_block_hash(self, previous_block_hash):
        txn_hash = self.data1 + self.data2 + self.data3
        block_header = bytes(self.block_number)\
            + bytes(str(self.created_dt), encoding='utf8')\
            + previous_block_hash
        combined = bytes(txn_hash, encoding='utf8') + block_header
        return base64.b64encode(hashlib.sha256(combined).digest())

    def is_valid_chain(self, previous_block_hash):
        block_hash = self.get_block_hash(previous_block_hash)
        if block_hash != self.block_hash:
            self.logger.info('FAILED VERIFICATION')
            return False
        self.logger.info('PASS VERIFICATION')
        if self.next_block is None:
            return True
        return self.next_block.is_valid_chain(self.block_hash)

class BlockChain:

    def __init__(self):
        self._head = None
        self._last_block = None
        self._count = 0

    def add_block(self, data1, data2, data3):
        self._count += 1
        previous_block_hash = self._last_block.block_hash if self._last_block else b''
        block = Block(data1, data2, data3, self._count, previous_block_hash)
        if self._head is None:
            self._head = block
        if self._last_block is not None:
            self._last_block.next_block = block
        self._last_block = block

    def is_valid_chain(self):
        if self._head is None:
            raise ValueError('Genesis block not set')
        return self._head.is_valid_chain(b'')
