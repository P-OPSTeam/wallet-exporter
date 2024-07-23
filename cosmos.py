from utils import http_json_call


def get_coins_balances(restprovider, addr: str, rpc_call_status_counter):
    coins = {}
    try:
        d = http_json_call(
            url=f"{restprovider}/cosmos/bank/v1beta1/balances/{addr}",
            rpc_call_status_counter=rpc_call_status_counter,
            params={},
        )
        if "balances" in d:
            for i in d["balances"]:
                coins[i["denom"]] = i["amount"]
            return coins
        return 0
    except Exception as addr_balancer_err:
        raise addr_balancer_err


def get_maincoin_balance(apiprovider, addr: str, maindenom, rpc_call_status_counter):
    try:
        d = http_json_call(
            url=f"{apiprovider}/cosmos/bank/v1beta1/balances/{addr}",
            rpc_call_status_counter=rpc_call_status_counter,
            params={},
        )
        if "balances" in str(d):
            for i in d["balances"]:
                if i["denom"] == maindenom:
                    return i["amount"]
        return 0
    except Exception as addr_balancer_err:
        raise addr_balancer_err


def get_delegations(apiprovider, addr: str, maindenom, rpc_call_status_counter):
    try:
        params: dict = {}
        total_delegations = float(0)
        while True:
            d = http_json_call(
                url=f"{apiprovider}/cosmos/staking/v1beta1/delegations/{addr}",
                rpc_call_status_counter=rpc_call_status_counter,
                params=params,
            )

            for i in d["delegation_responses"]:
                if i["balance"]["denom"] == maindenom:
                    total_delegations = total_delegations + float(
                        i["balance"]["amount"]
                    )
            if d["pagination"]["next_key"] is not None:
                params = {
                    "pagination.key": d["pagination"]["next_key"],
                }
            else:
                break
        return total_delegations
    except Exception as addr_balancer_err:
        raise addr_balancer_err


def get_unbonding_delegations(apiprovider, addr: str, rpc_call_status_counter):
    try:
        params: dict = {}
        total_unbounding_delegations = float(0)
        while True:
            d = http_json_call(
                url=f"{apiprovider}/cosmos/staking/v1beta1/delegators/{addr}/unbonding_delegations",
                rpc_call_status_counter=rpc_call_status_counter,
                params=params,
            )

            for i in d["unbonding_responses"]:
                for entry in i["entries"]:
                    total_unbounding_delegations = total_unbounding_delegations + float(
                        entry["balance"]
                    )
            if d["pagination"]["next_key"] is not None:
                params = {
                    "pagination.key": d["pagination"]["next_key"],
                }
            else:
                break
        return total_unbounding_delegations
    except Exception as addr_balancer_err:
        raise addr_balancer_err


def get_rewards(apiprovider, addr: str, maindenom, rpc_call_status_counter):
    try:
        params: dict = {}
        d = http_json_call(
            url=f"{apiprovider}/cosmos/distribution/v1beta1/delegators/{addr}/rewards",
            rpc_call_status_counter=rpc_call_status_counter,
            params=params,
        )

        for i in d["total"]:
            if i["denom"] == maindenom:
                return i["amount"]
        return 0
    except Exception as addr_balancer_err:
        raise addr_balancer_err
