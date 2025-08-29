"""Defines a blockchain"""

from   pydantic import BaseModel, Field
from   typing import Optional
import datetime
import hashlib
import base64


def get_block_hash(block_info: dict, previous_hash: Optional[bytes] = None) -> bytes:
    """Calculate the hash of the current block"""
    previous_hash = previous_hash or block_info['previous_block_hash']
    txn_hash = block_info['data1'] + block_info['data2'] + block_info['data3']
    block_header = bytes(block_info['block_number'])
    block_header += bytes(str(block_info['created_dt']), encoding='utf8')
    block_header += previous_hash
    combined = bytes(txn_hash, encoding='utf8') + block_header
    return base64.b64encode(hashlib.sha256(combined).digest())


class Block(BaseModel):
    """Block for Blockchain"""

    data1: str
    data2: str
    data3: str
    block_number: int
    previous_block_hash: bytes
    created_dt: datetime.datetime = datetime.datetime.now()
    block_hash: bytes = Field(default_factory=get_block_hash)
    next_block: 'Block|None' = None

    def __repr__(self):
        return f'Block{self.block_number}'

    def is_valid_block(self, previous_block_hash: bytes) -> bool:
        """Validate block
        If validation fails, the entire blockchain is not valid
        """
        if self.block_hash != get_block_hash(self.model_dump(), previous_block_hash):
            return False
        if self.next_block is None:
            return True
        return self.next_block.is_valid_block(self.block_hash)


class BlockChain:
    """Blockchain class"""

    def __init__(self):
        self._head = None
        self._last_block = None
        self._count = 0

    def add_block(self, data1, data2, data3):
        """Add a block to the blockchain with given data"""

        self._count += 1
        previous_block_hash = self._last_block.block_hash if self._last_block else b''
        block = Block(
            data1=data1, data2=data2, data3=data3, block_number=self._count,
            previous_block_hash=previous_block_hash
        )

        if self._head is None:
            self._head = block
        if self._last_block is not None:
            self._last_block.next_block = block
        self._last_block = block

    def is_valid_chain(self):
        """Check if blockchain is valid"""
        if self._head is None:
            raise ValueError('Genesis block not set')
        return self._head.is_valid_block(b'')
