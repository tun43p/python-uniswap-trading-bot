// SPDX-License-Identifier: MIT
pragma solidity ^0.8.26;

import "openzeppelin-contracts/contracts/token/ERC20/ERC20.sol";

contract SmartERC20 is ERC20 {
    constructor() ERC20("SmartERC20", "SERC20") {
        _mint(msg.sender, 1000000 * 10 ** decimals());
    }
}
