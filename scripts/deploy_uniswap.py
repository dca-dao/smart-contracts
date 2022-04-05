from brownie import SwapExamples
from scripts.useful_scripts import get_account
from scripts.fund_and_withdraw import fund_contract, withdraw_contract


def deploy_dao():
    account = get_account()
    dca_dao = SwapExamples.deploy(
        "0x7a250d5630B4cF539739dF2C5dAcb4c659F2488D",
        {"from": account},
        publish_source=False,
    )
    return dca_dao


def main():
    deploy_dao()
    fund_contract()
    withdraw_contract()
