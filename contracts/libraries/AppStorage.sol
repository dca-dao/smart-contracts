// SPDX-License-Identifier: MIT
pragma solidity 0.7.6;
pragma experimental ABIEncoderV2;

struct DcaSettings {
    uint256 amount;
    uint256 period;
    uint256 lastDcaTimestamp;
}

struct AppStorage {
    address daiAddress;
    address wEthAddress;
    address uniswapRouterAddress;
    uint24 uniSwapPoolFees;
    address[] accounts;
    mapping(address => uint256) addressToDaiAmountFunded;
    mapping(address => uint256) addressToWEthAmount;
    mapping(address => DcaSettings) addressToDcaSettings;
}
