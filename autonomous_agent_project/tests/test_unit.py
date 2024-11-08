import unittest
import asyncio
import os
from unittest.mock import patch, MagicMock
from main import check_token_balance
from web3 import Web3

class TestCheckTokenBalance(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        # Connect to Tenderly RPC endpoint
        cls.w3 = Web3(Web3.HTTPProvider(os.getenv("TENDERLY_RPC_URL")))

    @patch('main.web3') 
    def checking_token_balance(self, MockWeb3):

        async def async_test():
            # Test the checking_token_balance function with a mock address
            address = "0x3225ed03f7921DADB3bF3EA84945e1034609F390"
            balance = await check_token_balance(address)
            # Assert that balance is correctly fetched
            self.assertEqual(balance, 2000000000000000000)  # 1 token in wei

        # Run the async test
        asyncio.run(async_test())

    def test_connection(self):
        # Test if Web3 is connected to Tenderly
        self.assertTrue(self.w3.is_connected(), "Failed to connect to Tenderly")

if __name__ == '__main__':
    unittest.main()
