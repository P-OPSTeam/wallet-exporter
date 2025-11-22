"""Sui blockchain wallet functions"""

from metrics_enum import MetricsUrlStatus
from utils import http_json_call


def get_sui_balance(rpc_url, address, rpc_call_status_counter):
    """
    Get SUI balance for a given address using JSON-RPC

    Args:
        rpc_url: The Sui RPC endpoint URL
        address: The Sui wallet address
        rpc_call_status_counter: Prometheus counter for RPC call status

    Returns:
        list: List of balance dicts with 'balance', 'symbol', 'coin_type'
    """
    try:
        # Get all coin balances for the address
        payload = {
            "jsonrpc": "2.0",
            "id": 1,
            "method": "suix_getAllBalances",
            "params": [address],
        }

        response = http_json_call(
            url=rpc_url,
            rpc_call_status_counter=rpc_call_status_counter,
            params=payload,
            method="POST",
        )

        if "result" not in response:
            raise Exception(f"Invalid response from Sui RPC: {response}")

        balances = []

        # Process all coin types
        for coin_balance in response["result"]:
            coin_type = coin_balance.get("coinType", "")
            total_balance = int(coin_balance.get("totalBalance", 0))

            # SUI native token has 9 decimals
            if coin_type == "0x2::sui::SUI":
                balance_sui = total_balance / 10**9
                balances.append(
                    {"balance": balance_sui, "symbol": "SUI", "coin_type": coin_type}
                )
            else:
                # For other tokens, we'll need to fetch metadata
                # For now, just store the raw balance
                symbol = coin_type.split("::")[-1] if "::" in coin_type else "UNKNOWN"
                balances.append(
                    {"balance": total_balance, "symbol": symbol, "coin_type": coin_type}
                )

        # If no balances found, return zero balance for SUI
        if not balances:
            balances.append(
                {"balance": 0.0, "symbol": "SUI", "coin_type": "0x2::sui::SUI"}
            )

        rpc_call_status_counter.labels(
            url=rpc_url, status=MetricsUrlStatus.SUCCESS.value
        ).inc()

        return balances

    except Exception as err:
        rpc_call_status_counter.labels(
            url=rpc_url, status=MetricsUrlStatus.FAILED.value
        ).inc()
        raise err


def get_sui_balance_simple(rpc_url, address, rpc_call_status_counter):
    """
    Get only SUI native token balance (simplified version)

    Args:
        rpc_url: The Sui RPC endpoint URL
        address: The Sui wallet address
        rpc_call_status_counter: Prometheus counter for RPC call status

    Returns:
        float: SUI balance
    """
    try:
        payload = {
            "jsonrpc": "2.0",
            "id": 1,
            "method": "suix_getBalance",
            "params": [address, "0x2::sui::SUI"],
        }

        response = http_json_call(
            url=rpc_url,
            rpc_call_status_counter=rpc_call_status_counter,
            params=payload,
            method="POST",
        )

        if "result" not in response:
            raise Exception(f"Invalid response from Sui RPC: {response}")

        total_balance = int(response["result"].get("totalBalance", 0))
        balance_sui = total_balance / 10**9  # SUI has 9 decimals

        rpc_call_status_counter.labels(
            url=rpc_url, status=MetricsUrlStatus.SUCCESS.value
        ).inc()

        return balance_sui

    except Exception as err:
        rpc_call_status_counter.labels(
            url=rpc_url, status=MetricsUrlStatus.FAILED.value
        ).inc()
        raise err
