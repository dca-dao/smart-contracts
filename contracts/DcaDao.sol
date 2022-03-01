// SPDX-License-Identifier: MIT

pragma solidity ^0.6.6;

contract DcaDao {
    address payable[] public members;
    mapping(address => uint256) public addressToAmountFunded;

    constructor() public {}

    function fund() public payable {
        addressToAmountFunded[msg.sender] += msg.value;
        members.push(msg.sender);
    }

    function withdraw() public {
        require(addressToAmountFunded[msg.sender] != 0);
        msg.sender.transfer(addressToAmountFunded[msg.sender]);
        addressToAmountFunded[msg.sender] = 0;
    }
}
