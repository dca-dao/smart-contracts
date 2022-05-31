// SPDX-License-Identifier: MIT

pragma solidity ^0.6.6;

contract Staking {
    ILendingPoolAddressesProvider _addressesProvider;

    ILendingPool lendingPool = ILendingPool(provider.getLendingPool());

    constructor(ILendingPoolAddressesProvider addressesProvider) public {
        _addressesProvider = addressesProvider;
    }

    function stakeToken(address tokenAddress, uint256 amount) public {
        require(
            IERC20(tokenAddress).balanceOf(msg.sender) >= amount,
            "Insufficient balance"
        );
        // Transfer funds from the caller to the depositing contract
        IERC20(tokenAddress).transferFrom(msg.sender, address(this), amount);

        // Approve LendingPool to spend your contracts funds
        if (
            IERC20(tokenAddress).allowance(
                address(this),
                address(lendingPool)
            ) == 0
        ) {
            IERC20(tokenAddress).approve(address(lendingPool), uint256(-1));
        }

        // Deposit on onBehalf of msg.sender
        lendingPool.deposit(tokenAddress, amount, msg.sender, 0);
    }
}
