import pytest
from brownie import Contract
from scripts.useful_scripts import (
    LOCAL_BLOCKCHAIN_ENVIRONMENTS,
    get_account,
    get_contract,
)
from brownie import network, exceptions

from web3 import Web3


def test_only_owner_can_change_pool_fees(deploy_contracts):
    if network.show_active() not in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        pytest.skip()
    # Arrange
    account = get_account()
    non_owner = get_account(index=1)
    dca_diamond = deploy_contracts[0]
    dca_keeper_facet = deploy_contracts[5]
    dca_keeper = Contract.from_abi(
        "DcaKeeperFacet", dca_diamond.address, dca_keeper_facet.abi
    )

    # Act/Assert
    assert dca_keeper.setUniswapPoolFees(2000, {"from": account})
    with pytest.raises(exceptions.VirtualMachineError):
        dca_keeper.setUniswapPoolFees(2000, {"from": non_owner})


def test_only_owner_can_change_uniswap_router_address(deploy_contracts):
    if network.show_active() not in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        pytest.skip()
    # Arrange
    account = get_account()
    non_owner = get_account(index=1)
    dca_diamond = deploy_contracts[0]
    dca_keeper_facet = deploy_contracts[5]
    dca_keeper = Contract.from_abi(
        "DcaKeeperFacet", dca_diamond.address, dca_keeper_facet.abi
    )

    # Act/Assert
    assert dca_keeper.setUniswapRouterAddress(
        "0xE592427A0AEce92De3Edee1F18E0157C05861564", {"from": account}
    )
    with pytest.raises(exceptions.VirtualMachineError):
        dca_keeper.setUniswapRouterAddress(
            "0xE592427A0AEce92De3Edee1F18E0157C05861564", {"from": non_owner}
        )


def test_get_total_to_swap(deploy_contracts):
    if network.show_active() not in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        pytest.skip()
    # Arrange
    account_1 = get_account()
    account_2 = get_account(index=1)
    mock_dai = get_contract("dai_token")
    dca_diamond = deploy_contracts[0]
    dca_manager_facet = deploy_contracts[4]
    dca_keeper_facet = deploy_contracts[5]
    dca_manager = Contract.from_abi(
        "DcaManagerFacet", dca_diamond.address, dca_manager_facet.abi
    )
    dca_keeper = Contract.from_abi(
        "DcaKeeperFacet", dca_diamond.address, dca_keeper_facet.abi
    )

    # send dai to account 2
    mock_dai.transfer(account_2, 10 * 10**18, {"from": account_1})

    # fund account 1
    mock_dai.approve(dca_manager.address, 1000000 * 10**18, {"from": account_1})
    tx = dca_manager.fundAccount(1 * 10**18, mock_dai.address, {"from": account_1})
    tx.wait(1)

    # fund account 2
    mock_dai.approve(dca_manager.address, 1000000 * 10**18, {"from": account_2})
    tx = dca_manager.fundAccount(1 * 10**18, mock_dai.address, {"from": account_2})
    tx.wait(1)

    # set dca settings account 1
    tx = dca_manager.setDcaSettings(1 * 10**18, 86400, {"from": account_1})
    tx.wait(1)

    # set dca settings account 2
    tx = dca_manager.setDcaSettings(1 * 10**18, 86400, {"from": account_2})
    tx.wait(1)

    # Act/Assert
    assert dca_keeper.getTotalToSwap() == 2 * 10**18


# TODO : check why this test fails on mainnet ()
"""
def test_perfrom_up_keep(deploy_contracts):
    if network.show_active() not in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        pytest.skip()
    # Arrange
    account_1 = get_account()
    account_2 = get_account(index=1)
    mock_dai = get_contract("dai_token")
    dca_diamond = deploy_contracts[0]
    dca_manager_facet = deploy_contracts[4]
    dca_keeper_facet = deploy_contracts[5]
    dca_manager = Contract.from_abi(
        "DcaManagerFacet", dca_diamond.address, dca_manager_facet.abi
    )
    dca_keeper = Contract.from_abi(
        "DcaKeeperFacet", dca_diamond.address, dca_keeper_facet.abi
    )

    # send dai to account 2
    mock_dai.transfer(account_2, 10 * 10**18, {"from": account_1})

    # fund account 1
    mock_dai.approve(dca_manager.address, 1000000 * 10**18, {"from": account_1})
    tx = dca_manager.fundAccount(1 * 10**18, mock_dai.address, {"from": account_1})
    tx.wait(1)

    # fund account 2
    mock_dai.approve(dca_manager.address, 1000000 * 10**18, {"from": account_2})
    tx = dca_manager.fundAccount(1 * 10**18, mock_dai.address, {"from": account_2})
    tx.wait(1)

    # set dca settings account 1
    tx = dca_manager.setDcaSettings(1 * 10**18, 86400, {"from": account_1})
    tx.wait(1)

    # set dca settings account 2
    tx = dca_manager.setDcaSettings(1 * 10**18, 86400, {"from": account_2})
    tx.wait(1)

    # Act
    tx = dca_keeper.performUpkeep(b"", {"from": account_1})
    tx.wait(1)

    # Assert
    assert dca_keeper.getTotalToSwap() == 0
"""
