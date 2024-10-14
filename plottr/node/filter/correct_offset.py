import numpy as np

from plottr.data.datadict import DataDictBase, MeshgridDataDict
from plottr.gui.widgets import AxisSelector
from plottr.node import Node, NodeWidget, updateOption


class SubtractAverageWidget(NodeWidget):
    def __init__(self, node: Node | None = None):
        super().__init__(node=node, embedWidgetClass=AxisSelector)
        if self.widget is None:
            raise RuntimeError

        self.optSetters = {
            "averagingAxis": self.setAvgAxis,
        }

        self.optGetters = {
            "averagingAxis": self.getAvgAxis,
        }

        self.combo = self.widget.elements["Axis"]
        self.combo.connectNode(self.node)
        self.combo.dimensionSelected.connect(
            lambda x: self.signalOption("averagingAxis")
        )

    def setAvgAxis(self, val: str) -> None:
        self.combo.setCurrentText(val)

    def getAvgAxis(self) -> str:
        return self.combo.currentText()


class SubtractAverage(Node):
    nodeName = "SubtractAverage"

    useUi = True
    uiClass = SubtractAverageWidget

    def __init__(self, name: str):
        super().__init__(name)
        self._averagingAxis: str | None = None

    @property
    def averagingAxis(self) -> str | None:
        return self._averagingAxis

    @averagingAxis.setter
    @updateOption("averagingAxis")
    def averagingAxis(self, value: str) -> None:
        self._averagingAxis = value

    def process(
        self, dataIn: DataDictBase | None = None
    ) -> dict[str, DataDictBase | None] | None:
        if super().process(dataIn=dataIn) is None:
            return None
        assert dataIn is not None
        assert self.dataAxes is not None
        data = dataIn.copy()
        if self._averagingAxis in self.dataAxes and self.dataType == MeshgridDataDict:
            axidx = self.dataAxes.index(self._averagingAxis)
            for dep in dataIn.dependents():
                data_vals = np.asanyarray(data.data_vals(dep))
                avg = data_vals.mean(axis=axidx, keepdims=True)
                data[dep]["values"] -= avg

        return dict(dataOut=data)
