from brownie import DcaDao
from web3 import Web3
from scripts.useful_scripts import get_account


def main():
    fund_contract()
    withdraw_contract()


def fund_contract():
    account = get_account()
    dca_dao = DcaDao[-1]
    tx = dca_dao.fund({"from": account, "value": Web3.Wei("0.1 ether")})
    tx.wait(1)


def withdraw_contract():
    account = get_account()
    dca_dao = DcaDao[-1]
    tx = dca_dao.withdraw({"from": account})
    tx.wait(1)
