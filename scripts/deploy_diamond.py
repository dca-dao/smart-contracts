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

FACET_NAMES = [
    # "DiamondCutFacet",
    # "DiamondLoupeFacet",
    # "OwnershipFacet",
    "DcaManagerFacet",
    # "DcaKeeperFacet",
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
            [
                facet.address,
                facetCutAction["Add"],
                getSelectors(facet),
            ]
        )
        print(f"{facet_name} deployed at {facet.address}")
    return cut


def main():
    # cut = deploy_facets()

    account = get_account()
    cut = [
        [
            # DiamondLoupeFacet
            "0x3938BD8c629e07dF7854E904Ef6D98C8409Ae79a",
            facetCutAction["Add"],
            getSelectors(DiamondLoupeFacet),
        ],
        [
            # DiamondCutFacet
            "0x2aBbd99DA4F4dD8F43B1f83F4e1174e9B17B7785",
            facetCutAction["Add"],
            getSelectors(DiamondCutFacet),
        ],
        [
            # OwnershipFacet
            "0x3A3508476738Bb73C17fD84B018A7D073Ad8974C",
            facetCutAction["Add"],
            getSelectors(OwnershipFacet),
        ],
        [
            # DcaManagerFacet
            "0x3f459F3Dc4542dD64afEDb143F8A0C3eAbDD8c07",
            facetCutAction["Add"],
            getSelectors(DcaManagerFacet),
        ],
        [
            # DcaKeeperFacet
            "0x6eacbC2ce689ed1412C227f4D8A83b008cDF6879",
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
        {"from": account},
        publish_source=True,
    )
    # upgrade_diamond(cut, diamond_init)
