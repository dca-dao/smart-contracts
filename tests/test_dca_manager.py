import pytest
from brownie import Contract
from scripts.useful_scripts import (
    LOCAL_BLOCKCHAIN_ENVIRONMENTS,
    get_account,
    get_contract,
)
from brownie import network, exceptions

from web3 import Web3


def test_can_fund_contract(deploy_contracts):
    if network.show_active() not in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        pytest.skip()
    # Arrange
    account = get_account()
    mock_dai = get_contract("dai_token")
    dca_diamond = deploy_contracts[0]
    dca_manager_facet = deploy_contracts[4]
    dca_manager = Contract.from_abi(
        "DcaManagerFacet", dca_diamond.address, dca_manager_facet.abi
    )

    mock_dai.approve(dca_manager.address, 1000000 * 10**18, {"from": account})

    # Act
    tx = dca_manager.fundAccount(1 * 10**18, mock_dai.address, {"from": account})
    tx.wait(1)
    # Assert
    assert dca_manager.getDaiUserBalance(account.address) == 1 * 10**18


def test_can_withdraw(deploy_contracts):
    if network.show_active() not in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        pytest.skip()
    # Arrange
    account = get_account()
    mock_dai = get_contract("dai_token")
    dca_diamond = deploy_contracts[0]
    dca_manager_facet = deploy_contracts[4]
    dca_manager = Contract.from_abi(
        "DcaManagerFacet", dca_diamond.address, dca_manager_facet.abi
    )
    mock_dai.approve(dca_manager.address, 1000000 * 10**18, {"from": account})
    tx = dca_manager.fundAccount(1 * 10**18, mock_dai.address, {"from": account})
    tx.wait(1)

    # Act
    balance_before_withdraw = mock_dai.balanceOf(account.address)
    tx = dca_manager.withdraw(1 * 10**18, mock_dai, {"from": account})
    tx.wait(1)

    # Assert
    assert mock_dai.balanceOf(account.address) == balance_before_withdraw + 1 * 10**18


def test_can_set_dca_settings(deploy_contracts):
    if network.show_active() not in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        pytest.skip()
    # Arrange
    account = get_account()
    mock_dai = get_contract("dai_token")
    dca_diamond = deploy_contracts[0]
    dca_manager_facet = deploy_contracts[4]
    dca_manager = Contract.from_abi(
        "DcaManagerFacet", dca_diamond.address, dca_manager_facet.abi
    )
    mock_dai.approve(dca_manager.address, 1000000 * 10**18, {"from": account})
    tx = dca_manager.fundAccount(1 * 10**18, mock_dai.address, {"from": account})
    tx.wait(1)

    # Act
    tx = dca_manager.setDcaSettings(1 * 10**18, 86400, {"from": account})
    tx.wait(1)

    # Assert
    assert dca_manager.getUserDcaSettings(account.address) == [1 * 10**18, 86400, 0]


def test_set_dca_settings_reverted_when_wrong_inputs(deploy_contracts):
    if network.show_active() not in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        pytest.skip()
    # Arrange
    account = get_account()
    mock_dai = get_contract("dai_token")
    dca_diamond = deploy_contracts[0]
    dca_manager_facet = deploy_contracts[4]
    dca_manager = Contract.from_abi(
        "DcaManagerFacet", dca_diamond.address, dca_manager_facet.abi
    )
    mock_dai.approve(dca_manager.address, 1000000 * 10**18, {"from": account})
    tx = dca_manager.fundAccount(1 * 10**18, mock_dai.address, {"from": account})
    tx.wait(1)

    # Act/Assert
    with pytest.raises(exceptions.VirtualMachineError):
        dca_manager.setDcaSettings(1 * 10**18, 10, {"from": account})


def test_only_owner_can_change_set_dai_address(deploy_contracts):
    if network.show_active() not in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        pytest.skip()
    # Arrange
    account = get_account()
    non_owner = get_account(index=1)
    mock_dai = get_contract("dai_token")
    dca_diamond = deploy_contracts[0]
    dca_manager_facet = deploy_contracts[4]
    dca_manager = Contract.from_abi(
        "DcaManagerFacet", dca_diamond.address, dca_manager_facet.abi
    )

    # Act/Assert
    assert dca_manager.setDaiAddress(mock_dai.address, {"from": account})
    with pytest.raises(exceptions.VirtualMachineError):
        dca_manager.setDaiAddress(mock_dai.address, {"from": non_owner})


def test_only_owner_can_change_set_weth_address(deploy_contracts):
    if network.show_active() not in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        pytest.skip()
    # Arrange
    account = get_account()
    non_owner = get_account(index=1)
    mock_weth = get_contract("weth_token")
    dca_diamond = deploy_contracts[0]
    dca_manager_facet = deploy_contracts[4]
    dca_manager = Contract.from_abi(
        "DcaManagerFacet", dca_diamond.address, dca_manager_facet.abi
    )

    # Act/Assert
    assert dca_manager.setWEthAddress(mock_weth.address, {"from": account})
    with pytest.raises(exceptions.VirtualMachineError):
        dca_manager.setWEthAddress(mock_weth.address, {"from": non_owner})
