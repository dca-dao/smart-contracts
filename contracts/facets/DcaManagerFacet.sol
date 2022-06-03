// SPDX-License-Identifier: MIT
pragma solidity ^0.7.0;
pragma abicoder v2;

import "../interfaces/IERC20.sol";
import "../libraries/AppStorage.sol";
import "../libraries/LibDiamond.sol";
import {DcaSettings} from "../libraries/AppStorage.sol";

contract DcaManagerFacet {
    AppStorage internal s;

    function setDaiAddress(address daiAddress) public {
        LibDiamond.enforceIsContractOwner();
        s.daiAddress = daiAddress;
    }

    function getDaiAddress() public view returns (address) {
        return s.daiAddress;
    }

    function setWEthAddress(address wEthAddress) public {
        LibDiamond.enforceIsContractOwner();
        s.wEthAddress = wEthAddress;
    }

    function getWEthAddress() public view returns (address) {
        return s.wEthAddress;
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

    function getDaiUserBalance(address _account) public view returns (uint256) {
        return s.addressToDaiAmountFunded[_account];
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

    function getUserDcaSettings(address _account)
        public
        view
        returns (DcaSettings memory)
    {
        return s.addressToDcaSettings[_account];
    }
}
