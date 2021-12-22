from brownie import FundMe, MockV3Aggregator, network, config
from scripts.helpful_scripts import (
    get_account,
    deploy_mocks,
    LOCAL_BLOCKCHAIN_ENVIRONMENTS,
    FORKED_LOCAL_ENVIRONMENTS,
)
from web3 import Web3


def deploy_fund_me():
    account = get_account()
    active_network = network.show_active()
    print(f"Current active network is {active_network}")
    if (
        active_network not in LOCAL_BLOCKCHAIN_ENVIRONMENTS
        or active_network not in FORKED_LOCAL_ENVIRONMENTS
    ):
        price_feed_address = config["networks"][active_network]["eth_usd_price_feed"]
    else:
        deploy_mocks()
        price_feed_address = MockV3Aggregator[-1].address

    fund_me = FundMe.deploy(
        price_feed_address,
        {"from": account},
        publish_source=config["networks"][active_network].get("verify"),
    )
    print(f"Contract deployed at {fund_me.address}")
    return fund_me


def main():
    deploy_fund_me()
