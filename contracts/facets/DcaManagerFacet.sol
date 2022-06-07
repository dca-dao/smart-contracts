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

    function fundAccount(uint256 amount) public {
        require(
            IERC20(s.daiAddress).balanceOf(msg.sender) > amount,
            "Insuffisant balance"
        );
        IERC20(s.daiAddress).transferFrom(msg.sender, address(this), amount);
        s.addressToDaiAmountFunded[msg.sender] += amount;
        s.accounts.push(msg.sender);
    }

    // TODO : add a check that the amount is not greater than the amount of DAI
    function withdrawDai(uint256 amount) public {
        require(
            s.addressToDaiAmountFunded[msg.sender] > 0,
            "Account no funded"
        );
        IERC20(s.daiAddress).transfer(msg.sender, amount);
        s.addressToDaiAmountFunded[msg.sender] -= amount;
    }

    // TODO : add a check that the amount is not greater than the amount of WETH
    function withdrawWEth(uint256 amount) public {
        require(s.addressToWEthAmount[msg.sender] > 0, "Account no funded");
        IERC20(s.wEthAddress).transfer(msg.sender, amount);
        s.addressToWEthAmount[msg.sender] -= amount;
    }

    function getDaiUserBalance(address _account) public view returns (uint256) {
        return s.addressToDaiAmountFunded[_account];
    }

    function getWEthBalance(address _account) public view returns (uint256) {
        return s.addressToWEthAmount[_account];
    }

    /*
    DAILY = 86400,
    BI_WEEKLY 302400,
    WEEKLY = 604800,
    MONTHLY = 2592000
    */
    function setDcaSettings(uint256 amount, uint256 period) public {
        require(
            s.addressToDaiAmountFunded[msg.sender] > 0,
            "Account not funded"
        );
        require(
            period == 86400 ||
                period == 302400 ||
                period == 604800 ||
                period == 2592000,
            "DcaManager: Invalid interval"
        );
        DcaSettings memory dcaSettings = DcaSettings(amount, period, 0);
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
