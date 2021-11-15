# SPDX-License-Identifier: AGPL-3.0-or-later
# Copyright (C) 2021 Andrew Rechnitzer
# Copyright (C) 2021 Colin B. Macdonald

from collections import defaultdict
from datetime import datetime
import logging

from plom.comment_utils import generate_new_comment_ID
from plom.db.tables import Rubric, User, Test, QGroup, Tag
from plom.db.tables import plomdb


log = logging.getLogger("DB")

# ------------------
# Rubric stuff (prefix still M since is marker-stuff)


def McreateRubric(self, user_name, rubric):
    """Create a new rubric entry in the DB

    Args:
        user_name (str): name of user creating the rubric element
        rubric (dict): dict containing the rubric details.
            Must contain these fields:
            `{kind: "relative", delta: "-1", text: "blah", question: 2}`
            The following fields are optional and empty strings will be
            substituted:
            `{tags: "blah", meta: "blah"}`
            Currently, its ok if it contains other fields: they are
            ignored.

    Returns:
        tuple: `(True, key)` or `(False, err_msg)` where `key` is the
            key for the new rubric.  Can fail if missing fields.
    """
    need_fields = ("kind", "delta", "text", "question")
    optional_fields = ("tags", "meta")
    if any(x not in rubric for x in need_fields):
        return (False, "Must have all fields {}".format(need_fields))
    for f in optional_fields:
        if f not in rubric:
            rubric = rubric.copy()  # in case caller uses reference
            rubric[f] = ""
    uref = User.get(name=user_name)  # authenticated, so not-None
    with plomdb.atomic():
        # build unique key while holding atomic access
        key = generate_new_comment_ID()
        while Rubric.get_or_none(key=key) is not None:
            key = generate_new_comment_ID()
        Rubric.create(
            key=key,
            user=uref,
            question=rubric["question"],
            kind=rubric["kind"],
            delta=rubric["delta"],
            text=rubric["text"],
            creationTime=datetime.now(),
            modificationTime=datetime.now(),
            meta=rubric["meta"],
            tags=rubric["tags"],
        )
    return (True, key)


def MgetRubrics(self, question_number=None):
    # return the rubric sorted by kind, then delta, then text
    rubric_list = []
    if question_number is None:
        query = Rubric.select().order_by(Rubric.kind, Rubric.delta, Rubric.text)
    else:
        query = (
            Rubric.select()
            .where(Rubric.question == question_number)
            .order_by(Rubric.kind, Rubric.delta, Rubric.text)
        )
    for r in query:
        rubric_list.append(
            {
                "id": r.key,
                "kind": r.kind,
                "delta": r.delta,
                "text": r.text,
                "tags": r.tags,
                "meta": r.meta,
                "count": r.count,
                "created": r.creationTime.strftime("%y:%m:%d-%H:%M:%S"),
                "modified": r.modificationTime.strftime("%y:%m:%d-%H:%M:%S"),
                "username": r.user.name,
                "question_number": r.question,
            }
        )
    return rubric_list


def MmodifyRubric(self, user_name, key, change):
    """Modify or create a rubric based on an existing rubric in the DB.

    Currently this modifies the existing rubric, increasing its revision
    number.  However, this is subject to change and should be considered
    an implementation detail.  Its very likely we will move to an
    immutable model.  At any rate, the returned `new_key` should be
    considered as replacing the original and the old key should not be
    used to place new annotations.  It might however be used to find
    outdated ones to tag or otherwise update papers.

    Args:
        user_name (str): name of user creating the rubric element
        key(str): key for the rubric
        change (dict): dict containing the changes to make to the
            rubric.  Must contain these fields:
            `{kind: "relative", delta: "-1", text: "blah", tags: "blah", meta: "blah"}`
            Other fields will be ignored.  Note this means you can think
            you are changing, e.g., the question but this will silently
            not happen.
            TODO: in the future we might prevent changing the "kind"
            or the sign of the delta.

    Returns:
        tuple: `(True, new_key)` containing the newly generated key
             (which might be the old key but this is not promised),
             or `(False, "incomplete")`, or `(False, "noSuchRubric")`.
    """
    need_fields = ("delta", "text", "tags", "meta", "kind")
    if any(x not in change for x in need_fields):
        return (False, "incomplete")
    uref = User.get(name=user_name)  # authenticated, so not-None
    # check if the rubric exists made by this user - cannot modify other user's rubric
    # TODO: should we have another bail case here `(False, "notYours")`?
    # TODO: maybe manager will be able modify all rubrics.
    rref = Rubric.get_or_none(key=key, user=uref)
    if rref is None:
        return (False, "noSuchRubric")

    with plomdb.atomic():
        rref.kind = change["kind"]
        rref.delta = change["delta"]
        rref.text = change["text"]
        rref.modificationTime = datetime.now()
        rref.revision += 1
        rref.meta = change["meta"]
        rref.tags = change["tags"]
        rref.save()
    return (True, key)


