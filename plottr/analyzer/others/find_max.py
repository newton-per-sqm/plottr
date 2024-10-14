from typing import Any

import numpy as np

from ..base import Analysis, AnalysisResult


class FindMax(Analysis):
    """A simple example class to illustrate the concept."""

    def analyze(
        self,
        coordinates: tuple[np.ndarray, ...] | np.ndarray,
        data: np.ndarray,
        *args: Any,
        **kwargs: Any,
    ) -> AnalysisResult:
        i = np.argmax(data)

        return AnalysisResult(dict(max_val=data[i], max_pos=coordinates[i]))
