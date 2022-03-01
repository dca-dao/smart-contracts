from scripts.useful_scripts import LOCAL_BLOCKCHAIN_ENVIRONMENTS, get_account
from scripts.deploy_dao import deploy_dao
from brownie import DcaDao, network, exceptions
import pytest
from web3 import Web3


@pytest.fixture
def contract():
    return DcaDao.deploy({"from": get_account()})


def test_can_fund_contract(contract):
    if network.show_active() not in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        pytest.skip()
    # Arrange
    account = get_account()
    # Act
    tx = contract.fund({"from": account, "value": Web3.toWei(0.1, "ether")})
    tx.wait(1)
    # Assert
    assert contract.addressToAmountFunded(account.address) == 0.1 * 10 ** 18


def test_can_withdraw_funded_contract(contract):
    if network.show_active() not in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        pytest.skip()
    # Arrange
    account = get_account()
    tx = contract.fund({"from": account, "value": Web3.toWei(0.1, "ether")})
    tx.wait(1)
    # Act
    before_withdraw_balance = account.balance()
    tx = contract.withdraw({"from": account})
    tx.wait(1)
    after_withdraw_balance = account.balance()
    # Assert
    assert after_withdraw_balance - before_withdraw_balance == 0.1 * 10 ** 18


def test_cannot_withdraw_when_not_funded(contract):
    if network.show_active() not in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        pytest.skip()
    # Arrange
    account = get_account()
    # Act / Assert
    with pytest.raises(exceptions.VirtualMachineError):
        contract.withdraw({"from": account})
