from typing import (
    Collection,
    Dict,
    NamedTuple,
    Set,
    Tuple,
)

from eth_typing import (
    Address,
    Hash32,
)

from eth.abc import (
    WitnessIndexAPI,
)


class AccountQueryTracker(NamedTuple):
    did_query_bytecode: bool
    slots_queried: Tuple[int, ...]


class WitnessIndex(WitnessIndexAPI):
    def __init__(
            self,
            witness_hashes: Set[Hash32],
            accounts_metadata_queried: Dict[Address, AccountQueryTracker]) -> None:

        self._trie_node_hashes = tuple(witness_hashes)
        self._accounts_metadata_queried = accounts_metadata_queried

    @property
    def hashes(self) -> Tuple[Hash32, ...]:
        return self._trie_node_hashes

    @property
    def accounts_queried(self) -> Collection[Address]:
        return self._accounts_metadata_queried.keys()

    @property
    def account_bytecodes_queried(self) -> Tuple[Address, ...]:
        return tuple(
            address
            for address, query_tracker in self._accounts_metadata_queried.items()
            if query_tracker.did_query_bytecode
        )

    def get_slots_queried(self, address: Address) -> Tuple[int, ...]:
        try:
            query_tracker = self._accounts_metadata_queried[address]
        except KeyError:
            return tuple()
        else:
            return query_tracker.slots_queried

    @property
    def total_slots_queried(self) -> int:
        """
        Summed across all accounts, how many storage slots were queried?
        """
        return sum(
            len(query_tracker.slots_queried)
            for query_tracker in self._accounts_metadata_queried.values()
        )

    # TODO do we need a `has_hash()` method for trie nodes? If so, maybe store internally as a set
