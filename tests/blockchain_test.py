import unittest
import datetime
from blockchain import Block, BlockChain, get_block_hash


class TestBlock(unittest.TestCase):

    def setUp(self):
        self.data1 = "foo"
        self.data2 = "bar"
        self.data3 = "baz"
        self.block_number = 1
        self.previous_block_hash = b''
        self.created_dt = datetime.datetime(2024, 1, 1, 12, 0, 0)
        self.block_info = {
            "data1": self.data1,
            "data2": self.data2,
            "data3": self.data3,
            "block_number": self.block_number,
            "previous_block_hash": self.previous_block_hash,
            "created_dt": self.created_dt
        }
        self.block_hash = get_block_hash(self.block_info)
        self.block = Block(
            data1=self.data1,
            data2=self.data2,
            data3=self.data3,
            block_number=self.block_number,
            previous_block_hash=self.previous_block_hash,
            created_dt=self.created_dt
        )

    def test_block_attributes(self):
        self.assertEqual(self.block.data1, self.data1)
        self.assertEqual(self.block.data2, self.data2)
        self.assertEqual(self.block.data3, self.data3)
        self.assertEqual(self.block.block_number, self.block_number)
        self.assertEqual(self.block.previous_block_hash, self.previous_block_hash)
        self.assertEqual(self.block.created_dt, self.created_dt)
        self.assertEqual(self.block.block_hash, self.block_hash)

    def test_repr(self):
        self.assertEqual(repr(self.block), f'Block{self.block_number}')

    def test_is_valid_block_true(self):
        self.assertTrue(self.block.is_valid_block(self.previous_block_hash))

    def test_is_valid_block_false(self):
        wrong_hash = b'not_a_real_hash'
        self.assertFalse(self.block.is_valid_block(wrong_hash))


class TestBlockChain(unittest.TestCase):

    def test_valid_chain(self):
        chain = BlockChain()
        chain.add_block("a", "b", "c")
        chain.add_block("d", "e", "f")
        chain.add_block("g", "h", "i")
        self.assertTrue(chain.is_valid_chain())

    def test_invalid_chain(self):
        chain = BlockChain()
        chain.add_block("a", "b", "c")
        chain.add_block("d", "e", "f")
        # Tamper with second block's data
        block = chain._block_map[list(chain._block_map.keys())[1]]
        block.data1 = "tampered"
        self.assertFalse(chain.is_valid_chain())

    def test_genesis_block_not_found(self):
        chain = BlockChain()
        with self.assertRaises(ValueError):
            chain.is_valid_chain()


if __name__ == '__main__':
    unittest.main()
