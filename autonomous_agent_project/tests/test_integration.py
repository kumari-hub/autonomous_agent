import asyncio
import unittest

class Agent:
    def __init__(self, name):
        self.name = name
        self.inbox = asyncio.Queue()
        self.outbox = asyncio.Queue()
        self.handlers = {}
        self.behaviors = []

    def register_handler(self, message_type, handler):
        self.handlers[message_type] = handler

    def register_behavior(self, behavior):
        self.behaviors.append(behavior)

    async def consume_messages(self):
        # Consume only one message for testing to avoid infinite loop during test
        message = await self.inbox.get()
        message_type = message.get("type")
        if message_type in self.handlers:
            handler = self.handlers[message_type]
            await handler(message)
            print(f"{self.name} received message: {message}")

    async def emit_messages(self, other_agent):
        # Emit only one message for testing purposes
        if self.behaviors:
            message = await self.behaviors[0]()
            if message:
                await self.outbox.put(message)
                await other_agent.inbox.put(message)
                print(f"{self.name} sent message to {other_agent.name}: {message}")

class TestAgentCommunication(unittest.IsolatedAsyncioTestCase):
    async def asyncSetUp(self):
        # Set up two agents
        self.agent1 = Agent("Agent 1")
        self.agent2 = Agent("Agent 2")

        # Register handlers for each agent
        self.agent1.register_handler("response", self.agent1_message_handler)
        self.agent2.register_handler("greeting", self.agent2_message_handler)
        
        # Register behaviors for each agent
        self.agent1.register_behavior(self.agent1_behavior)
        self.agent2.register_behavior(self.agent2_behavior)
        
        # Track received messages for assertions
        self.agent1.received_messages = []
        self.agent2.received_messages = []

    async def agent1_message_handler(self, message):
        self.agent1.received_messages.append(message)
        print(f"Agent 1 handler processed message: {message}")

    async def agent2_message_handler(self, message):
        self.agent2.received_messages.append(message)
        print(f"Agent 2 handler processed message: {message}")

    async def agent1_behavior(self):
        return {"type": "greeting", "content": "Hello from Agent 1"}

    async def agent2_behavior(self):
        return {"type": "response", "content": "Hello back from Agent 2"}

    async def test_agents_communication(self):
        # Start message tasks
        agent1_consume_task = asyncio.create_task(self.agent1.consume_messages())
        agent2_consume_task = asyncio.create_task(self.agent2.consume_messages())
        
        # Send messages between agents
        await self.agent1.emit_messages(self.agent2)
        await self.agent2.emit_messages(self.agent1)
        
        # Wait for messages to be handled
        await asyncio.wait([agent1_consume_task, agent2_consume_task], timeout=2)

        # Assertions to verify communication
        self.assertTrue(any(msg["type"] == "greeting" for msg in self.agent2.received_messages),
                        "Agent 2 did not receive a greeting message from Agent 1.")
        self.assertTrue(any(msg["type"] == "response" for msg in self.agent1.received_messages),
                        "Agent 1 did not receive a response message from Agent 2.")

if __name__ == "__main__":
    unittest.main()
