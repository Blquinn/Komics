from PyQt5 import QtWidgets, QtGui, QtCore


class PhotoViewer(QtWidgets.QGraphicsView):
    def __init__(self, parent):
        super(PhotoViewer, self).__init__(parent)
        self._zoom = 0
        self._scene = QtWidgets.QGraphicsScene(self)
        self._photo = QtWidgets.QGraphicsPixmapItem()
        self._scene.addItem(self._photo)
        # self.zoomInFactor = 1.2
        # self.zoomOutFactor = 0.8
        self.setScene(self._scene)
        self.setTransformationAnchor(QtWidgets.QGraphicsView.AnchorUnderMouse)
        self.setResizeAnchor(QtWidgets.QGraphicsView.AnchorUnderMouse)
        # self.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        # self.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.setBackgroundBrush(QtGui.QBrush(QtGui.QColor(30, 30, 30)))
        self.setFrameShape(QtWidgets.QFrame.NoFrame)

    def fitInView(self):
        rect = QtCore.QRectF(self._photo.pixmap().rect())
        if not rect.isNull():
            unity = self.transform().mapRect(QtCore.QRectF(0, 0, 1, 1))
            self.scale(1 / unity.width(), 1 / unity.height())
            viewrect = self.viewport().rect()
            scenerect = self.transform().mapRect(rect)
            factor = min(viewrect.width() / scenerect.width(),
                         viewrect.height() / scenerect.height())
            self.scale(factor, factor)
            self.centerOn(rect.center())
            self._zoom = 0

    def scrollToTop(self):
        self.verticalScrollBar().setValue(0)

    def scrollHalf(self):
        size = self.verticalScrollBar().maximum()
        position = self.verticalScrollBar().value()
        # 5 is a random buffer
        if position < ((size / 2) - 5):
            self.verticalScrollBar().setValue(size/2)
            return False
        elif ((size / 2) -5) <= position < size-1:
            self.verticalScrollBar().setValue(size-1)
            return False
        else:
            return True # Switch to next picture

    def setPhoto(self, pixmap=None):
        # self._zoom = 0
        if pixmap and not pixmap.isNull():
            self.setDragMode(QtWidgets.QGraphicsView.ScrollHandDrag)
            self._photo.setPixmap(pixmap)
            self.scrollToTop()
            # self.fitInView()
        else:
            self.setDragMode(QtWidgets.QGraphicsView.NoDrag)
            self._photo.setPixmap(QtGui.QPixmap())

    def zoomFactor(self):
        return self._zoom

    def setZoomFactor(self, zoomFactor):
        self._zoom = zoomFactor

    def zoomInKeys(self):
        self._zoom += 1
        factor = 1.2
        self.scale(factor, factor)

    def zoomOutKeys(self):
        self._zoom -= 1
        factor = 0.8
        self.scale(factor, factor)

    def scrollForward(self):
        pass

    def wheelEvent(self, event):
        modifiers = QtWidgets.QApplication.keyboardModifiers()
        if modifiers == QtCore.Qt.ControlModifier:
            if not self._photo.pixmap().isNull():
                if event.angleDelta().y() > 0:
                    factor = 1.25
                    self._zoom += 1
                else:
                    factor = 0.8
                    self._zoom -= 1
                if self._zoom > 0:
                    self.scale(factor, factor)
                elif self._zoom == 0:
                    self.fitInView()
                else:
                    self._zoom = 0
        else:
            super(PhotoViewer, self).wheelEvent(event)
