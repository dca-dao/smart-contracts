from brownie import Contract
from brownie import (
    DiamondCutFacet,
    DiamondLoupeFacet,
    OwnershipFacet,
    DcaManagerFacet,
    DcaKeeperFacet,
    DcaDiamond,
)
from scripts.useful_scripts import get_account
from scripts.diamond_helper import *


def remove_diamond_facet(contractName):
    account = get_account()
    diamondCut = Contract.from_abi(
        "DiamondCut", DcaDiamond[-1].address, DiamondCutFacet[-1].abi
    )
    diamondCut.diamondCut(
        [
            [
                "0x0000000000000000000000000000000000000000",
                facetCutAction["Remove"],
                getSelectors(globals()[contractName]),
            ]
        ],
        "0x0000000000000000000000000000000000000000",
        b"",
        {"from": account},
    )


def deploy_diamond_facet(facet_name):
    account = get_account()
    facet = globals()[facet_name].deploy(
        {"from": account},
        publish_source=True,
    )
    return facet


def add_diamond_facet(address):
    account = get_account()
    diamondCut = Contract.from_abi(
        "DiamondCut", DcaDiamond[-1].address, DiamondCutFacet[-1].abi
    )
    diamondCut.diamondCut(
        [
            [
                address,
                facetCutAction["Add"],
                getSelectors(DcaManagerFacet),
            ]
        ],
        "0x0000000000000000000000000000000000000000",
        b"",
        {
            "from": account,
            "allow_revert": True,
            "gas_limit": 30000000,
        },
    )


def main():
    remove_diamond_facet("DcaKeeperFacet")
    # facet = deploy_diamond_facet("DcaManagerFacet")
    # add_diamond_facet(facet.address)
