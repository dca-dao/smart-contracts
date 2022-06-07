// SPDX-License-Identifier: MIT
pragma solidity ^0.7.0;
pragma abicoder v2;

// KeeperCompatible.sol imports the functions from both ./KeeperBase.sol and
// ./interfaces/KeeperCompatibleInterface.sol
import "@chainlink/contracts/src/v0.7/KeeperCompatible.sol";
import "@uniswap/v3-periphery/contracts/interfaces/ISwapRouter.sol";
import "../interfaces/IERC20.sol";
import "../libraries/AppStorage.sol";
import "../libraries/LibDiamond.sol";
import "../libraries/TransferHelper.sol";

contract DcaKeeperFacet is KeeperCompatibleInterface {
    AppStorage internal s;

    function getUniswapPoolFees() public view returns (uint24) {
        return s.uniSwapPoolFees;
    }

    function setUniswapPoolFees(uint24 _uniSwapPoolFees) public {
        LibDiamond.enforceIsContractOwner();
        s.uniSwapPoolFees = _uniSwapPoolFees;
    }

    function getUniswapRouterAddress() public view returns (address) {
        return s.uniswapRouterAddress;
    }

    function setUniswapRouterAddress(address _uniswapRouterAddress) public {
        LibDiamond.enforceIsContractOwner();
        s.uniswapRouterAddress = _uniswapRouterAddress;
    }

    function getTotalToSwap() public view returns (uint256) {
        return calcAmountToSwap();
    }

    function calcAmountToSwap() internal view returns (uint256) {
        uint256 total = 0;
        for (uint256 i = 0; i < s.accounts.length; i++) {
            if (
                block.timestamp -
                    s.addressToDcaSettings[s.accounts[i]].lastDcaTimestamp >
                s.addressToDcaSettings[s.accounts[i]].period
            ) {
                total += s.addressToDcaSettings[s.accounts[i]].amount;
            }
        }
        return total;
    }

    function checkUpkeep(
        bytes calldata /* checkData */
    ) external view override returns (bool upkeepNeeded, bytes memory) {
        upkeepNeeded = calcAmountToSwap() > 0;
    }

    function performUpkeep(bytes calldata) external override {
        // Check if we need to perform dca for any of the accounts
        uint256 totalToSwap = calcAmountToSwap();
        if (totalToSwap > 0) {
            uint256 amountOut = swapExactInputSingle(
                totalToSwap,
                s.daiAddress,
                s.wEthAddress
            );
            // TODO : Should refactor this to remove the need for the loop since calcAmountToSwap() already loop through all the accounts dcas
            for (uint256 i = 0; i < s.accounts.length; i++) {
                if (
                    block.timestamp -
                        s.addressToDcaSettings[s.accounts[i]].lastDcaTimestamp >
                    s.addressToDcaSettings[s.accounts[i]].period
                ) {
                    s
                        .addressToDcaSettings[s.accounts[i]]
                        .lastDcaTimestamp = block.timestamp;
                    s.addressToDaiAmountFunded[s.accounts[i]] -= s
                        .addressToDcaSettings[s.accounts[i]]
                        .amount;
                    s.addressToWEthAmount[s.accounts[i]] +=
                        (amountOut *
                            s.addressToDcaSettings[s.accounts[i]].amount) /
                        totalToSwap;
                }
            }
        }
    }

    /// @notice swapExactInputSingle swaps a fixed amount of DAI for a maximum possible amount of WETH9
    /// using the DAI/WETH9 0.3% pool by calling `exactInputSingle` in the swap router.
    /// @dev The calling address must approve this contract to spend at least `amountIn` worth of its DAI for this function to succeed.
    /// @param amountIn The exact amount of DAI that will be swapped for WETH9.
    /// @return amountOut The amount of WETH9 received.
    function swapExactInputSingle(
        uint256 amountIn,
        address addressTokenIn,
        address addressTokenOut
    ) public returns (uint256 amountOut) {
        require(
            addressTokenIn != address(0) || addressTokenOut != address(0),
            "DcaKeeper: Tokens must be set"
        );

        // Approve the router to spend DAI.
        TransferHelper.safeApprove(
            addressTokenIn,
            s.uniswapRouterAddress,
            amountIn
        );

        // Naively set amountOutMinimum to 0. In production, use an oracle or other data source to choose a safer value for amountOutMinimum.
        // We also set the sqrtPriceLimitx96 to be 0 to ensure we swap our exact input amount.
        ISwapRouter.ExactInputSingleParams memory params = ISwapRouter
            .ExactInputSingleParams({
                tokenIn: addressTokenIn,
                tokenOut: addressTokenOut,
                fee: s.uniSwapPoolFees,
                recipient: address(this),
                deadline: block.timestamp,
                amountIn: amountIn,
                amountOutMinimum: 0,
                sqrtPriceLimitX96: 0
            });

        // The call to `exactInputSingle` executes the swap.
        amountOut = ISwapRouter(s.uniswapRouterAddress).exactInputSingle(
            params
        );
    }
}
