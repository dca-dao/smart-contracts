// SPDX-License-Identifier: MIT
pragma solidity ^0.7.0;
pragma abicoder v2;

import "./interfaces/IERC20.sol";

contract DcaManager {
    struct DcaSettings {
        uint256 amount;
        uint256 period;
    }

    mapping(address => uint256) public addressToDaiAmountFunded;
    mapping(address => DcaSettings) public addressToDcaSettings;

    constructor() public {}

    function fundAccount(uint256 amount, address tokenAddress) public {
        require(
            IERC20(tokenAddress).balanceOf(msg.sender) > amount,
            "Insuffisant balance"
        );
        IERC20(tokenAddress).transferFrom(msg.sender, address(this), amount);
        addressToDaiAmountFunded[msg.sender] += amount;
    }

    function withdraw(uint256 amount, address tokenAddress) public {
        require(addressToDaiAmountFunded[msg.sender] > 0, "Account no funded");
        IERC20(tokenAddress).transfer(msg.sender, amount);
        addressToDaiAmountFunded[msg.sender] = 0;
    }

    /*
    DAILY = 86400,
    BI_WEEKLY 302400,
    WEEKLY = 604800,
    MONTHLY = 2592000
    */
    function setDcaSettings(DcaSettings memory dcaSettings) public {
        require(addressToDaiAmountFunded[msg.sender] > 0, "Account not funded");
        require(
            dcaSettings.period == 86400 ||
                dcaSettings.period == 302400 ||
                dcaSettings.period == 604800 ||
                dcaSettings.period == 2592000,
            "DcaManager: Invalid interval"
        );
        addressToDcaSettings[msg.sender] = dcaSettings;
    }
}
