#!/bin/sh

if [ "$#" -ne 2 ]; then
  echo "Deploy SmartERC20 contract"
  echo "Usage: $0 <private-key> <contract-name>"
  exit 1
fi

cd contracts; forge create \
  --rpc-url http://localhost:8545 \
  --private-key $2 \
  src/$3.sol:$3