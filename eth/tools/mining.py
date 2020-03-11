from eth.abc import (
    BlockAPI,
    BlockEvalResult,
    VirtualMachineAPI,
)
from eth.consensus import (
    pow,
)


class POWMiningMixin(VirtualMachineAPI):
    """
    A VM that does POW mining as well. Should be used only in tests, when we
    need to programatically populate a ChainDB.
    """
    def finalize_block(self, block: BlockAPI) -> BlockEvalResult:
        block_result = super().finalize_block(block)
        block = block_result.block

        nonce, mix_hash = pow.mine_pow_nonce(
            block.number, block.header.mining_hash, block.header.difficulty)

        mined_block = block.copy(header=block.header.copy(nonce=nonce, mix_hash=mix_hash))

        return BlockEvalResult(mined_block, block_result.witness_index)
