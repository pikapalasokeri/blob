class PointCloudCreator:
    def __init__(self, tableModel):
        self._tableModel = tableModel
        self._currentlySelected = []

    def launchCloudCreator(self, args):
        print("Launching cloud creator")
        print(self._currentlySelected)

    def updateSelection(self, selected, deselected):
        print("Updating selection")
        for modelIndex in selected.indexes():
            self._currentlySelected.append((modelIndex.row(), modelIndex.column()))
        for modelIndex in deselected.indexes():
            self._currentlySelected.remove((modelIndex.row(), modelIndex.column()))
        self._currentlySelected.sort()
