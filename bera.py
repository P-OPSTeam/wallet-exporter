import json

from web3 import Web3


def create_contract(address, abi, api):
    w3 = Web3(Web3.HTTPProvider(api))
    contract_address = Web3.to_checksum_address(address)
    with open(abi) as abi_file:
        abi_file = json.load(abi_file)

    return w3.eth.contract(address=contract_address, abi=abi_file)


def get_bera_boosts(bgt_address, wallet, api):
    bgt = create_contract(bgt_address, "./abi/BGT.json", api)
    result = bgt.functions.boosts(wallet).call()
    return result


def get_bera_boostees(bgt_address, wallet, api):
    bgt = create_contract(bgt_address, "./abi/BGT.json", api)
    result = bgt.functions.boostees(wallet).call()
    return result


def get_bera_unboosted(bgt_address, wallet, api):
    bgt = create_contract(bgt_address, "./abi/BGT.json", api)
    result = bgt.functions.unboostedBalanceOf(wallet).call()
    return result


def get_bera_queued_boost(bgt_address, wallet, api):
    bgt = create_contract(bgt_address, "./abi/BGT.json", api)
    result = bgt.functions.queuedBoost(wallet).call()
    return result
