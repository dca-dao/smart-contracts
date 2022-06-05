import pytest
from brownie import config, network
from brownie import (
    DiamondCutFacet,
    DiamondLoupeFacet,
    OwnershipFacet,
    DcaManagerFacet,
    DcaKeeperFacet,
    DcaDiamond,
)
from scripts.diamond_helper import facetCutAction, getSelectors
from scripts.useful_scripts import deploy_mocks, get_account, get_contract


@pytest.fixture(scope="module")
def deploy_contracts():
    owner = get_account()

    diamond_cut_facet = DiamondCutFacet.deploy({"from": owner})
    diamond_loupe_facet = DiamondLoupeFacet.deploy({"from": owner})
    ownership_facet = OwnershipFacet.deploy({"from": owner})
    dca_manager_facet = DcaManagerFacet.deploy({"from": owner})
    dca_keeper_facet = DcaKeeperFacet.deploy({"from": owner})

    cut = [
        [
            # DcaKeeperFacet
            dca_keeper_facet.address,
            facetCutAction["Add"],
            getSelectors(DcaKeeperFacet),
        ],
        [
            # DiamondLoupeFacet
            diamond_loupe_facet.address,
            facetCutAction["Add"],
            getSelectors(DiamondLoupeFacet),
        ],
        [
            # DiamondCutFacet
            diamond_cut_facet.address,
            facetCutAction["Add"],
            getSelectors(DiamondCutFacet),
        ],
        [
            # OwnershipFacet
            ownership_facet.address,
            facetCutAction["Add"],
            getSelectors(OwnershipFacet),
        ],
        [
            # DcaManagerFacet
            dca_manager_facet.address,
            facetCutAction["Add"],
            getSelectors(DcaManagerFacet),
        ],
    ]

    (mock_dai_adress, mock_weth_address) = deploy_mocks()

    diamond = DcaDiamond.deploy(
        cut,
        [
            owner,
            config["networks"][network.show_active()]["uniswap_router"],
            config["networks"][network.show_active()]["router_fees"],
            mock_dai_adress,
            mock_weth_address,
        ],
        {"from": owner},
    )

    return (
        diamond,
        diamond_cut_facet,
        diamond_loupe_facet,
        ownership_facet,
        dca_manager_facet,
        dca_keeper_facet,
    )
