from operator import truediv
import pytest
import sys
from brownie import Contract
from brownie import MockDAI, MockERC20
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
