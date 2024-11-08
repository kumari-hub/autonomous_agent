# Project Name

## Overview

This project implements an autonomous agent with asynchronous messaging, reactive and proactive behaviors, and Web3 interactions for managing Ethereum-based tokens. The project allows for the automation of tasks such as message generation, token balance checking, and conditional token transfers.

## Environment Setup

Before running the project, you'll need to set up your environment and dependencies.

### 1. Check if Python is installed
```
python3 --version
```

### 2. Setting up a Virtual Environment

```
python3 -m venv autonomous_agent_env
source autonomous_agent_env/bin/activate
```

### 3. Install dependencies

```
pip install -r requirements.txt
```


### 4. Setting Up Environment Variables

You need to configure environment variables for this project. 

```
export PRIVATE_KEY="your_private_key_here"
export TENDERLY_RPC_URL="your_tenderly_rpc_url_here"
```

### 5. Running the Project
```
python3 main.py
```

### 6. Error Handling and Troubleshooting
```
python main.py > app.log 2>&1
```

