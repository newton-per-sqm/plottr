from typing import Any

import numpy as np

from plottr.analyzer.fitters.fitter_base import Fit


class T1_Decay(Fit):
    @staticmethod
    def model(coordinates: np.ndarray, amp: float, tau: float) -> np.ndarray:
        """amp * exp(-1.0 * x / tau)"""
        return amp * np.exp(-1.0 * coordinates / tau)

    @staticmethod
    def guess(
        coordinates: tuple[np.ndarray, ...] | np.ndarray, data: np.ndarray
    ) -> dict[str, Any]:
        return dict(amp=1, tau=2)


class T2_Ramsey(Fit):
    @staticmethod
    def model(
        coordinates: np.ndarray, amp: float, tau: float, freq: float, phase: float
    ) -> np.ndarray:
        """amp * exp(-1.0 * x / tau) * sin(2 * PI * freq * x + phase)"""
        return (
            amp
            * np.exp(-1.0 * coordinates / tau)
            * np.sin(2 * np.pi * freq * coordinates + phase)
        )

    @staticmethod
    def guess(
        coordinates: tuple[np.ndarray, ...] | np.ndarray, data: np.ndarray
    ) -> dict[str, Any]:
        return dict(amp=1, tau=2, freq=3, phase=4)
