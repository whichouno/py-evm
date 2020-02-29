from typing import (
    Tuple,
)

from eth.abc import (
    BlockAPI,
    VirtualMachineAPI,
    WitnessIndexAPI,
)
from eth.consensus import (
    pow,
)


class POWMiningMixin(VirtualMachineAPI):
    """
    A VM that does POW mining as well. Should be used only in tests, when we
    need to programatically populate a ChainDB.
    """
    def finalize_block(self, block: BlockAPI) -> Tuple[BlockAPI, WitnessIndexAPI]:
        block, witness_index = super().finalize_block(block)
        nonce, mix_hash = pow.mine_pow_nonce(
            block.number, block.header.mining_hash, block.header.difficulty)
        return block.copy(header=block.header.copy(nonce=nonce, mix_hash=mix_hash)), witness_index
