from scripts.helpful_scripts import get_account
from scripts.deploy import deploy_fund_me
from brownie import network, accounts, exceptions
import pytest


def test_fund_and_withdraw():
    account = get_account()
    fund_me = deploy_fund_me()
    entrance_fee = 250000000000  # fund_me.getEntranceFee()
    print(f"Minimum entrance_fee {entrance_fee}")
    tx1 = fund_me.fund({"from": account, "value": entrance_fee})
    tx1.wait(1)
    assert fund_me.addressToAmountFunded(account.address) == entrance_fee

    tx2 = fund_me.withdraw({"from": account})
    tx2.wait(1)
    assert fund_me.addressToAmountFunded(account.address) == 0


def test_only_owner_can_withdraw():
    if network.show_active() != "development":
        pytest.skip("only for local testing")

    fund_me = deploy_fund_me()
    bad_actor = accounts.add()

    with pytest.raises(exceptions.VirtualMachineError):
        fund_me.withdraw({"from": bad_actor})
