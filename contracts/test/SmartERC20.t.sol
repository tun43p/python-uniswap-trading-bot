// SPDX-License-Identifier: MIT
pragma solidity ^0.8.26;

import {Test, console} from "forge-std/Test.sol";
import {SmartERC20} from "../src/SmartERC20.sol";

contract SmartERC20Test is Test {
    SmartERC20 public token;

    function setUp() public {
        token = new SmartERC20();
    }

    function testTokenName() public view {
        assertEq(token.name(), "SmartERC20");
    }

    function testTokenSymbol() public view {
        assertEq(token.symbol(), "SERC20");
    }

    function testTokenDecimals() public view {
        assertEq(token.decimals(), 18);
    }

    function testTokenTotalSupply() public view {
        assertEq(token.totalSupply(), 1000000 * 10 ** 18);
    }
}
