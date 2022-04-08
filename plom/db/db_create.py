# SPDX-License-Identifier: AGPL-3.0-or-later
# Copyright (C) 2018-2021 Andrew Rechnitzer
# Copyright (C) 2020-2021 Colin B. Macdonald
# Copyright (C) 2021 Nicholas J H Lai

from datetime import datetime
import logging

from peewee import fn
import peewee as pw

from plom.rules import censorStudentNumber as censorID
from plom.rules import censorStudentName as censorName
from plom.db.tables import (
    Annotation,
    Bundle,
    DNMGroup,
    Group,
    IDGroup,
    IDPrediction,
    QGroup,
    Rubric,
    Test,
    TPage,
    User,
)
from plom.db.tables import plomdb

log = logging.getLogger("DB")


# Bundle creation


def createReplacementBundle(self):
    try:
        Bundle.create(name="__replacements__system__")
    except pw.IntegrityError as e:
        log.error(f"Failed to create replacement page bundle - {e}")
        return False
    return True


def doesBundleExist(self, bundle_name, md5):
    """Checks if bundle with certain name and md5sum exists.

    Args:
        bundle_name (str)
        md5 (str)

    Returns:
        2-tuple: there are 4 possibilities:
            * neither match: no matching bundle, return `(False, None)`
            * name but not md5: return `(True, "name")` - user is trying
              to upload different bundles with same name.
            * md5 but not name: return `(True, "md5sum")` - user is trying
              to upload same bundle with different name.
            * both match: return `(True, "both")` - user could be retrying
              after network failure (for example) or uploading unknown or
              colliding pages.  That is, they previously uploaded some
              from the bundle but now are uploading more (Issue #1008).
    """
    bref = Bundle.get_or_none(name=bundle_name)
    if bref is not None:
        if bref.md5sum == md5:
            return (True, "both")
        else:
            return (True, "name")
    # name not known, so just check md5sum
    if Bundle.get_or_none(md5sum=md5) is not None:
        return (True, "md5sum")
    return (False, None)


def createNewBundle(self, bundle_name, md5):
    """Checks to see if bundle exists.

    Args:
        bundle_name (str)
        md5 (str)

    Returns:
        2-tuple: If bundle exists that matches by name *xor* by md5sum
            then return `(False, "name")` or `(False, "md5sum")`.
            If bundle matches both 'name' *and* 'md5sum' then return
            `(True, skip_list)` where `skip_list` is a list of the
            page-orders from that bundle that are already in the
            system.  The scan scripts will then skip those uploads.
            If no such bundle return `(True, [])`: we have created
            the bundle and return an empty skip-list.
    """
    exists, reason = self.doesBundleExist(bundle_name, md5)
    if not exists:
        Bundle.create(name=bundle_name, md5sum=md5)
        return (True, [])
    elif reason == "both":
        bref = Bundle.get_or_none(name=bundle_name, md5sum=md5)
        skip_list = []
        for iref in bref.images:
            skip_list.append(iref.bundle_order)
        return (True, skip_list)
    else:
        return (False, reason)


# Test creation stuff
def how_many_papers_in_database(self):
    """How many papers have been created in the database."""
    return len(Test.select())


def is_paper_database_populated(self):
    """True if any papers have been created in the DB.

    The database is initially created with empty tables.  Users get added.
    This function still returns False.  Eventually `Test`s (i.e., "papers")
    get created.  Then this function returns True.
    """
    return self.how_many_papers_in_database() > 0


def nextqueue_position(self):
    lastPos = Group.select(fn.MAX(Group.queue_position)).scalar(plomdb)
    if lastPos is None:
        return 0
    return lastPos + 1


# to create one test of the db at a time


def addSingleTestToDB(self, spec, t, vmap_for_test):
    """Build a single test in the data base from spc and version_map

    Arguments:
        spec (dict): exam specification, see :func:`plom.SpecVerifier`.
        t (int): the test number to build
        vmap_for_test (dict): version map indexed by question number for
            the given test. It is a slice of the global version_map

    Returns:
        (bool, str): where bool is true if succuess, and str is a
            status string, one line per test, ending with an error
            if failure.

    Raises:
        KeyError: problems with version map or spec
        ValueError: attempt to create test n without test n-1.
            or attempts to create a test that already exists.
        RuntimeError: unexpected error, for example we were able
            to create the test but not the question groups
            associated with it.
    """
    # Cannot create test n before test n-1 (yet: Issue #1745)
    if t > 1:
        if Test.get_or_none(test_number=t - 1) is None:
            raise ValueError(f"Error creating test {t} without test {t-1}")

    status = f"Add DB row for paper {t:04}:"
    if not self.createTest(t):
        raise ValueError(f"A DB row for paper {t:04} already exists")
    if not self.createIDGroup(t, [spec["idPage"]]):
        raise RuntimeError(f"Failed to create idgroup for paper {t:04}")
    status += " ID"

    if not self.createDNMGroup(t, spec["doNotMarkPages"]):
        raise RuntimeError(f"Failed to create DoNotMark-group for paper {t:04}")
    status += " DNM"

    for g in range(spec["numberOfQuestions"]):  # runs from 0,1,2,...
        gs = str(g + 1)  # now a str and 1,2,3,...
        v = vmap_for_test[g + 1]
        if v not in range(1, spec["numberOfVersions"] + 1):
            raise KeyError(f"problem with version map for Q{gs}: v={v} out of range")
        select = spec["question"][gs]["select"]
        if select == "fix":
            vstr = "f{}".format(v)
            if v != 1:
                raise KeyError(f"v={v} but select=fix question only allows v=1")
        elif select == "shuffle":
            vstr = "v{}".format(v)
        else:
            raise KeyError(f'Invalid spec: Q{gs} unexpected select="{select}"')
        if not self.createQGroup(t, g + 1, v, spec["question"][gs]["pages"]):
            raise RuntimeError(f"Failed to create Question {gs} ver {v}")
        status += f" Q{gs}{vstr}"

    return status


