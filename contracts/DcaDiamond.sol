// SPDX-License-Identifier: MIT
pragma solidity ^0.7.0;
pragma experimental ABIEncoderV2;

/******************************************************************************\
* Author: Nick Mudge <nick@perfectabstractions.com> (https://twitter.com/mudgen)
* EIP-2535 Diamonds: https://eips.ethereum.org/EIPS/eip-2535
*
* Implementation of a diamond.
/******************************************************************************/

import "./libraries/LibDiamond.sol";
import "./interfaces/IDiamondLoupe.sol";
import "./interfaces/IDiamondCut.sol";
import "./interfaces/IERC173.sol";
import "./interfaces/IERC165.sol";
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
        s.lastDcaTimeStamp = block.timestamp;

        // adding ERC165 data
        ds.supportedInterfaces[type(IERC165).interfaceId] = true;
        //ds.supportedInterfaces[type(IDiamondCut).interfaceId] = true;
        ds.supportedInterfaces[type(IDiamondLoupe).interfaceId] = true;
        ds.supportedInterfaces[type(IERC173).interfaceId] = true;

        // ERC1155
        // ERC165 identifier for the main token standard.
        ds.supportedInterfaces[0xd9b67a26] = true;
    }

    // Find facet for function that is called and execute the
    // function if a facet is found and return any value.
    fallback() external payable {
        LibDiamond.DiamondStorage storage ds;
        bytes32 position = LibDiamond.DIAMOND_STORAGE_POSITION;
        assembly {
            ds.slot := position
        }
        address facet = address(bytes20(ds.facets[msg.sig]));
        require(facet != address(0), "DcaDiamond: Function does not exist");
        assembly {
            calldatacopy(0, 0, calldatasize())
            let result := delegatecall(gas(), facet, 0, calldatasize(), 0, 0)
            returndatacopy(0, 0, returndatasize())
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
        revert("DcaDiamond: Does not accept ether");
    }
}
