import abc
from collections.abc import Mapping
from typing import Any, Dict


class TableRow(Mapping):
    """
    A dict-like row of a tabular ``Dataset``.

    This implements the dictionary mapping interface, but provides more
    efficient access with less data copying than converting Arrow Tables
    or Pandas DataFrames into per-row dicts. This class must be subclassed,
    with subclasses implementing ``__getitem__``, ``__iter__``, and ``__len__``.

    Concrete subclasses include ``ray.data._internal.arrow_block.ArrowRow`` and
    ``ray.data._internal.pandas_block.PandasRow``.
    """

    def __init__(self, row: Any):
        """
        Construct a ``TableRow`` (internal API).

        Args:
            row: The tabular row that backs this row mapping.
        """
        self._row = row

    @abc.abstractmethod
    def as_pydict(self) -> Dict[str, Any]:
        """Convert to a normal Python dict.

        This can create a new copy of the row.
        """
        ...

    def __str__(self):
        return str(self.as_pydict())

    def __repr__(self):
        return str(self)

    def _repr_pretty_(self, p, cycle):
        from IPython.lib.pretty import _dict_pprinter_factory

        pprinter = _dict_pprinter_factory("{", "}")
        return pprinter(self, p, cycle)