def createTest(self, t):
    with plomdb.atomic():
        try:
            Test.create(test_number=t)  # must be unique
        except pw.IntegrityError as e:
            log.error("Create test {} error - {}".format(t, e))
            return False
    return True


def addTPages(self, tref, gref, t, pages, v):
    """
    For initial construction of test-pages for a test. We use these so we know what structured pages we should have.
    """
    flag = True
    with plomdb.atomic():
        for p in pages:
            try:
                TPage.create(
                    test=tref,
                    group=gref,
                    page_number=p,
                    version=v,
                    scanned=False,
                )
            except pw.IntegrityError as e:
                log.error("Adding page {} for test {} error - {}".format(p, t, e))
                flag = False
    return flag


def createIDGroup(self, t, pages):
    tref = Test.get_or_none(test_number=t)
    if tref is None:
        log.warning("Create IDGroup - No test with number {}".format(t))
        return False
    with plomdb.atomic():
        # make the Group
        gid = "i{}".format(str(t).zfill(4))
        try:
            gref = Group.create(
                test=tref,
                gid=gid,
                group_type="i",
                queue_position=self.nextqueue_position(),
            )  # must be unique
        except pw.IntegrityError as e:
            log.error(
                "Create ID for gid={} test={}: cannot create Group - {}".format(
                    gid, t, e
                )
            )
            return False
        # make the IDGroup
        try:
            IDGroup.create(test=tref, group=gref)
        except pw.IntegrityError as e:
            log.error(
                "Create ID for gid={} test={} Group={}: cannot create IDGroup - {}.".format(
                    gid, t, gref, e
                )
            )
            return False
        return self.addTPages(tref, gref, t, pages, 1)  # always version 1.


def createDNMGroup(self, t, pages):
    tref = Test.get_or_none(test_number=t)
    if tref is None:
        log.warning("Create DNM - No test with number %s", t)
        return False

    gid = "d{}".format(str(t).zfill(4))
    with plomdb.atomic():
        # make the dnmgroup
        try:
            # A DNM group may have 0 pages, in that case mark it as scanned and set status = "complete"
            scanned = True if len(pages) == 0 else False
            gref = Group.create(
                test=tref,
                gid=gid,
                group_type="d",
                scanned=scanned,
                queue_position=self.nextqueue_position(),
            )
        except pw.IntegrityError as e:
            log.error("Create DNM - cannot make Group for %s - %s", gid, e)
            return False
        try:
            DNMGroup.create(test=tref, group=gref)
        except pw.IntegrityError as e:
            log.error("Create DNM - cannot create DNMGroup of Group %s - %s", gref, e)
            return False
        return self.addTPages(tref, gref, t, pages, 1)


# def createQGroup(self, t, q, v, pages, mark):
def createQGroup(self, t, q, v, pages):
    tref = Test.get_or_none(test_number=t)
    if tref is None:
        log.warning("Create Q - No test with number {}".format(t))
        return False

    gid = "q{}g{}".format(str(t).zfill(4), q)

    with plomdb.atomic():
        # make the qgroup
        try:
            gref = Group.create(
                test=tref,
                gid=gid,
                group_type="q",
                version=v,
                queue_position=self.nextqueue_position(),
            )
        except pw.IntegrityError as e:
            log.error(
                "Create Q - cannot create group {} of Test {} error - {}".format(
                    gid, t, e
                )
            )
            return False
        try:
            # qref = QGroup.create(
            #     test=tref, group=gref, question=q, version=v, fullmark=mark
            # )
            qref = QGroup.create(test=tref, group=gref, question=q, version=v)
        except pw.IntegrityError as e:
            log.error(
                "Create Q - cannot create QGroup of question {} error - {}.".format(
                    gid, e
                )
            )
            return False
        # create annotation 0 owned by HAL
        try:
            uref = User.get(name="HAL")
            Annotation.create(qgroup=qref, edition=0, user=uref)
            # pylint: disable=no-member
            log.warn(
                f"Created edition {len(qref.annotations)} annotation for qgroup {gid}"
            )
        except pw.IntegrityError as e:
            log.error(
                "Create Q - cannot create Annotation  of question {} error - {}.".format(
                    gid, e
                )
            )
            return False

        return self.addTPages(tref, gref, t, pages, v)


