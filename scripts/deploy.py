from brownie import FundMe, MockV3Aggregator, network, config
from scripts.helpful_scripts import (
    deploy_mocks,
    get_account,
    LOCAL_BLOCKCHAIN_ENVIRONMENTS,
)
from web3 import Web3


# 1. Fork
# 2. Mock
#       Mock contract will go to contract/test

# Deploying to persistent ganache
# open ganache quickstart and run the deployment script again
# brownie attaching
# brownie will detect ganache blockchain and attach to it. The port should be 8545

# brownies does not keep track of development depolyment. We need to add it.


def deploy_fund_me():
    account = get_account()
    # pass the price feed address to our fundme contract
    # can pass variables to constructor function via brownie deploy function

    # if we are on a persistent network like rinkeby, use the associated address
    # otherwise, deploy mocks.

    if network.show_active() not in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        price_feed_address = config["networks"][network.show_active()][
            "eth_usd_price_feed"
        ]
    else:
        deploy_mocks()
        price_feed_address = MockV3Aggregator[-1].address

    fund_me = FundMe.deploy(
        price_feed_address,
        {"from": account},
        publish_source=config["networks"][network.show_active()].get("verify"),
    )
    print(f"Contract deploy to {fund_me.address}")
    return fund_me


def main():
    deploy_fund_me()


# fork from Alchemy.io
