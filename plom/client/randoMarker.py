#!/usr/bin/env python3
# SPDX-License-Identifier: AGPL-3.0-or-later
# Copyright (C) 2020-2021 Andrew Rechnitzer
# Copyright (C) 2020-2021 Colin B. Macdonald
# Copyright (C) 2020 Victoria Schuster

"""Randomly scribble on papers to mark them for testing purposes.

This is a very very cut-down version of Annotator, used to
automate some random marking of papers.
"""

__copyright__ = "Copyright (C) 2020-2021 Andrew Rechnitzer and others"
__credits__ = "The Plom Project Developers"
__license__ = "AGPL-3.0-or-later"

import argparse
from stdiomask import getpass
import json
import os
from pathlib import Path
import random
import sys
import tempfile
import time

from PyQt5.QtCore import Qt, QPointF, QRectF
from PyQt5.QtGui import QPainterPath, QPen
from PyQt5.QtWidgets import QApplication, QWidget

from plom.plom_exceptions import PlomTakenException, PlomExistingLoginException
from plom.client.pageview import PageView
from plom.client.pagescene import PageScene
from plom import AnnFontSizePts

from plom.client.tools import *

from plom.messenger import Messenger


# comments which will be made into rubrics by pushing them to server and getting back keys
# need different ones for each question
negativeComments = [
    (-1, "Careful"),
    (-1, "Algebra"),
    (-1, "Arithmetic"),
    (-2, "Sign error"),
    (-2, "Huh?"),
]
positiveComments = [
    (1, "Yes"),
    (1, "Nice"),
    (1, "Well done"),
    (2, "Good"),
    (2, "Clever approach"),
]
negativeRubrics = {}
positiveRubrics = {}


class RW:
    """A dummy class needed for compatibility with pagescene."""

    def changeMark(self, a, b):
        pass


class SceneParent(QWidget):
    def __init__(self, question, maxMark):
        super().__init__()
        self.view = PageView(self)
        self.ink = QPen(Qt.red, 2)
        self.question = question
        self.maxMark = maxMark
        self.rubric_widget = RW()  # a dummy class needed for compat with pagescene.

    def doStuff(self, src_img_data, saveName, maxMark, markStyle):
        self.saveName = saveName
        self.src_img_data = src_img_data

        self.scene = PageScene(self, src_img_data, saveName, maxMark, None)
        self.view.connectScene(self.scene)

    def pickleIt(self):
        lst = self.scene.pickleSceneItems()  # newest items first
        lst.reverse()  # so newest items last
        plomDict = {
            "base_images": self.src_img_data,
            "saveName": os.path.basename(self.saveName),
            "markState": self.scene.getMarkingState(),
            "maxMark": self.maxMark,
            "currentMark": self.scene.getScore(),
            "sceneItems": lst,
        }
        # save pickled file as <blah>.plom
        plomFile = self.saveName[:-3] + "plom"
        with open(plomFile, "w") as fh:
            json.dump(plomDict, fh, indent="  ")
            fh.write("\n")

    def rpt(self):
        return QPointF(
            random.randint(100, 800) / 1000 * self.X,
            random.randint(100, 800) / 1000 * self.Y,
        )

    def TQX(self):
        c = random.choice([CommandTick, CommandCross, CommandQMark])
        self.scene.undoStack.push(c(self.scene, self.rpt()))

    def BE(self):
        c = random.choice([CommandBox, CommandEllipse])
        self.scene.undoStack.push(c(self.scene, QRectF(self.rpt(), self.rpt())))

    def LA(self):
        c = random.choice([CommandArrow, CommandLine, CommandArrowDouble])
        self.scene.undoStack.push(c(self.scene, self.rpt(), self.rpt()))

    def PTH(self):
        pth = QPainterPath()
        pth.moveTo(self.rpt())
        for k in range(random.randint(1, 4)):
            pth.lineTo(self.rpt())
        c = random.choice([CommandPen, CommandHighlight, CommandPenArrow])
        self.scene.undoStack.push(c(self.scene, pth))

    def doRubric(self):
        if random.choice([-1, 1]) == 1:
            rubric = random.choice(positiveRubrics[self.question])
        else:
            rubric = random.choice(negativeRubrics[self.question])

        self.scene.changeTheRubric(
            rubric["delta"],
            rubric["text"],
            rubric["id"],
            rubric["kind"],
        )

        # only do rubric if it is legal
        if self.scene.isLegalRubric("relative", rubric["delta"]):
            self.scene.undoStack.push(
                CommandGroupDeltaText(
                    self.scene,
                    self.rpt(),
                    rubric["id"],
                    rubric["kind"],
                    rubric["delta"],
                    rubric["text"],
                )
            )
        else:  # not legal - push text
            self.scene.undoStack.push(
                CommandText(self.scene, self.rpt(), rubric["text"])
            )

    def doRandomAnnotations(self):
        br = self.scene.underImage.boundingRect()
        self.X = br.width()
        self.Y = br.height()

        for k in range(8):
            random.choice([self.TQX, self.BE, self.LA, self.PTH])()
        for k in range(5):
            # self.GDT()
            self.doRubric()
        self.scene.undoStack.push(
            CommandText(
                self.scene, QPointF(200, 100), "Random annotations for testing only."
            )
        )

    def doneAnnotating(self):
        plomFile = self.saveName[:-3] + "plom"
        self.scene.save()
        # Pickle the scene as a plom-file
        self.pickleIt()
        return self.scene.score, self.scene.get_rubrics_from_page()

    def refreshDisplayedMark(self, score):
        # needed for compat with pagescene.py
        pass

    def setModeLabels(self, mode):
        # needed for compat with pagescene.py
        pass