def getPageVersions(self, t):
    """Get the mapping between page numbers and version for a test.

    Args:
        t (int): a paper number.

    Returns:
        dict: keys are page numbers (int) and value is the page
            version (int), or empty dict if there was no such paper.
    """
    tref = Test.get_or_none(test_number=t)
    if tref is None:
        return {}
    return {p.page_number: p.version for p in tref.tpages}


def get_question_versions(self, t):
    """Get the mapping between question numbers and versions for a test.

    Args:
        t (int): a paper number.

    Returns:
        dict: keys are question numbers (int) and value is the question
        version (int), or empty dict if there was no such paper.
    """
    tref = Test.get_or_none(test_number=t)
    if tref is None:
        return {}
    return {q.question: q.version for q in tref.qgroups}


def get_all_question_versions(self):
    """Get the mapping between question numbers and versions for all tests.

    Returns:
        dict: a dict of dicts, where the outer keys are test number (int),
        the inner keys are question numbers (int), and values are the
        question version (int).  If there are no papers yet, return an
        empty dict.
    """
    qvmap = {}
    for tref in Test.select():
        tn = tref.test_number
        qvmap[tn] = {q.question: q.version for q in tref.qgroups}
    return qvmap


def prename_paper(self, paper_number, sid, sname):
    """Prename a paper with a given student name and id. If that test
    already has a prediction of that sid, then do nothing.

    See also :func:`plom.db.db_identify.ID_predict_paper_id` which is similar.

    Args:
        paper_number (int)
        sid (str): student id.
        sname (str): student name.

    Returns:
        tuple: `(True, None, None)` if successful, `(False, 409, msg)`
        or `(False, 404, msg)` on error.  See docs in other function.
    """
    uref = User.get(name="HAL")
    # Manager calls this function, but since these are build by
    # by the plom system, we put user = HAL.

    logbase = "Manager tried to prename paper {}".format(paper_number)
    with plomdb.atomic():
        # find the test-ref
        tref = Test.get_or_none(Test.test_number == paper_number)
        if tref is None:
            msg = "denied b/c paper not found"
            log.error("{}: {}".format(logbase, msg))
            return False, 404, msg

        # check if pushing identical predicted sid to that test
        if IDPrediction.get_or_none(test=tref, student_id=sid):
            # this prediction already exists, so do nothing - just return
            return True, None, None
        # now try to create a predicted_id entry - certainty is 0.9
        try:
            IDPrediction.create(
                test=tref, user=uref, certainty=0.9, student_id=sid, student_name=sname
            )
        except pw.IntegrityError:
            log.error(f"{logbase} but student id {censorID(sid)} in use elsewhere")
            return False, 409, f"student id {sid} in use elsewhere"
        log.info(
            'Paper {} prenamed by HAL as "{}" "{}"'.format(
                paper_number, censorID(sid), censorName(sname)
            )
        )
    return True, None, None


def remove_id_from_paper(self, paper_num):
    """Remove association between student name and id and a paper.

    This returns the paper to the ones that need to be ID'd.

    Args:
        paper_num (int)

    Returns:
        bool
    """
    with plomdb.atomic():
        tref = Test.get_or_none(Test.test_number == paper_num)
        if tref is None:
            log.error("Could not unID paper %s b/c paper not found", paper_num)
            return False
        iref = tref.idgroups[0]
        if iref.status == "done":
            log.info(
                'Paper %s being unID\'d: currently ID by %s as "%s" "%s"',
                paper_num,
                iref.user.name,
                censorID(iref.student_id),
                censorName(iref.student_name),
            )
        iref.user = None
        iref.status = "todo"
        iref.student_id = None
        iref.student_name = None
        iref.identified = False
        iref.time = datetime.now()
        iref.save()
        tref.identified = False
        tref.save()
        log.info("Paper %s unID'd", paper_num)

    return True


# Create some default rubrics
def createNoAnswerRubric(self, questionNumber, maxMark):
    """Create rubrics for when no answer given for question

    Each question needs one such rubric

    Args:
        questionNumber (int)
        maxMark: the max mark for that question

    Returns:
        Bool: True if successful, False if rubric already exists.
    """
    rID = 1000 + questionNumber
    uref = User.get(name="HAL")

    if Rubric.get_or_none(rID) is None:
        Rubric.create(
            key=rID,
            delta="0",
            text="No answer given",
            kind="absolute",
            question=questionNumber,
            user=uref,
            creationTime=datetime.now(),
            modificationTime=datetime.now(),
        )
        log.info("Created no-answer-rubric for question {}".format(questionNumber))
    else:
        log.info(
            "No-answer-rubric (up) for question {} already exists".format(
                questionNumber
            )
        )
        return False

    return True
