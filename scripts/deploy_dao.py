from brownie import DcaDao
from scripts.useful_scripts import get_account


def deploy_dao():
    account = get_account()
    diploma = DcaDao.deploy({"from": account}, publish_source=False)


def main():
    deploy_dao()
