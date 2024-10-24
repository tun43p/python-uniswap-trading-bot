// SPDX-License-Identifier: MIT
pragma solidity ^0.8.26;

import {Script, console} from "forge-std/Script.sol";
import {SmartERC20} from "../src/SmartERC20.sol";

contract SmartERC20Script is Script {
    SmartERC20 public token;

    function setUp() public {}

    function run() public {
        vm.startBroadcast();

        token = new SmartERC20();

        vm.stopBroadcast();
    }
}
