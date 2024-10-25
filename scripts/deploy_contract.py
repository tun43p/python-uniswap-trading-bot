# Deploy a contract to the blockchain based on the contract name provided as an argument
# to the script. The script uses the Forge CLI to deploy the contract to the specified
# RPC_URL using the provided PRIVATE_KEY located in your env variables. The deployment
# process is logged to a file in the logs directory.

import datetime
import dotenv
import logging
import os
import subprocess
import sys


if len(sys.argv) < 2:
    logging.error("No contract name provided.")
    raise ValueError("No contract name provided.")

contract_name = sys.argv[1]

dotenv.load_dotenv()

if not os.path.exists("logs/contracts"):
    os.makedirs("logs/contracts")

logging.basicConfig(
    filename="logs/contracts/{}_{}_deploy.log".format(
        contract_name, int(datetime.datetime.now().timestamp())
    ),
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
)

RPC_URL = os.environ.get("RPC_URL")
DEPLOYER_PRIVATE_KEY = os.environ.get("DEPLOYER_PRIVATE_KEY")

if not RPC_URL:
    logging.error("RPC_URL environment variable not set.")
    raise ValueError("RPC_URL environment variable not set")

if not DEPLOYER_PRIVATE_KEY:
    logging.error("DEPLOYER_PRIVATE_KEY environment variable not set.")
    raise ValueError("DEPLOYER_PRIVATE_KEY environment variable not set")

logging.info(f"Deploying contract {contract_name} to {RPC_URL}")
print(f"Deploying contract {contract_name} to {RPC_URL}")

command = (
    f"cd contracts && forge create --rpc-url {RPC_URL} --private-key {DEPLOYER_PRIVATE_KEY} "
    f"src/{contract_name}.sol:{contract_name}"
)

process = subprocess.Popen(
    command,
    shell=True,
    stdout=subprocess.PIPE,
    stderr=subprocess.PIPE,
    text=True,
)

with process.stdout as stdout, process.stderr as stderr:
    for line in stdout:
        logging.info(line.strip())
        print(line.strip())
    for line in stderr:
        logging.error(line.strip())
        raise ValueError(line.strip())

return_code = process.wait()
if return_code != 0:
    logging.error(f"Deployment failed with exit code {return_code}")
    raise ValueError(f"Deployment failed with exit code {return_code}")
else:
    logging.info("Deployment succeeded.")
    print("Deployment succeeded.")
