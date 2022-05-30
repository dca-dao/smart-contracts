from brownie import DcaManager
from scripts.useful_scripts import get_account


def deploy_dao():
    account = get_account()
    dca_dao = DcaManager.deploy({"from": account}, publish_source=True)
    return dca_dao


def main():
    deploy_dao()
