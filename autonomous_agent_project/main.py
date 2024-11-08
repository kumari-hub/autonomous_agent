import asyncio
from agent import Agent
import random
from web3 import Web3
import os
import json
import logging
from web3.exceptions import Web3Exception, ContractLogicError

# Set up logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Web3 setup
web3 = Web3(Web3.HTTPProvider(os.getenv("TENDERLY_RPC_URL")))
address = "0xb92F639699F4673b1aE4bfF8Fd961ED5E663d2E1" 
contract_address = "0x6B175474E89094C44Da98b954EedeAC495271d0F"  # Replace with ERC-20 token contract
# Connect to Tenderly RPC URL
contract_abi = [{"inputs":[{"internalType":"uint256","name":"chainId_","type":"uint256"}],"payable":False,"stateMutability":"nonpayable","type":"constructor"},{"anonymous":False,"inputs":[{"indexed":True,"internalType":"address","name":"src","type":"address"},{"indexed":True,"internalType":"address","name":"guy","type":"address"},{"indexed":False,"internalType":"uint256","name":"wad","type":"uint256"}],"name":"Approval","type":"event"},{"anonymous":True,"inputs":[{"indexed":True,"internalType":"bytes4","name":"sig","type":"bytes4"},{"indexed":True,"internalType":"address","name":"usr","type":"address"},{"indexed":True,"internalType":"bytes32","name":"arg1","type":"bytes32"},{"indexed":True,"internalType":"bytes32","name":"arg2","type":"bytes32"},{"indexed":False,"internalType":"bytes","name":"data","type":"bytes"}],"name":"LogNote","type":"event"},{"anonymous":False,"inputs":[{"indexed":True,"internalType":"address","name":"src","type":"address"},{"indexed":True,"internalType":"address","name":"dst","type":"address"},{"indexed":False,"internalType":"uint256","name":"wad","type":"uint256"}],"name":"Transfer","type":"event"},{"constant":True,"inputs":[],"name":"DOMAIN_SEPARATOR","outputs":[{"internalType":"bytes32","name":"","type":"bytes32"}],"payable":False,"stateMutability":"view","type":"function"},{"constant":True,"inputs":[],"name":"PERMIT_TYPEHASH","outputs":[{"internalType":"bytes32","name":"","type":"bytes32"}],"payable":False,"stateMutability":"view","type":"function"},{"constant":True,"inputs":[{"internalType":"address","name":"","type":"address"},{"internalType":"address","name":"","type":"address"}],"name":"allowance","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"payable":False,"stateMutability":"view","type":"function"},{"constant":False,"inputs":[{"internalType":"address","name":"usr","type":"address"},{"internalType":"uint256","name":"wad","type":"uint256"}],"name":"approve","outputs":[{"internalType":"bool","name":"","type":"bool"}],"payable":False,"stateMutability":"nonpayable","type":"function"},{"constant":True,"inputs":[{"internalType":"address","name":"","type":"address"}],"name":"balanceOf","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"payable":False,"stateMutability":"view","type":"function"},{"constant":False,"inputs":[{"internalType":"address","name":"usr","type":"address"},{"internalType":"uint256","name":"wad","type":"uint256"}],"name":"burn","outputs":[],"payable":False,"stateMutability":"nonpayable","type":"function"},{"constant":True,"inputs":[],"name":"decimals","outputs":[{"internalType":"uint8","name":"","type":"uint8"}],"payable":False,"stateMutability":"view","type":"function"},{"constant":False,"inputs":[{"internalType":"address","name":"guy","type":"address"}],"name":"deny","outputs":[],"payable":False,"stateMutability":"nonpayable","type":"function"},{"constant":False,"inputs":[{"internalType":"address","name":"usr","type":"address"},{"internalType":"uint256","name":"wad","type":"uint256"}],"name":"mint","outputs":[],"payable":False,"stateMutability":"nonpayable","type":"function"},{"constant":False,"inputs":[{"internalType":"address","name":"src","type":"address"},{"internalType":"address","name":"dst","type":"address"},{"internalType":"uint256","name":"wad","type":"uint256"}],"name":"move","outputs":[],"payable":False,"stateMutability":"nonpayable","type":"function"},{"constant":True,"inputs":[],"name":"name","outputs":[{"internalType":"string","name":"","type":"string"}],"payable":False,"stateMutability":"view","type":"function"},{"constant":True,"inputs":[{"internalType":"address","name":"","type":"address"}],"name":"nonces","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"payable":False,"stateMutability":"view","type":"function"},{"constant":False,"inputs":[{"internalType":"address","name":"holder","type":"address"},{"internalType":"address","name":"spender","type":"address"},{"internalType":"uint256","name":"nonce","type":"uint256"},{"internalType":"uint256","name":"expiry","type":"uint256"},{"internalType":"bool","name":"allowed","type":"bool"},{"internalType":"uint8","name":"v","type":"uint8"},{"internalType":"bytes32","name":"r","type":"bytes32"},{"internalType":"bytes32","name":"s","type":"bytes32"}],"name":"permit","outputs":[],"payable":False,"stateMutability":"nonpayable","type":"function"},{"constant":False,"inputs":[{"internalType":"address","name":"usr","type":"address"},{"internalType":"uint256","name":"wad","type":"uint256"}],"name":"pull","outputs":[],"payable":False,"stateMutability":"nonpayable","type":"function"},{"constant":False,"inputs":[{"internalType":"address","name":"usr","type":"address"},{"internalType":"uint256","name":"wad","type":"uint256"}],"name":"push","outputs":[],"payable":False,"stateMutability":"nonpayable","type":"function"},{"constant":False,"inputs":[{"internalType":"address","name":"guy","type":"address"}],"name":"rely","outputs":[],"payable":False,"stateMutability":"nonpayable","type":"function"},{"constant":True,"inputs":[],"name":"symbol","outputs":[{"internalType":"string","name":"","type":"string"}],"payable":False,"stateMutability":"view","type":"function"},{"constant":True,"inputs":[],"name":"totalSupply","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"payable":False,"stateMutability":"view","type":"function"},{"constant":False,"inputs":[{"internalType":"address","name":"dst","type":"address"},{"internalType":"uint256","name":"wad","type":"uint256"}],"name":"transfer","outputs":[{"internalType":"bool","name":"","type":"bool"}],"payable":False,"stateMutability":"nonpayable","type":"function"},{"constant":False,"inputs":[{"internalType":"address","name":"src","type":"address"},{"internalType":"address","name":"dst","type":"address"},{"internalType":"uint256","name":"wad","type":"uint256"}],"name":"transferFrom","outputs":[{"internalType":"bool","name":"","type":"bool"}],"payable":False,"stateMutability":"nonpayable","type":"function"},{"constant":True,"inputs":[],"name":"version","outputs":[{"internalType":"string","name":"","type":"string"}],"payable":False,"stateMutability":"view","type":"function"},{"constant":True,"inputs":[{"internalType":"address","name":"","type":"address"}],"name":"wards","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"payable":False,"stateMutability":"view","type":"function"}]  # Contract ABI for ERC-20 token
contract = web3.eth.contract(address=contract_address, abi=contract_abi)

# This code defines Behaviour 
async def random_message_generator():
    try:
        words = ["hello", "sun", "world", "space", "moon", "crypto", "sky", "ocean", "universe", "human"]
        message = {"type": "random_message", "content": f"{random.choice(words)} {random.choice(words)}"}
        logger.debug(f"Generated random message: {message}")
        await asyncio.sleep(2)
        return message
    except Exception as e:
        logger.error(f"Error generating random message: {e}")
        return None


# This code defines Handler
async def print_message(message):
    try:
        logger.info(f"Received message: {message['content']}")

        #Checking if the hello exist in the message
        if "hello" in message["content"]:
            logger.info(f"Received 'hello' message: {message['content']}")
    
    except KeyError as e:
        logger.error(f"Error in print_message: Key error - {e}")
    
    except Exception as e:
        logger.error(f"Unexpected error in print_message: {e}")


#This code checks token balance
async def check_token_balance():
    try:
        logger.debug(f"Checking balance for address: {address}")

        #Fetching balance from ERC-20 contract
        balance = contract.functions.balanceOf(address).call()
        logger.info(f"ERC-20 Token Balance: {balance}")
        await asyncio.sleep(10)  # Run every 10 seconds
        return None

    except Web3Exception as e:
        logger.error(f"Web3Exception occurred: {e}")

    except Exception as e:
        logger.error(f"Error checking token balance: {e}")


# This code is for transaction from Account1 to Account2 if message contains Crytp via Contract Address
async def transfer_token(message):
    try:
        logger.debug("Attempting to transfer token if 'crypto' in message")
        
        if "crypto" in message["content"]:
            address_from = "0xb92F639699F4673b1aE4bfF8Fd961ED5E663d2E1"
            address_to = "0x3225ed03f7921DADB3bF3EA84945e1034609F390"
            private_key = os.getenv("PRIVATE_KEY")
            amount = web3.to_wei(1, 'ether')
            nonce = web3.eth.get_transaction_count(address_from)

             # Build the transaction for the ERC-20 token transfer        
            transaction = contract.functions.transfer(address_to, amount).build_transaction({
                'chainId': 1,  # Ethereum mainnet
                'gas': 2000000,
                'gasPrice': web3.to_wei('20', 'gwei'),
                'nonce': nonce,
            })
            #Signing the transaction
            signed_transaction = web3.eth.account.sign_transaction(transaction, private_key)

            #Getting transaction hash
            tx_hash = web3.eth.send_raw_transaction(signed_transaction.raw_transaction)

            #Getting transaction hash details
            transaction_receipt = web3.eth.wait_for_transaction_receipt(tx_hash)
            
            #Checking Account1 and Account2 token balance
            if transaction_receipt['status'] == 1:
                logger.info("Transaction successful!")
                recipient_balance1 = contract.functions.balanceOf(address_from).call()

                logger.info(f"New balance of sender: {web3.from_wei(recipient_balance1, 'ether')} tokens")
                recipient_balance2 = contract.functions.balanceOf(address_to).call()
                logger.info(f"New balance of recipient: {web3.from_wei(recipient_balance2, 'ether')} tokens")

            else:
                logger.warning("Transaction failed.")

            return tx_hash
        else:
            logger.info("No 'crypto' message found, skipping transfer.")

    except ContractLogicError as e:
        logger.error(f"Contract error during token transfer: {e}")

    except Web3Exception as e:
        logger.error(f"Web3Exception occurred: {e}")

    except Exception as e:
        logger.error(f"Unexpected error during token transfer: {e}")


# 
# This creates an instance of the 'Agent' class named 'Agent 1'
agent1 = Agent("Agent 1")

# Registering the behavior 'generate_random_message' to 'Agent 1'
# This behavior will periodically generate a random message
agent1.register_behavior(random_message_generator)

# Registering a handler for the 'random_message' type
# This handler will process messages of type 'random_message' and call 'print_message'
agent1.register_handler("random_message", print_message)


# Registering another behavior 'check_token_balance' to 'Agent 1'
# This behavior will periodically check the token balance for the agent's address
agent1.register_behavior(check_token_balance)


# Creating Agent2 from AgentClass
# This creates another instance of the 'Agent' class named 'Agent 2'
agent2 = Agent("Agent 2")

# Registering the behavior 'generate_random_message' to 'Agent 2'
# Similar to 'Agent 1', this behavior will generate a random message
agent2.register_behavior(random_message_generator)

# Registering the handler for the 'random_message' type to 'Agent 2'
# This handler will process and print messages of type 'random_message'
agent2.register_handler("random_message", print_message)

# Registering the behavior 'check_token_balance' to 'Agent 2'
# This behavior checks the token balance for 'Agent 2' just like it does for 'Agent 1'
agent2.register_behavior(check_token_balance)

# Registering another handler for 'random_message' to 'Agent 2'
# This handler triggers the 'transfer_token' function if the message contains the word 'crypto'
agent2.register_handler("random_message", transfer_token)


async def run_agents():

    # Create a list of tasks to be run concurrently.
    # These tasks include both message consumption and emission for both agents.

    # loop = asyncio.get_event_loop()
    try:
        tasks = [
            agent1.messages_consume(),
            
            # Agent1 emits messages to Agent2
            agent1.messages_emit(agent2),  # Pass agent2 as the other agent
            
            agent2.messages_consume(),

            # Agent2 emits messages to Agent1
            agent2.messages_emit(agent1),  # Pass agent1 as the other agent
        ]
# Using asyncio.gather to run all tasks concurrently
        await asyncio.gather(*tasks)

# If any exception occurs during the execution of the tasks, log the error
    except Exception as e:
        logger.error(f"Error running agents: {e}")


# If running this as a script, ensure the loop is properly run
if __name__ == "__main__":
    try:
        loop = asyncio.get_event_loop()  # Ensure we get the same event loop
        loop.run_until_complete(run_agents())  # Manually run the event loop
    except Exception as e:
        logger.error(f"Error starting the event loop: {e}")

