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
        {
            "from": account,
            "allow_revert": True,
            "gas_limit": 30000000,
        },
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


def perfrom_upkeep():
    account = get_account()
    dcaKeeper = Contract.from_abi(
        "DcaKeeperFacet", DcaDiamond[-1].address, DcaKeeperFacet[-1].abi
    )
    dcaKeeper.swapExactInputSingle(
        "1000000",
        "0x4F96Fe3b7A6Cf9725f59d353F723c1bDb64CA6Aa",
        "0xd0A1E359811322d97991E03f863a0C30C2cF029C",
        {
            "from": account,
            "allow_revert": True,
            "gas_limit": 30000000,
        },
    )


def main():
    # perfrom_upkeep()
    # remove_diamond_facet("DcaKeeperFacet")
    facet = deploy_diamond_facet("DcaKeeperFacet")
    # add_diamond_facet("0x28154e6986DE12D8688F67Cb2dE050772d31B30b")
