from typing import Any

import lmfit
import numpy as np

from ..base import Analysis, AnalysisResult


class FitResult(AnalysisResult):
    def __init__(self, lmfit_result: lmfit.model.ModelResult):
        self.lmfit_result = lmfit_result
        self.params = lmfit_result.params

    def eval(self, *args: Any, **kwargs: Any) -> np.ndarray:
        return self.lmfit_result.eval(*args, **kwargs)


class Fit(Analysis):
    @staticmethod
    def model(*arg: Any, **kwarg: Any) -> np.ndarray:
        raise NotImplementedError

    def analyze(
        self,
        coordinates: tuple[np.ndarray, ...] | np.ndarray,
        data: np.ndarray,
        dry: bool = False,
        params: dict[str, Any] = {},
        *args: Any,
        **fit_kwargs: Any,
    ) -> FitResult:
        model = lmfit.model.Model(self.model)

        _params = lmfit.Parameters()
        for pn, pv in self.guess(coordinates, data).items():
            _params.add(pn, value=pv)
        for pn, pv in params.items():
            if isinstance(pv, lmfit.Parameter):
                _params[pn] = pv
            else:
                _params[pn].set(value=pv)

        if dry:
            for pn, pv in _params.items():
                pv.set(vary=False)
        lmfit_result = model.fit(
            data, params=_params, coordinates=coordinates, **fit_kwargs
        )

        return FitResult(lmfit_result)

    @staticmethod
    def guess(
        coordinates: tuple[np.ndarray, ...] | np.ndarray, data: np.ndarray
    ) -> dict[str, Any]:
        raise NotImplementedError
