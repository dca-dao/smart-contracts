// SPDX-License-Identifier: MIT
pragma solidity 0.7.6;
pragma experimental ABIEncoderV2;

struct DcaSettings {
    uint256 amount;
    uint256 period;
}

struct AppStorage {
    address daiAddress;
    address wEthAddress;
    address uniSwapRouterAddress;
    mapping(address => uint256) addressToDaiAmountFunded;
    mapping(address => DcaSettings) addressToDcaSettings;
    uint256 lastDcaTimeStamp;
}