def Rget_tests_using_given_rubric(self, key):
    """Given the rubric, return counts of the the number of times it is used in tests."""
    rref = Rubric.get_or_none(key=key)
    test_dict = defaultdict(int)
    if rref is None:
        return (False, "noSuchRubric")
    for arlink_ref in rref.arlinks:
        aref = arlink_ref.annotation
        # make sure the annotation is the latest one for
        # that qgroup
        qref = aref.qgroup
        if aref == qref.annotations[-1]:
            test_dict[qref.test.test_number] += 1
    return (True, test_dict)


def Rget_rubrics_in_a_given_test(self, test_number):
    """Return counts of number of times rubrics used in latest annotations of a given test (indep of question/version)"""

    tref = Test.get_or_none(test_number=test_number)
    if tref is None:
        return (False, "noSuchTest")
    rubric_dict = defaultdict(int)
    for qref in tref.qgroups:
        aref = qref.annotations[-1]
        for arlink_ref in aref.arlinks:
            rubric_dict[arlink_ref.rubric.key] += 1
    return (True, rubric_dict)


def Rget_test_rubric_count_matrix(self):
    """Return count matrix of rubric vs test_number"""
    adjacency = defaultdict(list)
    for tref in Test.select():
        tn = tref.test_number
        for qref in tref.qgroups:
            aref = qref.annotations[-1]
            for arlink_ref in aref.arlinks:
                adjacency[tn].append(arlink_ref.rubric.key)
    return adjacency


def Rget_rubric_counts(self):
    """Return dict of rubrics indexed by key containing min details and counts"""
    rubric_info = {}
    # note that the rubric-count in the rubric table is total number
    # used in all annotations not just the latest annotation
    # so we recompute the counts now.

    # Go through rubrics adding them to the above with count=0
    # and minimal info.
    for rref in Rubric.select():
        rubric_info[rref.key] = {
            "id": rref.key,
            "kind": rref.kind,
            "delta": rref.delta,
            "text": rref.text,
            "count": 0,
            "username": rref.user.name,
            "question_number": rref.question,
        }

    # now go through all rubrics that **have** been used
    # and increment the count
    for qref in QGroup.select().where(QGroup.marked == True):
        # grab latest annotation for each qgroup.
        aref = qref.annotations[-1]
        # go through the rubric links
        for arlink_ref in aref.arlinks:
            rref = arlink_ref.rubric
            rubric_info[rref.key]["count"] += 1

    return rubric_info


def Rget_rubric_details(self, key):
    """Get a given rubric by its key, return its details and all the tests using that rubric."""
    r = Rubric.get_or_none(Rubric.key == key)
    if r is None:
        return (False, "No such rubric.")
    rubric_details = {
        "id": r.key,
        "kind": r.kind,
        "delta": r.delta,
        "text": r.text,
        "tags": r.tags,
        "meta": r.meta,
        "count": r.count,
        "created": r.creationTime.strftime("%y:%m:%d-%H:%M:%S"),
        "modified": r.modificationTime.strftime("%y:%m:%d-%H:%M:%S"),
        "username": r.user.name,
        "question_number": r.question,
        "test_list": [],
    }
    # now compute all tests using that rubric.
    # find all the annotations
    import logging

    for arlink_ref in r.arlinks:
        logging.warn(f"Looking at arlink = {arlink_ref}")
        aref = arlink_ref.annotation
        logging.warn(f"Looking at aref = {aref}")
        # check if that annotation is the latests
        qref = aref.qgroup
        if aref == qref.annotations[-1]:
            rubric_details["test_list"].append(qref.test.test_number)
    # recompute the count since the original actually counts how many
    # annotations (current or not) it is used in - is an overcount.
    rubric_details["count"] = len(rubric_details["test_list"])
    return (True, rubric_details)


# ===== tag stuff


def McreateTag(self, user_name, tag_text):
    """Create a new tag entry in the DB

    Args:
        user_name (str): name of user creating the rubric element
        tag_text (str): the text of the tag

    Returns:
        tuple: `(True, key)` or `(False, err_msg)` where `key` is the
            key for the new tag.  Can fail if missing fields.
    """
    uref = User.get(name=user_name)  # authenticated, so not-None
    with plomdb.atomic():
        # build unique key while holding atomic access
        # use a 10digit key to distinguish from rubrics
        key = generate_new_comment_ID(10)
        while Tag.get_or_none(key=key) is not None:
            key = generate_new_comment_ID(10)
        Tag.create(key=key, user=uref, creationTime=datetime.now(), text=tag_text)
    return (True, key)


def MgetAllTags(self):
    """Return a list of all tags - each tag is pair (key, text)"""
    # return all the tags
    tag_list = []
    for tref in Tag.select():
        tag_list.append({"key": tref.key, "text": tref.text})
    return tag_list
