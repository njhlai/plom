import hashlib
import os
import shlex
import shutil
import subprocess
import uuid


def addKnownPage(self, t, p, v, fname, image, md5o):
    # create a filename for the image
    prefix = "t{}p{}v{}".format(str(t).zfill(4), str(p).zfill(2), v)
    while True:
        unique = "." + str(uuid.uuid4())[:8]
        newName = "pages/originalPages/" + prefix + unique + ".png"
        if not os.path.isfile(newName):
            break
    val = self.DB.uploadKnownPage(t, p, v, fname, newName, md5o)
    if val[0]:
        with open(newName, "wb") as fh:
            fh.write(image)
        md5n = hashlib.md5(open(newName, "rb").read()).hexdigest()
        assert md5n == md5o
        print("Storing {} as {} = {}".format(prefix, newName, val))
    else:
        print("Did not store page")
        print("From database = {}".format(val[1]))
    return val


def addUnknownPage(self, fname, image, md5o):
    # create a filename for the image
    prefix = "unk."
    while True:
        unique = str(uuid.uuid4())[:8]
        newName = "pages/originalPages/" + prefix + unique + ".png"
        if not os.path.isfile(newName):
            break
    val = self.DB.uploadUnknownPage(fname, newName, md5o)
    if val[0]:
        with open(newName, "wb") as fh:
            fh.write(image)
        md5n = hashlib.md5(open(newName, "rb").read()).hexdigest()
        assert md5n == md5o
        print("Storing {} = {}".format(newName, val))
    else:
        print("Did not store page")
        print("From database = {}".format(val[1]))
    return val


def addCollidingPage(self, t, p, v, fname, image, md5o):
    # create a filename for the image
    prefix = "col.t{}p{}v{}".format(str(t).zfill(4), str(p).zfill(2), v)
    while True:
        unique = "." + str(uuid.uuid4())[:8]
        newName = "pages/collidingPages/" + prefix + unique + ".png"
        if not os.path.isfile(newName):
            break
    val = self.DB.uploadCollidingPage(t, p, v, fname, newName, md5o)
    if val[0]:
        with open(newName, "wb") as fh:
            fh.write(image)
        md5n = hashlib.md5(open(newName, "rb").read()).hexdigest()
        assert md5n == md5o
        print("Storing {} as {} = {}".format(prefix, newName, val))
    else:
        print("Did not store page")
        print("From database = {}".format(val[1]))
    return val


def replaceMissingPage(self, testNumber, pageNumber, version):
    rval = self.DB.checkTestPageUnscanned(testNumber, pageNumber, version)
    if not (rval[0] and rval[1]):
        return rval
    # build a "pageNotSubmitted page"
    cmd = "python3 ./pageNotSubmitted.py {} {} {}".format(
        testNumber, pageNumber, version
    )
    subprocess.check_call(shlex.split(cmd))
    # produces a file "pns.<testNumber>.<pageNumber>.<ver>.png"
    originalName = "pns.{}.{}.{}.png".format(testNumber, pageNumber, version)
    prefix = "pages/originalPages/pns.{}p{}v{}".format(
        str(testNumber).zfill(4), str(pageNumber).zfill(2), version
    )
    while True:
        unique = "." + str(uuid.uuid4())[:8]
        newName = prefix + unique + ".png"
        if not os.path.isfile(newName):
            break
        newName = "pages/originalPages/" + prefix + unique + ".png"

    md5 = hashlib.md5(open(originalName, "rb").read()).hexdigest()
    val = self.DB.replaceMissingPage(
        testNumber, pageNumber, version, originalName, newName, md5
    )
    shutil.move(originalName, newName)
    return val


def removeScannedPage(self, testNumber, pageNumber, version):
    fnon = self.DB.checkScannedPage(testNumber, pageNumber, version)
    # returns either None or [filename, originalName, md5sum]
    if fnon is None:
        return [False, "Cannot find page"]
    # need to create a discardedPage object and move files
    newFilename = "pages/discardedPages/" + os.path.split(fnon[0])[1]
    shutil.move(fnon[0], newFilename)
    self.DB.createDiscardedPage(
        fnon[1],  # originalName
        newFilename,
        fnon[2],  # md5sum
        "Manager removed page",
        "t{}p{}v{}".format(testNumber, pageNumber, version),
    )
    rval = self.DB.removeScannedPage(testNumber, pageNumber, version)
    if (
        len(rval) == 5
    ):  # the page belonged to a marked question group - have to do something with the files
        # rval = [True, annotatedFile, md5sum, plomFile, commentFile] - save the annot file
        os.unlink(rval[3])
        os.unlink(rval[4])
        newFilename = "pages/discardedPages/" + os.path.split(rval[2])[1]
        shutil.move(rval[2], newFilename)
        self.DB.createDiscardedPage(
            "",
            newFilename,
            rval[3],
            "Page removed post annotation",
            "annot{}p{}v{}".format(testNumber, pageNumber, version),
        )
    return [True]
