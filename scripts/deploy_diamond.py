from brownie import (
    DcaKeeperFacet,
    DcaManagerFacet,
    DiamondLoupeFacet,
    OwnershipFacet,
    DiamondCutFacet,
    DcaDiamond,
    network,
)
from scripts.useful_scripts import get_account
from scripts.diamond_helper import *

FACET_NAMES = [
    # "DiamondLoupeFacet",
    # "OwnershipFacet",
    # "DcaManagerFacet",
    "DcaKeeperFacet",
]


def deploy_diamond_cut():
    account = get_account()
    diamond_cut = DiamondCutFacet.deploy(
        {"from": account},
        publish_source=True,
    )
    return diamond_cut


def deploy_diamond(diamond_cut_address):
    account = get_account()
    diamond = DcaDiamond.deploy(
        diamond_cut_address,
        [
            account.address,
            "0xE592427A0AEce92De3Edee1F18E0157C05861564",
            "0x4F96Fe3b7A6Cf9725f59d353F723c1bDb64CA6Aa",
            "0xd0A1E359811322d97991E03f863a0C30C2cF029C",
        ],
        {"from": account},
        publish_source=True,
    )
    return diamond


def deploy_facets():
    account = get_account()
    cut = []
    for facet_name in FACET_NAMES:
        facet = globals()[facet_name].deploy(
            {"from": account},
            publish_source=True,
        )
        cut.append(
            {
                "facetAddress": facet.address,
                "action": facetCutAction["Add"],
                "functionSelectors": getSelectors(facet),
            }
        )
        print(f"{facet_name} deployed at {facet.address}")
    return cut


def upgrade_diamond(cut, diamond_init):
    account = get_account()
    diamond_cut = DiamondCutFacet[-1]
    tx = diamond_cut.diamondCut(
        cut, diamond_init, getSelectors(DiamondInit), {"from": account}
    )
    tx.wait(5)


def main():
    network.gas_limit(10000000000)
    # diamond_cut = deploy_diamond_cut()
    # diamond = deploy_diamond(diamond_cut.address)
    # cut = deploy_diamond_cut()
    account = get_account()
    cut = [
        [
            # DiamondLoupeFacet
            "0x91DF1CDc8623FC353A38853AD1cC429cF1D28012",
            facetCutAction["Add"],
            getSelectors(DiamondLoupeFacet),
        ],
        [
            # DiamondCutFacet
            "0xBC77d7891977ae85A005984279928C715244F513",
            facetCutAction["Add"],
            getSelectors(DiamondCutFacet),
        ],
        [
            # OwnershipFacet
            "0xbb2c1ADd512024b5AaBb7389a50BCb1aC91BA018",
            facetCutAction["Add"],
            getSelectors(OwnershipFacet),
        ],
        [
            # DcaManagerFacet
            "0xaEbe5556BAAb50bD9a3DeF796A5972F29C07E56D",
            facetCutAction["Add"],
            getSelectors(DcaManagerFacet),
        ],
        [
            # DcaKeeperFacet
            "0x2A4B02369d021d4Dbc26cc8d8c39Ffebc0238C86",
            facetCutAction["Add"],
            getSelectors(DcaKeeperFacet),
        ],
    ]

    diamond = DcaDiamond.deploy(
        cut,
        [
            account,
            "0xE592427A0AEce92De3Edee1F18E0157C05861564",
            "0x4F96Fe3b7A6Cf9725f59d353F723c1bDb64CA6Aa",
            "0xd0A1E359811322d97991E03f863a0C30C2cF029C",
        ],
        {"from": account, "gas_limit": 1000000000, "allow_revert": True},
        publish_source=True,
    )
    # upgrade_diamond(cut, diamond_init)
