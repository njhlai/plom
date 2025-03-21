# SPDX-License-Identifier: AGPL-3.0-or-later
# Copyright (C) 2020-2021 Andrew Rechnitzer
# Copyright (C) 2020-2022 Colin B. Macdonald
# Copyright (C) 2020 Victoria Schuster

from PyQt5.QtCore import QPointF
from PyQt5.QtGui import QPen, QPainterPath, QColor, QBrush
from PyQt5.QtWidgets import QGraphicsPathItem, QGraphicsItem

from plom.client.tools import CommandTool, DeleteObject, UndoStackMoveMixin
from plom.client.tools import log


class CommandPen(CommandTool):
    def __init__(self, scene, path):
        super().__init__(scene)
        self.obj = PenItem(path, scene.style)
        self.do = DeleteObject(self.obj.shape())
        self.setText("Pen")

    @classmethod
    def from_pickle(cls, X, *, scene):
        """Reconstruct from a serialized form.

        Raises:
            ValueError: malformed or otherwise incorrect data
            AssertionError: there is a bug somewhere.

        Other Pen-like annotations subclasses inherit this function.
        """
        assert cls.__name__.endswith(X[0]), 'Type "{}" mismatch: "{}"'.format(X[0], cls)
        X = X[1:]
        if len(X) != 1:
            raise ValueError("wrong length of pickle data")
        # Format is X = [['m',x,y], ['l',x,y], ['l',x,y], ...]
        X = X[0]
        pth = QPainterPath()
        # unpack ['m', x, y] or ValueError
        cmd, x, y = X[0]
        if cmd != "m":
            raise ValueError("malformed start of Pen-like annotation")
        pth.moveTo(QPointF(x, y))
        for pt in X[1:]:
            # unpack ['l', x, y] or ValueError
            cmd, x, y = pt
            if cmd != "l":
                raise ValueError("malformed Pen-like annotation in interior")
            pth.lineTo(QPointF(x, y))
        return cls(scene, pth)


class PenItem(UndoStackMoveMixin, QGraphicsPathItem):
    def __init__(self, path, style):
        super().__init__()
        self.saveable = True
        self.path = path
        self.setPath(self.path)
        self.restyle(style)

        self.setFlag(QGraphicsItem.ItemIsMovable)
        self.setFlag(QGraphicsItem.ItemSendsGeometryChanges)

    def restyle(self, style):
        self.normal_thick = style["pen_width"]
        self.setPen(QPen(style["annot_color"], style["pen_width"]))

    def pickle(self):
        name = self.__class__.__name__.replace("Item", "")  # i.e., "Pen",
        pth = []
        for k in range(self.path.elementCount()):
            # e should be either a moveTo or a lineTo
            e = self.path.elementAt(k)
            if e.isMoveTo():
                pth.append(["m", e.x + self.x(), e.y + self.y()])
            else:
                if e.isLineTo():
                    pth.append(["l", e.x + self.x(), e.y + self.y()])
                else:
                    log.error("Problem pickling Pen-like path {}".format(self.path))
        return [name, pth]

    def paint(self, painter, option, widget):
        if not self.scene().itemWithinBounds(self):
            # paint a bounding rectangle out-of-bounds warning
            painter.setPen(QPen(QColor(255, 165, 0), 8))
            painter.setBrush(QBrush(QColor(255, 165, 0, 128)))
            painter.drawRoundedRect(option.rect, 10, 10)
        # paint the normal item with the default 'paint' method
        super().paint(painter, option, widget)
