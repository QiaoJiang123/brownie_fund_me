import pytest
from scripts.helpful_scripts import get_account, LOCAL_BLOCKCHAIN_ENVIRONMENTS
from scripts.deploy import deploy_fund_me
from brownie import accounts, network, exceptions
import pytest

# brownie automatically choose default network to use, which is development. We can reset it.


def test_can_fund_and_withdraw():
    account = get_account()
    fund_me = deploy_fund_me()
    entrance_fee = fund_me.getEntranceFee() + 100
    tx = fund_me.fund({"from": account, "value": entrance_fee})
    tx.wait(1)
    assert fund_me.addressToAmountFunded(account.address) == entrance_fee
    tx2 = fund_me.withdraw({"from": account})
    tx2.wait(1)
    assert fund_me.addressToAmountFunded(account.address) == 0


def test_only_owner_can_withdraw():
    if network.show_active() not in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        pytest.skip("only for local testing")
    # account = get_account()
    fund_me = deploy_fund_me()
    bad_actor = accounts.add()
    # fund_me.withdraw({"from": bad_actor})
    with pytest.raises(exceptions.VirtualMachineError):
        fund_me.withdraw({"from": bad_actor})


# mainnet-forking, built in feature in brownie

# Where should I run my tests?
# 1. Brownie Ganache Chain with Mocks: Always
# 2. Testnets: Always (but only for integration testing)
# 3. Brownie mainnet-fork: Optional
# 4. Custom mainnet-fork: Optional
# 5. Self/Local Ganache: Not necessary, but good for tinkering.
