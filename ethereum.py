from metrics_enum import MetricsUrlStatus, TokenType
from utils import http_json_call
from web3 import Web3


def get_evm_chains_data(rpc_call_status_counter):
    try:
        d = http_json_call(
            url="https://chainid.network/chains.json",
            rpc_call_status_counter=rpc_call_status_counter,
            params={},
        )
        return d
    except Exception as err:
        raise err


def get_chain_symbol(chain_id, chain_data):
    for chain in chain_data:
        if chain["chainId"] == chain_id:
            return chain["nativeCurrency"]["symbol"]
    return "Unknown"


def get_ethereum_balance(apiprovider, wallet, rpc_call_status_counter, chains_evm):
    try:
        balances = []
        addr = wallet["address"]

        web3 = Web3(Web3.HTTPProvider(apiprovider))
        balance = web3.eth.get_balance(addr)
        balance_ether = web3.from_wei(balance, "ether")
        chain_id = web3.eth.chain_id
        symbol = get_chain_symbol(chain_id=chain_id, chain_data=chains_evm)
        rpc_call_status_counter.labels(
            url=apiprovider, status=MetricsUrlStatus.SUCCESS.value
        ).inc()
        balances.append(
            {
                "balance": balance_ether,
                "symbol": symbol,
                "token_type": TokenType.NATIVE.value
            }
        )

        # if it is erc20
        if "contract_address" in wallet:
            contract_address = wallet["contract_address"]
            erc20_data = get_erc20_balance(
                apiprovider=apiprovider,
                addr=addr,
                contract_address=contract_address,
                rpc_call_status_counter=rpc_call_status_counter,
            )
            rpc_call_status_counter.labels(
                url=apiprovider, status=MetricsUrlStatus.SUCCESS.value
            ).inc()
            balances.append(
                {
                    "balance": erc20_data["balance"],
                    "symbol": erc20_data["symbol"],
                    "token_type": TokenType.ERC_20.value
                }
            )

        return balances
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
        {
            "constant": True,
            "inputs": [],
            "name": "symbol",
            "outputs": [{"name": "", "type": "string"}],
            "type": "function",
        },
    ]
    web3 = Web3(Web3.HTTPProvider(apiprovider))
    contract = web3.eth.contract(address=contract_address, abi=minABI)
    balance = contract.functions.balanceOf(addr).call()
    decimals = contract.functions.decimals().call()
    symbol = contract.functions.symbol().call()
    adjusted_balance = balance / (10**decimals)
    rpc_call_status_counter.labels(
        url=apiprovider, status=MetricsUrlStatus.SUCCESS.value
    ).inc()
    return {"balance": adjusted_balance, "symbol": symbol}
