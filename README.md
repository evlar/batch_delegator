
# Batch Delegator for Bittensor Network

## Introduction
This repository contains a Python script, `batch_delegator.py`, designed to automate batch delegation tasks within the Bittensor network. It utilizes a list of taostats certified validator hotkeys provided in `validator_hotkeys.csv` to efficiently manage delegations.

## Requirements
- Python 3.x
- Bittensor library
- Additional Python libraries as required (please refer to `requirements.txt`)

## Installation
To set up the project, follow these steps:
1. Clone this repository to your local machine.
2. pip install bittensor

## Usage
Run the script from the command line:
```
python3 batch_delegator.py
```
Ensure that the `validator_hotkeys.csv` file is in the same directory as the script. The script reads information from this file for processing.

## File Descriptions
- **batch_delegator.py**: The main Python script that automates batch delegation.
- **validator_hotkeys.csv**: A CSV file containing names and addresses of validators. This data is essential for the script to perform batch operations.

