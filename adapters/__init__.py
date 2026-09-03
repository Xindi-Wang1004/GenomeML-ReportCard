"""External artifact adapters → canonical fold membership payloads."""
from .tabular_membership_adapter import adapt_tabular_membership, write_canonical
from .json_fold_adapter import adapt_json_folds
from .indexed_split_adapter import adapt_indexed_split

__all__ = [
    "adapt_tabular_membership",
    "adapt_json_folds",
    "adapt_indexed_split",
    "write_canonical",
]
