from brownie import Staking
from scripts.useful_scripts import get_account


def deploy_aave():
    account = get_account()
    aave = Staking.deploy({"from": account}, publish_source=True)
    return aave


def main():
    deploy_aave()
