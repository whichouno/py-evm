from typing import (
    Collection,
    Dict,
    Set,
    Tuple,
)

from eth_typing import (
    Address,
    Hash32,
)

from eth.abc import (
    WitnessAPI,
)


class Witness(WitnessAPI):
    def __init__(
            self,
            witness_hashes: Set[Hash32],
            accounts_metadata_queried: Dict[Address, Tuple[bool, Tuple[int, ...]]]) -> None:

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
            for address, (was_bytecode_queried, _slots) in self._accounts_metadata_queried.items()
            if was_bytecode_queried
        )

    def get_slots_queried(self, address: Address) -> Tuple[int, ...]:
        try:
            _bytecode, slots_queried = self._accounts_metadata_queried[address]
        except KeyError:
            return tuple()
        else:
            return slots_queried

    @property
    def total_slots_queried(self) -> int:
        """
        Summed across all accounts, how many storage slots were queried?
        """
        return sum(
            len(slots_queried)
            for _bytecode, slots_queried in self._accounts_metadata_queried.values()
        )

    # TODO do we need a `has_hash()` method? If so, maybe store internally as a set
