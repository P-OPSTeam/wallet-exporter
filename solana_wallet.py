import base64
import struct

from solana.rpc.api import Client
from solana.rpc.types import TokenAccountOpts
from solders.pubkey import Pubkey

from metrics_enum import MetricsUrlStatus


def get_solana_balance(rpc_url, address: str, rpc_call_status_counter):
    """
    Get SOL balance for a Solana wallet address.

    Args:
        rpc_url: Solana RPC endpoint URL
        address: Solana wallet address (base58 encoded)
        rpc_call_status_counter: Prometheus counter for RPC call status

    Returns:
        dict: Contains balance in SOL and symbol
    """
    try:
        client = Client(rpc_url)
        pubkey = Pubkey.from_string(address)
        response = client.get_balance(pubkey)

        if response.value is not None:
            # Convert lamports to SOL (1 SOL = 1,000,000,000 lamports)
            balance_sol = response.value / 1_000_000_000

            rpc_call_status_counter.labels(
                url=rpc_url, status=MetricsUrlStatus.SUCCESS.value
            ).inc()

            return {"balance": balance_sol, "symbol": "SOL", "decimals": 9}
        else:
            rpc_call_status_counter.labels(
                url=rpc_url, status=MetricsUrlStatus.FAILED.value
            ).inc()
            raise Exception(f"Failed to get balance for address {address}")

    except Exception as err:
        rpc_call_status_counter.labels(
            url=rpc_url, status=MetricsUrlStatus.FAILED.value
        ).inc()
        raise err


def get_solana_token_balance(
    rpc_url, address: str, token_mint: str, rpc_call_status_counter
):
    """
    Get SPL token balance for a Solana wallet address.

    Args:
        rpc_url: Solana RPC endpoint URL
        address: Solana wallet address (base58 encoded)
        token_mint: SPL token mint address
        rpc_call_status_counter: Prometheus counter for RPC call status

    Returns:
        dict: Contains token balance and metadata
    """
    try:
        client = Client(rpc_url)

        # Get token accounts by owner
        opts = TokenAccountOpts(mint=Pubkey.from_string(token_mint))
        response = client.get_token_accounts_by_owner(Pubkey.from_string(address), opts)

        if response.value:
            # Parse the token account data
            for account in response.value:
                account_data = base64.b64decode(account.account.data[0])
                # SPL token account layout: amount is at bytes 64-72 (u64)
                amount = struct.unpack("<Q", account_data[64:72])[0]

                rpc_call_status_counter.labels(
                    url=rpc_url, status=MetricsUrlStatus.SUCCESS.value
                ).inc()

                return {"balance": amount, "raw_balance": amount}

        rpc_call_status_counter.labels(
            url=rpc_url, status=MetricsUrlStatus.SUCCESS.value
        ).inc()

        return {"balance": 0, "raw_balance": 0}

    except Exception as err:
        rpc_call_status_counter.labels(
            url=rpc_url, status=MetricsUrlStatus.FAILED.value
        ).inc()
        raise err
