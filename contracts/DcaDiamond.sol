// SPDX-License-Identifier: MIT
pragma solidity ^0.7.0;
pragma experimental ABIEncoderV2;

/******************************************************************************\
* Author: Nick Mudge <nick@perfectabstractions.com> (https://twitter.com/mudgen)
* EIP-2535 Diamonds: https://eips.ethereum.org/EIPS/eip-2535
*
* Implementation of a diamond.
/******************************************************************************/

import {LibDiamond} from "./libraries/LibDiamond.sol";
import {IDiamondCut} from "./interfaces/IDiamondCut.sol";
import "./libraries/AppStorage.sol";

contract DcaDiamond {
    AppStorage s;

    struct ConstructorArgs {
        address owner;
        address uniSwapRouterAddress;
        address daiAddress;
        address wEthAddress;
    }

    constructor(
        IDiamondCut.FacetCut[] memory _diamondCut,
        ConstructorArgs memory _args
    ) {
        require(
            _args.owner != address(0),
            "DcaDiamond: owner can't be address(0)"
        );
        require(
            _args.uniSwapRouterAddress != address(0),
            "DcaDiamond: uniSwapRouterAddress can't be address(0)"
        );
        require(
            _args.daiAddress != address(0),
            "DcaDiamond: daiAddress can't be address(0)"
        );
        require(
            _args.wEthAddress != address(0),
            "DcaDiamond: wEthAddress can't be address(0)"
        );

        LibDiamond.diamondCut(_diamondCut, address(0), new bytes(0));
        LibDiamond.setContractOwner(_args.owner);

        LibDiamond.DiamondStorage storage ds = LibDiamond.diamondStorage();

        s.daiAddress = _args.daiAddress;
        s.wEthAddress = _args.wEthAddress;
        s.uniSwapRouterAddress = _args.uniSwapRouterAddress;
    }

    // Find facet for function that is called and execute the
    // function if a facet is found and return any value.
    fallback() external payable {
        LibDiamond.DiamondStorage storage ds;
        bytes32 position = LibDiamond.DIAMOND_STORAGE_POSITION;
        // get diamond storage
        assembly {
            ds.slot := position
        }
        // get facet from function selector
        address facet = ds
            .facetAddressAndSelectorPosition[msg.sig]
            .facetAddress;
        require(facet != address(0), "Diamond: Function does not exist");
        // Execute external function from facet using delegatecall and return any value.
        assembly {
            // copy function selector and any arguments
            calldatacopy(0, 0, calldatasize())
            // execute function call using the facet
            let result := delegatecall(gas(), facet, 0, calldatasize(), 0, 0)
            // get any return value
            returndatacopy(0, 0, returndatasize())
            // return any return value or error back to the caller
            switch result
            case 0 {
                revert(0, returndatasize())
            }
            default {
                return(0, returndatasize())
            }
        }
    }

    receive() external payable {
        revert("Dca: Does not accept ether");
    }
}
