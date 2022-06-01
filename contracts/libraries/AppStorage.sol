// SPDX-License-Identifier: MIT
pragma solidity 0.7.6;
pragma experimental ABIEncoderV2;

struct DcaSettings {
    uint256 amount;
    uint256 period;
}

struct GlobalSettings {
    address dcaManagerAddress;
    address dcaKeeperAddress;
    address daiAddress;
    address wEthAddress;
}

struct AppStorage {
    address dcaManagerAddress;
    address dcaKeeperAddress;
    address daiAddress;
    address wEthAddress;
    address uniSwapRouterAddress;
    mapping(address => uint256) addressToDaiAmountFunded;
    mapping(address => DcaSettings) addressToDcaSettings;
    GlobalSettings globalSettings;
}
