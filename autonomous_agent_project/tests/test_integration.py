
from agent import Agent
import unittest
import asyncio
from unittest.mock import patch, MagicMock
from main import agent1, agent2, run_agents
from web3 import Web3



class TestAgentIntegration(unittest.TestCase):

    @patch('web3.Web3')  # Mock the contract to prevent actual blockchain calls
    # @patch('web3.Web3.eth.get_transaction_count')  # Mock the transaction count method
    # @patch('web3.Web3.eth.send_raw_transaction')  # Mock sending raw transactions
    # @patch('web3.Web3.eth.wait_for_transaction_receipt')  # Mock transaction receipt
    def test_agents_interaction(self, mock_web3):
        # Mock blockchain interactions
        # mock_get_tx_count.return_value = 1  # Pretend the nonce is 1
        # mock_send_tx.return_value = "0xMockTxHash"  # Mock a transaction hash
        # mock_wait_receipt.return_value = {'status': 1}  # Simulate successful transaction

        # # Mock the contract's balanceOf method to return a mock balance
        # mock_contract.return_value.functions.balanceOf.return_value.call.return_value = Web3.toWei(100, 'ether')
        
        mock_eth = MagicMock()
        mock_web3.eth = mock_eth
        
        # Mock the `contract` method to return a mock contract object
        mock_contract = MagicMock()
        mock_eth.contract.return_value = mock_contract
        mock_contract.functions.balanceOf.return_value = 1000  # Mock the balanceOf call
        mock_contract.functions.transfer.return_value = MagicMock()  # Mock transfer call


        # Register behaviors and handlers for agent1 and agent2
        agent1.register_behavior(self.mock_behavior)
        agent1.register_handler("random_message", self.mock_handler)
        agent2.register_behavior(self.mock_behavior)
        agent2.register_handler("random_message", self.mock_handler)
        agent2.register_behavior(self.mock_transfer_behavior)
        

        loop = asyncio.get_event_loop()
        loop.run_until_complete(run_agents())
        # Run the agents' behaviors and message consumption asynchronously
        # asyncio.run(run_agents())  # This will invoke agent1 and agent2 interactions
        
        # Test if messages were passed between agents
        self.assertTrue(agent1.outbox.qsize() > 0, "Agent1 should have messages in the outbox")
        self.assertTrue(agent2.inbox.qsize() > 0, "Agent2 should have messages in the inbox")

        # Check the balance mock was called
        mock_contract.return_value.functions.balanceOf.assert_called_with(agent1.address)
        
        # Check the transfer mock was triggered if 'crypto' was in the message content
        mock_send_tx.assert_called_once()
        mock_wait_receipt.assert_called_once()

    async def mock_behavior(self):
        # Simulate async behavior that generates a random message
        message = {"type": "random_message", "content": "hello world"}
        return message

    async def mock_handler(self, message):
        # Simulate handling the message
        print(f"Handled message: {message['content']}")
    
    async def mock_transfer_behavior(self, message):
        # Simulate transfer behavior if 'crypto' is in the message
        if 'crypto' in message["content"]:
            print("Initiating token transfer due to crypto message.")
            return True

if __name__ == '__main__':
    unittest.main()
