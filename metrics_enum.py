from enum import Enum


class MetricsUrlStatus(Enum):
    SUCCESS = "success"
    FAILED = "failed"


class MetricsAccountInfo(Enum):
    BALANCE = "balance"
    DELEGATIONS = "delegations"
    UNBOUNDING_DELEGATIONS = "unbounding_delegations"
    REWARDS = "rewards"
    BOOSTEES = "boostees"
    UNBOOSTED = "unboosted"


class NetworkType(Enum):
    COSMOS = "cosmos"
    EVM = "evm"
    SUBSTRATE = "substrate"
    BERA = "bera"
