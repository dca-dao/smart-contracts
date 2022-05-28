// SPDX-License-Identifier: MIT

pragma solidity ^0.6.6;

contract Staking {

  ILendingPool lendingPool = ILendingPool(provider.getLendingPool());

  // Transfer funds from the caller to the depositing contract
  IERC20(asset).transferFrom(msg.sender, address(this), amount);

  // Approve LendingPool to spend your contracts funds
  if (IERC20(asset).allowance(address(this), address(LendingPool)) == 0) {
    erc20.approve(address(LendingPool), uint256(-1));
  }

  // Deposit on onBehalf of msg.sender
  lendingPool.deposit(_asset, _amount, msg.sender, 0);

}