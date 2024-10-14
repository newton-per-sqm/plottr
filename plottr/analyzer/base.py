from collections import OrderedDict
from typing import Any

import numpy as np


class Parameter:
    def __init__(self, name: str, value: Any = None, **kw: Any):
        self.name = name
        self.value = value
        self._attrs = {}
        for k, v in kw.items():
            self._attrs[k] = v

    def __getattr__(self, key: str) -> Any:
        return self._attrs[key]


class Parameters(OrderedDict):
    """A collection of parameters"""

    def add(self, name: str, **kw: Any) -> None:
        """Add/overwrite a parameter in the collection."""
        self[name] = Parameter(name, **kw)


class AnalysisResult:
    def __init__(self, parameters: dict[str, dict[str, Any] | Any]):
        self.params = Parameters()
        for k, v in parameters.items():
            if isinstance(v, dict):
                self.params.add(k, **v)
            else:
                self.params.add(k, value=v)

    def eval(self, *args: Any, **kwargs: Any) -> np.ndarray:
        """Analysis types that produce data (like filters or fits) should implement this."""
        raise NotImplementedError

    def params_to_dict(self) -> dict[str, Any]:
        """Get all analysis parameters.
        Returns a dictionary that contains one key per parameter (its name).
        Each value contains all attributes of the parameter object, except
        those whose names start with `_` and those that are callable.
        """
        ret: dict[str, Any] = {}
        for name, param in self.params.items():
            ret[name] = {}
            for n in dir(param):
                attr = getattr(param, n)
                if n[0] != "_" and not callable(attr):
                    ret[name][n] = attr
        return ret


class Analysis:
    """Basic analysis object.

    Parameters
    ----------
    coordinates
        may be a single 1d numpy array (for a single coordinate) or a tuple
        of 1d arrays (for multiple coordinates).
    data
        a 1d array of data
    """

    def __init__(
        self, coordinates: tuple[np.ndarray, ...] | np.ndarray, data: np.ndarray
    ):
        """Constructor of `Analysis`."""
        self.coordinates = coordinates
        self.data = data

    def analyze(
        self,
        coordinates: tuple[np.ndarray, ...] | np.ndarray,
        data: np.ndarray,
        *args: Any,
        **kwargs: Any,
    ) -> AnalysisResult:
        """Needs to be implemented by each inheriting class."""
        raise NotImplementedError

    def run(self, *args: Any, **kwargs: Any) -> AnalysisResult:
        return self.analyze(self.coordinates, self.data, **kwargs)


# def analyze(analysis_class: Analysis, coordinates: Union[Tuple[np.ndarray, ...], np.ndarray],
#             data: np.ndarray, **kwarg: Any) -> AnalysisResult:
#     analysis = analysis_class(coordinates, data)
#     return analysis.run(**kwarg)
