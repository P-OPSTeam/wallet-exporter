from substrateinterface import SubstrateInterface
from substrateinterface.exceptions import SubstrateRequestException

from metrics_enum import MetricsUrlStatus


def get_substrate_account_balance(node_url, address, rpc_call_status_counter):
    try:
        substrate = SubstrateInterface(
            url=node_url,
        )
        result = substrate.query(
            module="System", storage_function="Account", params=[address]
        )
        balance_info = result.value["data"]["free"]

        rpc_call_status_counter.labels(
            url=node_url, status=MetricsUrlStatus.SUCCESS.value
        ).inc()
        decimals = substrate.properties.get("tokenDecimals", 0)
        symbol = substrate.properties.get("tokenSymbol", "UNIT")
        return {"balance": balance_info, "decimals": decimals, "symbol": symbol}
    except SubstrateRequestException as e:
        rpc_call_status_counter.labels(
            url=node_url, status=MetricsUrlStatus.FAILED.value
        ).inc()
        raise e
