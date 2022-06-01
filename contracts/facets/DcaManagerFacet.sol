// SPDX-License-Identifier: MIT
pragma solidity ^0.7.0;
pragma abicoder v2;

import "../interfaces/IERC20.sol";
import "../libraries/AppStorage.sol";
import {DcaSettings} from "../libraries/AppStorage.sol";

contract DcaManagerFacet {
    AppStorage internal s;
    event OwnershipTransferred(
        address indexed previousOwner,
        address indexed newOwner
    );

    address public owner;

    constructor() {
        owner = msg.sender;
        s.dcaManagerAddress = address(this);
    }

    modifier onlyOwner() {
        require(msg.sender == owner);
        _;
    }

    function setDaiAddress(address daiAddress) public onlyOwner {
        s.daiAddress = daiAddress;
    }

    function setWEthAddress(address wEthAddress) public onlyOwner {
        s.wEthAddress = wEthAddress;
    }

    function transferOwnership(address newOwner) public onlyOwner {
        require(newOwner != address(0));
        emit OwnershipTransferred(owner, newOwner);
        owner = newOwner;
    }

    function fundAccount(uint256 amount, address tokenAddress) public {
        require(
            IERC20(tokenAddress).balanceOf(msg.sender) > amount,
            "Insuffisant balance"
        );
        IERC20(tokenAddress).transferFrom(msg.sender, address(this), amount);
        s.addressToDaiAmountFunded[msg.sender] += amount;
    }

    function withdraw(uint256 amount, address tokenAddress) public {
        require(
            s.addressToDaiAmountFunded[msg.sender] > 0,
            "Account no funded"
        );
        IERC20(tokenAddress).transfer(msg.sender, amount);
        s.addressToDaiAmountFunded[msg.sender] = 0;
    }

    /*
    DAILY = 86400,
    BI_WEEKLY 302400,
    WEEKLY = 604800,
    MONTHLY = 2592000
    */
    function setDcaSettings(DcaSettings memory dcaSettings) public {
        require(
            s.addressToDaiAmountFunded[msg.sender] > 0,
            "Account not funded"
        );
        require(
            dcaSettings.period == 86400 ||
                dcaSettings.period == 302400 ||
                dcaSettings.period == 604800 ||
                dcaSettings.period == 2592000,
            "DcaManager: Invalid interval"
        );
        s.addressToDcaSettings[msg.sender] = dcaSettings;
    }

    function approveKeeper() public onlyOwner {
        IERC20(s.daiAddress).approve(s.dcaKeeperAddress, uint256(-1));
    }
}