def annotatePaper(question, maxMark, task, src_img_data, aname, tags):
    print("Starting random marking to task {}".format(task))
    annot = SceneParent(question, maxMark)
    annot.doStuff(src_img_data, aname, maxMark, random.choice([2, 3]))
    annot.doRandomAnnotations()
    # Issue #1391: settle annotation events, avoid races with QTimers
    Qapp.processEvents()
    time.sleep(0.25)
    Qapp.processEvents()
    return annot.doneAnnotating()


def startMarking(question, version):
    maxMark = messenger.MgetMaxMark(question, version)

    while True:
        task = messenger.MaskNextTask(question, version)
        if task is None:
            print("No more tasks.")
            break
        # print("Trying to claim next ask = ", task)
        try:
            image_metadata, tags, integrity_check = messenger.MclaimThisTask(task)
        except PlomTakenException:
            print("Another user got task {}. Trying again...".format(task))
            continue

        src_img_data = [
            {"id": r[0], "md5": r[1], "orientation": 0} for r in image_metadata
        ]
        with tempfile.TemporaryDirectory() as td:
            for i, r in enumerate(src_img_data):
                obj = messenger.MrequestOneImage(task, r["id"], r["md5"])
                tmp = os.path.join(td, f"{task}.{i}.image")
                with open(tmp, "wb") as f:
                    f.write(obj)
                r["filename"] = tmp
            aFile = os.path.join(td, "argh.png")
            plomFile = aFile[:-3] + "plom"
            score, rubrics = annotatePaper(
                question, maxMark, task, src_img_data, aFile, tags
            )
            print("Score of {} out of {}".format(score, maxMark))
            messenger.MreturnMarkedTask(
                task,
                question,
                version,
                score,
                random.randint(1, 20),
                "",
                aFile,
                plomFile,
                rubrics,
                integrity_check,
                [r["md5"] for r in src_img_data],
            )


def buildRubrics(question):
    for (d, t) in positiveComments:
        com = {
            "delta": d,
            "text": t,
            "tags": "Random",
            "meta": "Randomness",
            "kind": "relative",
            "question": question,
        }
        com["id"] = messenger.McreateRubric(com)[1]
        if question in positiveRubrics:
            positiveRubrics[question].append(com)
        else:
            positiveRubrics[question] = [com]
    for (d, t) in negativeComments:
        com = {
            "delta": d,
            "text": t,
            "tags": "Random",
            "meta": "Randomness",
            "kind": "relative",
            "question": question,
        }
        com["id"] = messenger.McreateRubric(com)[1]
        if question in negativeRubrics:
            negativeRubrics[question].append(com)
        else:
            negativeRubrics[question] = [com]


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Perform marking tasks randomly, generally for testing."
    )

    parser.add_argument("-w", "--password", type=str)
    parser.add_argument("-u", "--user", type=str)
    parser.add_argument(
        "-s",
        "--server",
        metavar="SERVER[:PORT]",
        action="store",
        help="Which server to contact.",
    )
    global messenger
    global Qapp
    args = parser.parse_args()
    if args.server and ":" in args.server:
        s, p = args.server.split(":")
        messenger = Messenger(s, port=p)
    else:
        messenger = Messenger(args.server)
    messenger.start()

    # If user not specified then default to scanner
    if args.user is None:
        user = "scanner"
    else:
        user = args.user

    # get the password if not specified
    if args.password is None:
        pwd = getpass(f"Please enter the '{user}' password:")
    else:
        pwd = args.password

    # get started
    try:
        messenger.requestAndSaveToken(user, pwd)
    except PlomExistingLoginException:
        print(
            "You appear to be already logged in!\n\n"
            "  * Perhaps a previous session crashed?\n"
            "  * Do you have another scanner-script running,\n"
            "    e.g., on another computer?\n\n"
            "This script has automatically force-logout'd that user."
        )
        messenger.clearAuthorisation(user, pwd)
        exit(1)

    spec = messenger.get_spec()

    # Headless QT: https://stackoverflow.com/a/35355906
    L = sys.argv
    L.extend(["-platform", "offscreen"])
    Qapp = QApplication(L)

    for q in range(1, spec["numberOfQuestions"] + 1):
        buildRubrics(q)
        for v in range(1, spec["numberOfVersions"] + 1):
            print("Annotating question {} version {}".format(q, v))
            startMarking(q, v)

    messenger.closeUser()
    messenger.stop()

    exit(0)
