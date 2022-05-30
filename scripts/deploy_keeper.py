from brownie import SwapExamples, DcaKeeper
from scripts.useful_scripts import get_account
from scripts.fund_and_withdraw import fund_contract, withdraw_contract


def deploy_dao():
    account = get_account()
    dca_dao = SwapExamples.deploy(
        "0xE592427A0AEce92De3Edee1F18E0157C05861564",
        {"from": account},
        publish_source=True,
    )
    return dca_dao


def deploy_dca_keeper():
    account = get_account()
    keeper_exemple = DcaKeeper.deploy(
        300,
        "0xE592427A0AEce92De3Edee1F18E0157C05861564",
        {"from": account},
        publish_source=True,
    )
    return keeper_exemple


def approuve_contract():
    # SwapExamples[0].approve(
    #    "0xaD6D458402F60fD3Bd25163575031ACDce07538D", 100, {"from": get_account()}
    # )
    pass


def main():
    deploy_dca_keeper()
