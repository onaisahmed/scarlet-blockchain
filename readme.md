# Scarlet Blockchain

Scarlet Blockchain is a simple and modular blockchain implementation built using Python and Flask. This project demonstrates the fundamental concepts of blockchain technology, including mining, transactions, and network communication between nodes.

## Project Structure

The project follows a structured layout for better organization:

- **scarlet-blockchain/**
  - **app/** _(Contains the application code)_
    - `__init__.py` _(Initializes the Flask application)_
    - `blockchain.py` _(Contains the Blockchain class with core logic)_
    - `routes.py` _(Defines the HTTP routes for interacting with the blockchain)_
  - **nodes/** _(Contains individual node scripts)_
    - `node1.py` _(Runs node 1 on port 5001)_
    - `node2.py` _(Runs node 2 on port 5002)_
    - `node3.py` _(Runs node 3 on port 5003)_
  - `requirements.txt` _(Lists required Python packages)_
  - `venv/` _(Virtual environment for package management)_
  - `run_nodes.sh` _(Script to start all nodes simultaneously)_
  - `run.py` _(Runs node on port 5000)_

## Features

- **Mining**: Implemented proof-of-work algorithm to mine new blocks.
- **Transactions**: Supports adding transactions between users.
- **Networked Nodes**: Multiple nodes can connect to each other, maintaining a consistent state across the network.
- **Blockchain Validity**: Mechanism to validate the integrity of the blockchain.
- **HTTP API**: Exposes RESTful endpoints to interact with the blockchain.

## Getting Started

### Prerequisites

- Python 3.6 or higher
- `pip` (Python package installer)

### Installation

1. **Clone the repository**:

   ```bash
   git clone https://github.com/onaisahmed/scarlet-blockchain.git
   cd scarlet-blockchain

   ```

2. **Set up a virtual environment**:

   ```bash
   python -m venv venv

   ```

3. **Activate the virtual environment**:

   - **Windows**: `venv\Scripts\activate`
   - **Mac/Linux**: `source venv/bin/activate`

4. **Install required packages**:

   ```bash
   pip install -r requirements.txt

   ```

### Running the Nodes

You can start all nodes simultaneously by running the run_nodes.sh script:

```bash
chmod +x run_nodes.sh    # Make the script executable (Linux/Mac)
./run_nodes.sh           # Start all nodes

```

### Testing the Blockchain

You can test the blockchain using curl or Postman to interact with the API endpoints:

**Mine a Block**:

```bash
curl http://localhost:5001/mine-block
```

**Get the Blockchain**:

```bash
curl  http://localhost:5001/get-chain
```

**Check Validity**:

```bash
curl   http://localhost:5001/is-valid
```

**Add Transaction**:

```bash
curl -X POST -H "Content-Type: application/json" -d '{"sender": "address1", "receiver": "address2", "amount": 5}' http://localhost:5001/add-transaction
```

**Connect Nodes**:

```bash
curl -X POST -H "Content-Type: application/json" -d '{"nodes": ["http://localhost:5002", "http://localhost:5003"]}' http://localhost:5001/connect-nodes
```

**Replace Chain**:

```bash
curl -X GET http://localhost:5001/replace-chain
```
