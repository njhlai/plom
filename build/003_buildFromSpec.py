#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "Andrew Rechnitzer"
__copyright__ = "Copyright (C) 2019 Andrew Rechnitzer and Colin Macdonald"
__credits__ = ["Andrew Rechnitzer", "Colin Macdonald"]
__license__ = "AGPL-3.0-or-later"
# SPDX-License-Identifier: AGPL-3.0-or-later

from collections import defaultdict
import random

from specParser import SpecParser


def buildDirectories():
    os.makedirs("examsToPrint", exist_ok=True)


def buildIDPages(exams, t, idpages):
    for p in idpages["pages"]:
        exams[t][str(p)] = 1  # ID pages are always version1
    return exams


def buildDoNotMark(exams, t, dnm):
    for p in dnm["pages"]:
        exams[t][str(p)] = 1  # Donotmark pages are always version1
    return exams


def buildExamPages(spec):
    """Build the metadata for a bunch of exams from a spec file

    Returns:
       exams: a dict keyed by [testnum][page]
    """
    exams = defaultdict(dict)
    for t in range(1, spec["numberToProduce"] + 1):
        pv = dict()
        # build the ID-pages - always version 1
        for p in spec["idPages"]["pages"]:
            pv[str(p)] = 1
        # build the DoNotMark-pages - always version 1
        for p in spec["doNotMark"]["pages"]:
            pv[str(p)] = 1
        # now build the groups
        for g in range(spec["numberOfGroups"]):  # runs from 1,2,...
            gs = str(g + 1)
            if spec[gs]["select"] == "fixed":  # all pages are version 1
                for p in spec[gs]["pages"]:
                    pv[str(p)] = 1
            elif spec[gs]["select"] == "shuffle":
                v = random.randint(
                    1, spec["sourceVersions"]
                )  # version selected randomly [1,2,..#versions]
                for p in spec[gs]["pages"]:
                    pv[str(p)] = v
            else:
                print("ERROR - problem with specification. Please check it carefully.")
                exit(1)
        exams[t] = pv
    return exams


if __name__ == "__main__":
    # buildDirectories()
    spec = SpecParser().spec
    random.seed(spec["privateSeed"])

    exams = buildExamPages(spec)
    print(exams)

    # writeExamLog(exams)
    # buildTestPDFs(spec, exams)
