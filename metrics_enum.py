from enum import Enum


class MetricsUrlStatus(Enum):
    SUCCESS = "success"
    FAILED = "failed"


class MetricsAccountInfo(Enum):
    BALANCE = "balance"
    DELEGATIONS = "delegations"
    UNBOUNDING_DELEGATIONS = "unbounding_delegations"
    REWARDS = "rewards"
    BOOSTS = "boosts"
    VALIDATOR_BOOSTEES = "validator_boostees"
    UNBOOSTED = "unboosted"
    QUEUED_BOOST = "queued_boost"


class NetworkType(Enum):
    COSMOS = "cosmos"
    EVM = "evm"
    SUBSTRATE = "substrate"
    BERA = "bera"
    SOLANA = "solana"


class TokenType(Enum):
    ERC_20 = "erc20"
    NATIVE = "native"
