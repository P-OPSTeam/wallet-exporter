from web3 import Web3
from metrics_enum import MetricsUrlStatus


def get_ethereum_balance(apiprovider, wallet, rpc_call_status_counter):
    try:
        addr = wallet["address"]
        # if it is erc20
        if "contract_address" in wallet:
            contract_address = wallet["contract_address"]
            erc20_balance = get_erc20_balance(
                apiprovider=apiprovider,
                addr=addr,
                contract_address=contract_address,
                rpc_call_status_counter=rpc_call_status_counter,
            )
            rpc_call_status_counter.labels(
                url=apiprovider, status=MetricsUrlStatus.SUCCESS.value
            ).inc()
            return erc20_balance
        else:
            web3 = Web3(Web3.HTTPProvider(apiprovider))
            balance = web3.eth.get_balance(addr)
            balance_ether = web3.from_wei(balance, "ether")
            rpc_call_status_counter.labels(
                url=apiprovider, status=MetricsUrlStatus.SUCCESS.value
            ).inc()
            return balance_ether
    except Exception as addr_balancer_err:
        rpc_call_status_counter.labels(
            url=apiprovider, status=MetricsUrlStatus.FAILED.value
        ).inc()
        raise addr_balancer_err


def get_erc20_balance(
    apiprovider, addr: str, contract_address: str, rpc_call_status_counter
):
    minABI = [
        {
            "constant": True,
            "inputs": [{"name": "_owner", "type": "address"}],
            "name": "balanceOf",
            "outputs": [{"name": "balance", "type": "uint256"}],
            "payable": False,
            "stateMutability": "view",
            "type": "function",
        },
        {
            "constant": True,
            "inputs": [],
            "name": "decimals",
            "outputs": [{"name": "", "type": "uint8"}],
            "type": "function",
        },
    ]
    web3 = Web3(Web3.HTTPProvider(apiprovider))
    contract = web3.eth.contract(address=contract_address, abi=minABI)
    balance = contract.functions.balanceOf(addr).call()
    decimals = contract.functions.decimals().call()
    adjusted_balance = balance / (10**decimals)
    rpc_call_status_counter.labels(
        url=apiprovider, status=MetricsUrlStatus.SUCCESS.value
    ).inc()
    return adjusted_balance
