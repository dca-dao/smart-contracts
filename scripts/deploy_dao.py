from brownie import DcaDao
from scripts.useful_scripts import get_account
from scripts.fund_and_withdraw import fund_contract, withdraw_contract


def deploy_dao():
    account = get_account()
    dca_dao = DcaDao.deploy({"from": account}, publish_source=False)
    return dca_dao


def main():
    deploy_dao()
    fund_contract()
    withdraw_contract()
