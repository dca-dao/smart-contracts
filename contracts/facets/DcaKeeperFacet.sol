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
    // This example swaps DAI/WETH9 for single path swaps and DAI/USDC/WETH9 for multi path swaps.

    //address public constant DAI = 0x4F96Fe3b7A6Cf9725f59d353F723c1bDb64CA6Aa;
    //address public constant WETH9 = 0xd0A1E359811322d97991E03f863a0C30C2cF029C;

    // For this example, we will set the pool fee to 0.3%.
    uint24 public poolFee = 3000;

    /**
     * Use an interval in seconds and a timestamp to slow execution of Upkeep
     */
    // uint256 public immutable interval;
    // uint256 public lastTimeStamp;

    function getUniswapV2SwapRouterAddress() public view returns (address) {
        return s.uniSwapRouterAddress;
    }

    function setUniswapV2SwapRouterAddress(address _uniSwapRouterAddress)
        public
    {
        LibDiamond.enforceIsContractOwner();
        s.uniSwapRouterAddress = _uniSwapRouterAddress;
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

    function setPoolFees(uint24 _poolFee) public {
        LibDiamond.enforceIsContractOwner();
        poolFee = _poolFee;
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
            for (uint256 i = 0; i < s.accounts.length; i++) {
                if (
                    block.timestamp -
                        s.addressToDcaSettings[s.accounts[i]].lastDcaTimestamp >
                    s.addressToDcaSettings[s.accounts[i]].period
                ) {
                    s
                        .addressToDcaSettings[s.accounts[i]]
                        .lastDcaTimestamp = block.timestamp;
                }
            }
            swapExactInputSingle(totalToSwap, s.daiAddress, s.wEthAddress);
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
            s.uniSwapRouterAddress,
            amountIn
        );

        // Naively set amountOutMinimum to 0. In production, use an oracle or other data source to choose a safer value for amountOutMinimum.
        // We also set the sqrtPriceLimitx96 to be 0 to ensure we swap our exact input amount.
        ISwapRouter.ExactInputSingleParams memory params = ISwapRouter
            .ExactInputSingleParams({
                tokenIn: addressTokenIn,
                tokenOut: addressTokenOut,
                fee: poolFee,
                recipient: address(this),
                deadline: block.timestamp,
                amountIn: amountIn,
                amountOutMinimum: 0,
                sqrtPriceLimitX96: 0
            });

        // The call to `exactInputSingle` executes the swap.
        amountOut = ISwapRouter(s.uniSwapRouterAddress).exactInputSingle(
            params
        );
    }
}
