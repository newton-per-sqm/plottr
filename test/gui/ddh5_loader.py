from plottr import QtWidgets
from plottr.data import datadict_storage as dds
from plottr.gui.tools import widgetDialog
from plottr.node.tools import linearFlowchart


def loader_node(interactive=False):
    def cb(*vals):
        print(vals)

    if not interactive:
        app = QtWidgets.QApplication([])

    fc = linearFlowchart(("loader", dds.DDH5Loader))
    loader = fc.nodes()["loader"]
    dialog = widgetDialog(loader.ui, "loader")

    if not interactive:
        loader.newDataStructure.connect(cb)
        app.exec_()
    else:
        return dialog, fc
