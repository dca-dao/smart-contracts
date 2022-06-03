from brownie import Staking, network
from scripts.useful_scripts import get_account


def deploy_aave():
    network.gas_limit(1000000000)
    account = get_account()
    aave = Staking.deploy("0x88757f2f99175387ab4c6a4b3067c77a695b0349", {
                          "from": account, "allow_revert": True, "gas_limit": 30000000}, publish_source=True)
    return aave


def main():
    deploy_aave()
