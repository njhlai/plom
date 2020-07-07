from aiohttp import web, MultipartWriter, MultipartReader

from .routeutils import authenticate_by_token, authenticate_by_token_required_fields
from .routeutils import validate_required_fields, log


class UploadHandler:
    def __init__(self, plomServer):
        self.server = plomServer

    async def declareBundle(self, request):
        data = await request.json()
        if not validate_required_fields(data, ["user", "token", "bundle", "md5sum"]):
            return web.Response(status=400)
        if not self.server.validate(data["user"], data["token"]):
            return web.Response(status=401)
        if not data["user"] in ["scanner", "manager"]:
            return web.Response(status=401)
        rval = self.server.declareBundle(data["bundle"], data["md5sum"])
        return web.json_response(rval, status=200)  # all fine

    async def uploadTestPage(self, request):
        reader = MultipartReader.from_response(request)

        part0 = await reader.next()  # should be parameters
        if part0 is None:  # weird error
            return web.Response(status=406)  # should have sent 3 parts
        param = await part0.json()

        if not validate_required_fields(
            param,
            [
                "user",
                "token",
                "test",
                "page",
                "version",
                "fileName",
                "md5sum",
                "bundle",
            ],
        ):
            return web.Response(status=400)
        if not self.server.validate(param["user"], param["token"]):
            return web.Response(status=401)
        if not param["user"] in ("manager", "scanner"):
            return web.Response(status=401)

        # TODO: unused, we should ensure this matches the data
        # TODO: or why bother passing those in to param?
        code = request.match_info["tpv"]

        part1 = await reader.next()  # should be the image file
        if part1 is None:  # weird error
            return web.Response(status=406)  # should have sent 3 parts
        image = await part1.read()
        # file it away.
        rmsg = self.server.addTestPage(
            param["test"],
            param["page"],
            param["version"],
            param["fileName"],
            image,
            param["md5sum"],
            param["bundle"],
        )
        return web.json_response(rmsg, status=200)  # all good

    async def uploadHWPage(self, request):
        reader = MultipartReader.from_response(request)

        part0 = await reader.next()  # should be parameters
        if part0 is None:  # weird error
            return web.Response(status=406)  # should have sent 3 parts
        param = await part0.json()

        if not validate_required_fields(
            param,
            [
                "user",
                "token",
                "sid",
                "question",
                "order",
                "fileName",
                "md5sum",
                "bundle",
            ],
        ):
            return web.Response(status=400)
        if not self.server.validate(param["user"], param["token"]):
            return web.Response(status=401)
        if not param["user"] in ("manager", "scanner"):
            return web.Response(status=401)

        part1 = await reader.next()  # should be the image file
        if part1 is None:  # weird error
            return web.Response(status=406)  # should have sent 3 parts
        image = await part1.read()
        # file it away.
        rmsg = self.server.addHWPage(
            param["sid"],
            param["question"],
            param["order"],
            param["fileName"],
            image,
            param["md5sum"],
            param["bundle"],
        )
        return web.json_response(rmsg, status=200)  # all good

    async def uploadLPage(self, request):
        reader = MultipartReader.from_response(request)

        part0 = await reader.next()  # should be parameters
        if part0 is None:  # weird error
            return web.Response(status=406)  # should have sent 3 parts
        param = await part0.json()

        if not validate_required_fields(
            param, ["user", "token", "sid", "order", "fileName", "md5sum"]
        ):
            return web.Response(status=400)
        if not self.server.validate(param["user"], param["token"]):
            return web.Response(status=401)
        if not param["user"] in ("manager", "scanner"):
            return web.Response(status=401)

        part1 = await reader.next()  # should be the image file
        if part1 is None:  # weird error
            return web.Response(status=406)  # should have sent 3 parts
        image = await part1.read()
        # file it away.
        rmsg = self.server.addLPage(
            param["sid"], param["order"], param["fileName"], image, param["md5sum"],
        )
        return web.json_response(rmsg, status=200)  # all good

    async def uploadUnknownPage(self, request):
        reader = MultipartReader.from_response(request)

        part0 = await reader.next()  # should be parameters
        if part0 is None:  # weird error
            return web.Response(status=406)  # should have sent 3 parts
        param = await part0.json()

        if not validate_required_fields(
            param, ["user", "token", "fileName", "order", "md5sum", "bundle"]
        ):
            return web.Response(status=400)
        if not self.server.validate(param["user"], param["token"]):
            return web.Response(status=401)
        if not param["user"] in ("manager", "scanner"):
            return web.Response(status=401)

        part1 = await reader.next()  # should be the image file
        if part1 is None:  # weird error
            return web.Response(status=406)  # should have sent 3 parts
        image = await part1.read()
        # file it away.
        rmsg = self.server.addUnknownPage(
            param["fileName"], image, param["order"], param["md5sum"], param["bundle"]
        )
        return web.json_response(rmsg, status=200)  # all good

    async def uploadCollidingPage(self, request):
        reader = MultipartReader.from_response(request)

        part0 = await reader.next()  # should be parameters
        if part0 is None:  # weird error
            return web.Response(status=406)  # should have sent 2 parts
        param = await part0.json()

        if not validate_required_fields(
            param, ["user", "token", "fileName", "md5sum", "test", "page", "version"]
        ):
            return web.Response(status=400)
        if not self.server.validate(param["user"], param["token"]):
            return web.Response(status=401)
        if not param["user"] in ("manager", "scanner"):
            return web.Response(status=401)

        # TODO: unused, we should ensure this matches the data
        code = request.match_info["tpv"]

        part1 = await reader.next()  # should be the image file
        if part1 is None:  # weird error
            return web.Response(status=406)  # should have sent 2 parts
        image = await part1.read()
        # file it away.
        rmsg = self.server.addCollidingPage(
            param["test"],
            param["page"],
            param["version"],
            param["fileName"],
            image,
            param["md5sum"],
        )
        return web.json_response(rmsg, status=200)  # all good

    async def replaceMissingTestPage(self, request):
        data = await request.json()
        if not validate_required_fields(
            data, ["user", "token", "test", "page", "version"]
        ):
            return web.Response(status=400)
        if not self.server.validate(data["user"], data["token"]):
            return web.Response(status=401)
        if not data["user"] == "manager":
            return web.Response(status=401)

        # TODO: unused, we should ensure this matches the data
        code = request.match_info["tpv"]

        rval = self.server.replaceMissingTestPage(
            data["test"], data["page"], data["version"]
        )
        if rval[0]:
            return web.json_response(rval, status=200)  # all fine
        else:
            return web.Response(status=404)  # page not found at all

    async def replaceMissingHWQuestion(self, request):
        data = await request.json()
        if not validate_required_fields(data, ["user", "token", "sid", "question"]):
            return web.Response(status=400)
        if not self.server.validate(data["user"], data["token"]):
            return web.Response(status=401)
        if data["user"] != "manager" and data["user"] != "scanner":
            return web.Response(status=401)

        rval = self.server.replaceMissingHWQuestion(data["sid"], data["question"])
        if rval[0]:
            return web.json_response(rval, status=200)  # all fine
        elif rval[1]:
            return web.Response(status=409)  # that question already has pages
        else:
            return web.Response(status=404)  # page not found at all

    async def removeAllScannedPages(self, request):
        data = await request.json()
        print("Got data {}".format(data))
        if not validate_required_fields(data, ["user", "token", "test",],):
            return web.Response(status=400)
        if not self.server.validate(data["user"], data["token"]):
            return web.Response(status=401)
        if not data["user"] == "manager":
            return web.Response(status=401)

        rval = self.server.removeAllScannedPages(data["test"],)
        if rval[0]:
            return web.json_response(rval, status=200)  # all fine
        else:
            return web.Response(status=404)  # page not found at all

    async def getUnknownPageNames(self, request):
        data = await request.json()
        if not validate_required_fields(data, ["user", "token"]):
            return web.Response(status=400)
        if not self.server.validate(data["user"], data["token"]):
            return web.Response(status=401)
        if not data["user"] == "manager":
            return web.Response(status=401)

        rval = self.server.getUnknownPageNames()
        return web.json_response(rval, status=200)  # all fine

    async def getDiscardNames(self, request):
        data = await request.json()
        if not validate_required_fields(data, ["user", "token"]):
            return web.Response(status=400)
        if not self.server.validate(data["user"], data["token"]):
            return web.Response(status=401)
        if not data["user"] == "manager":
            return web.Response(status=401)

        rval = self.server.getDiscardNames()
        return web.json_response(rval, status=200)  # all fine

    async def getCollidingPageNames(self, request):
        data = await request.json()
        if not validate_required_fields(data, ["user", "token"]):
            return web.Response(status=400)
        if not self.server.validate(data["user"], data["token"]):
            return web.Response(status=401)
        if not data["user"] == "manager":
            return web.Response(status=401)

        rval = self.server.getCollidingPageNames()
        return web.json_response(rval, status=200)  # all fine

    async def getTPageImage(self, request):
        data = await request.json()
        if not validate_required_fields(
            data, ["user", "token", "test", "page", "version"]
        ):
            return web.Response(status=400)
        if not self.server.validate(data["user"], data["token"]):
            return web.Response(status=401)
        if not data["user"] == "manager":
            return web.Response(status=401)

        rval = self.server.getTPageImage(data["test"], data["page"], data["version"])
        if rval[0]:
            return web.FileResponse(rval[1], status=200)  # all fine
        else:
            return web.Response(status=404)

    async def getHWPageImage(self, request):  # should this use version too?
        data = await request.json()
        if not validate_required_fields(
            data, ["user", "token", "test", "question", "order"]
        ):
            return web.Response(status=400)
        if not self.server.validate(data["user"], data["token"]):
            return web.Response(status=401)
        if not data["user"] == "manager":
            return web.Response(status=401)

        rval = self.server.getHWPageImage(data["test"], data["question"], data["order"])
        if rval[0]:
            return web.FileResponse(rval[1], status=200)  # all fine
        else:
            return web.Response(status=404)

    async def getLPageImage(self, request):
        data = await request.json()
        if not validate_required_fields(data, ["user", "token", "test", "order"]):
            return web.Response(status=400)
        if not self.server.validate(data["user"], data["token"]):
            return web.Response(status=401)
        if not data["user"] == "manager":
            return web.Response(status=401)

        rval = self.server.getLPageImage(data["test"], data["order"])
        if rval[0]:
            return web.FileResponse(rval[1], status=200)  # all fine
        else:
            return web.Response(status=404)

    async def getUnknownImage(self, request):
        data = await request.json()
        if not validate_required_fields(data, ["user", "token", "fileName"]):
            return web.Response(status=400)
        if not self.server.validate(data["user"], data["token"]):
            return web.Response(status=401)
        if not data["user"] == "manager":
            return web.Response(status=401)

        rval = self.server.getUnknownImage(data["fileName"])
        if rval[0]:
            return web.FileResponse(rval[1], status=200)  # all fine
        else:
            return web.Response(status=404)

    async def getDiscardImage(self, request):
        data = await request.json()
        if not validate_required_fields(data, ["user", "token", "fileName"]):
            return web.Response(status=400)
        if not self.server.validate(data["user"], data["token"]):
            return web.Response(status=401)
        if not data["user"] == "manager":
            return web.Response(status=401)

        rval = self.server.getDiscardImage(data["fileName"])
        if rval[0]:
            return web.FileResponse(rval[1], status=200)  # all fine
        else:
            return web.Response(status=404)

    async def getCollidingImage(self, request):
        data = await request.json()
        if not validate_required_fields(data, ["user", "token", "fileName"]):
            return web.Response(status=400)
        if not self.server.validate(data["user"], data["token"]):
            return web.Response(status=401)
        if not data["user"] == "manager":
            return web.Response(status=401)

        rval = self.server.getCollidingImage(data["fileName"])
        if rval[0]:
            return web.FileResponse(rval[1], status=200)  # all fine
        else:
            return web.Response(status=404)

    # @route.get("/admin/questionImages")
    @authenticate_by_token_required_fields(["user", "test", "question"])
    def getQuestionImages(self, data, request):
        if not data["user"] == "manager":
            return web.Response(status=401)

        rmsg = self.server.getQuestionImages(data["test"], data["question"])
        # returns either [True, fname1,fname2,..,fname.n] or [False, error]
        if rmsg[0]:
            with MultipartWriter("images") as mpwriter:
                for fn in rmsg[1:]:
                    mpwriter.append(open(fn, "rb"))
            return web.Response(body=mpwriter, status=200)
        else:
            return web.Response(status=404)  # couldnt find that test/question

    # @routes.get("/admin/testImages")
    @authenticate_by_token_required_fields(["user", "test"])
    def getAllTestImages(self, data, request):
        if not data["user"] == "manager":
            return web.Response(status=401)

        rmsg = self.server.getAllTestImages(data["test"])
        # returns either [True, fname1,fname2,..,fname.n] or [False, error]
        if rmsg[0]:
            with MultipartWriter("images") as mpwriter:
                for fn in rmsg[1:]:
                    if fn == "":
                        mpwriter.append("")
                    else:
                        mpwriter.append(open(fn, "rb"))
            return web.Response(body=mpwriter, status=200)
        else:
            return web.Response(status=404)  # couldnt find that test/question

    async def checkTPage(self, request):
        data = await request.json()
        if not validate_required_fields(data, ["user", "token", "test", "page"]):
            return web.Response(status=400)
        if not self.server.validate(data["user"], data["token"]):
            return web.Response(status=401)
        if not data["user"] == "manager":
            return web.Response(status=401)

        rmsg = self.server.checkTPage(data["test"], data["page"])
        # returns either [True, "collision", version, fname], [True, "scanned", version] or [False]
        if rmsg[0]:
            with MultipartWriter("images") as mpwriter:
                mpwriter.append("{}".format(rmsg[1]))  # append "collision" or "scanned"
                mpwriter.append("{}".format(rmsg[2]))  # append "version"
                if len(rmsg) == 4:  # append the image.
                    mpwriter.append(open(rmsg[3], "rb"))
            return web.Response(body=mpwriter, status=200)
        else:
            return web.Response(status=404)  # couldnt find that test/question

    async def removeUnknownImage(self, request):
        data = await request.json()
        if not validate_required_fields(data, ["user", "token", "fileName"]):
            return web.Response(status=400)
        if not self.server.validate(data["user"], data["token"]):
            return web.Response(status=401)
        if not data["user"] == "manager":
            return web.Response(status=401)

        rval = self.server.removeUnknownImage(data["fileName"])
        if rval[0]:
            return web.Response(status=200)  # all fine
        else:
            return web.Response(status=404)

    async def removeCollidingImage(self, request):
        data = await request.json()
        if not validate_required_fields(data, ["user", "token", "fileName"]):
            return web.Response(status=400)
        if not self.server.validate(data["user"], data["token"]):
            return web.Response(status=401)
        if not data["user"] == "manager":
            return web.Response(status=401)

        rval = self.server.removeCollidingImage(data["fileName"])
        if rval[0]:
            return web.Response(status=200)  # all fine
        else:
            return web.Response(status=404)

    async def unknownToTestPage(self, request):
        data = await request.json()
        if not validate_required_fields(
            data, ["user", "token", "fileName", "test", "page", "rotation"]
        ):
            return web.Response(status=400)
        if not self.server.validate(data["user"], data["token"]):
            return web.Response(status=401)
        if not data["user"] == "manager":
            return web.Response(status=401)

        rval = self.server.unknownToTestPage(
            data["fileName"], data["test"], data["page"], data["rotation"]
        )
        if rval[0]:
            return web.json_response(rval[1], status=200)  # all fine
        else:
            return web.Response(status=404)

    async def unknownToExtraPage(self, request):
        data = await request.json()
        if not validate_required_fields(
            data, ["user", "token", "fileName", "test", "question", "rotation"]
        ):
            return web.Response(status=400)
        if not self.server.validate(data["user"], data["token"]):
            return web.Response(status=401)
        if not data["user"] == "manager":
            return web.Response(status=401)

        rval = self.server.unknownToExtraPage(
            data["fileName"], data["test"], data["question"], data["rotation"]
        )
        if rval[0]:
            return web.Response(status=200)  # all fine
        else:
            return web.Response(status=404)

    async def collidingToTestPage(self, request):
        data = await request.json()
        if not validate_required_fields(
            data, ["user", "token", "fileName", "test", "page", "version"]
        ):
            return web.Response(status=400)
        if not self.server.validate(data["user"], data["token"]):
            return web.Response(status=401)
        if not data["user"] == "manager":
            return web.Response(status=401)

        rval = self.server.collidingToTestPage(
            data["fileName"], data["test"], data["page"], data["version"]
        )
        if rval[0]:
            return web.Response(status=200)  # all fine
        else:
            return web.Response(status=404)

    async def discardToUnknown(self, request):
        data = await request.json()
        if not validate_required_fields(data, ["user", "token", "fileName"]):
            return web.Response(status=400)
        if not self.server.validate(data["user"], data["token"]):
            return web.Response(status=401)
        if not data["user"] == "manager":
            return web.Response(status=401)

        rval = self.server.discardToUnknown(data["fileName"])
        if rval[0]:
            return web.Response(status=200)  # all fine
        else:
            return web.Response(status=404)

    async def processHWUploads(self, request):
        data = await request.json()
        if not validate_required_fields(data, ["user", "token"]):
            return web.Response(status=400)
        if not self.server.validate(data["user"], data["token"]):
            return web.Response(status=401)
        if data["user"] != "manager" and data["user"] != "scanner":
            return web.Response(status=401)

        rval = self.server.processHWUploads()
        return web.json_response(
            rval[1], status=200
        )  # all fine - report number of tests updated

    async def processLUploads(self, request):
        data = await request.json()
        if not validate_required_fields(data, ["user", "token"]):
            return web.Response(status=400)
        if not self.server.validate(data["user"], data["token"]):
            return web.Response(status=401)
        if data["user"] != "manager" and data["user"] != "scanner":
            return web.Response(status=401)

        rval = self.server.processLUploads()
        return web.json_response(
            rval[1], status=200
        )  # all fine - report number of tests updated

    async def processTUploads(self, request):
        data = await request.json()
        if not validate_required_fields(data, ["user", "token"]):
            return web.Response(status=400)
        if not self.server.validate(data["user"], data["token"]):
            return web.Response(status=401)
        if data["user"] != "manager" and data["user"] != "scanner":
            return web.Response(status=401)

        rval = self.server.processTUploads()
        return web.json_response(
            rval[1], status=200
        )  # all fine - report number of tests updated

    @authenticate_by_token_required_fields(["user"])
    def populateExamDatabase(self, data, request):
        """Instruct the server to generate paper data in the database.

        TODO: maybe the api call should just be for one row of the database.

        TODO: or maybe we can pass the page-to-version mapping to this?
        """
        if not data["user"] == "manager":
            return web.Response(status=400)  # malformed request.

        from plom.db import buildExamDatabaseFromSpec

        # TODO this is not the design we have elsewhere, should call helper function
        try:
            r, summary = buildExamDatabaseFromSpec(self.server.testSpec, self.server.DB)
        except ValueError:
            raise web.HTTPConflict(
                reason="Database already present: not overwriting"
            ) from None
        if r:
            return web.Response(text=summary, status=200)
        else:
            raise web.HTTPInternalServerError(text=summary)

    # TODO: would be nice to use @authenticate_by_token, see comments in routeutils.py
    @authenticate_by_token_required_fields([])
    def getPageVersionMap(self, data, request):
        """Get the mapping between page number and version for one test.

        Returns:
            dict: keyed by page number.  Note keys are strings b/c of
                json limitations; you may want to convert back to int.
        """
        spec = self.server.testSpec
        paper_idx = request.match_info["papernum"]
        ver = self.server.DB.getPageVersions(paper_idx)
        if ver:
            return web.json_response(ver, status=200)
        else:
            return web.Response(status=404)

    @authenticate_by_token_required_fields([])
    def getGlobalPageVersionMap(self, data, request):
        """Get the mapping between page number and version for all tests.

        Returns:
            dict: dict of dicts, keyed first by paper index then by page
                number.  Both keys are strings b/c of json limitations;
                you may need to iterate and convert back to int.  Fails
                with 500 Internal Server Error if a test does not exist.
        """
        spec = self.server.testSpec
        vers = {}
        for paper_idx in range(1, spec["numberToProduce"] + 1):
            ver = self.server.DB.getPageVersions(paper_idx)
            if not ver:
                return web.Response(status=500)
            vers[paper_idx] = ver
        # JSON converts int keys to strings, we'll fix this at the far end
        # return web.json_response(str(pickle.dumps(vers)), status=200)
        return web.json_response(vers, status=200)

    # @route.put("/admin/pdf_produced/{t}")
    @authenticate_by_token_required_fields(["user"])
    def notify_pdf_of_paper_produced(self, data, request):
        """Inform server that a PDF for this paper has been produced.

        This is to be called one-at-a-time for each paper.  If this is a
        bottleneck we could consider adding a "bulk" version.

        Note that the file itself is not uploaded to the server: we're
        just merely creating a record that such a file exists somewhere.

        TODO: pass in md5sum too and if its unchanged no need to
        complain about conflict, just quietly return 200.
        TODO: implement force as mentioned below.

        Inputs:
            t (int?, str?): part of URL that specifies the paper number.
            user (str): who's calling?  A field of the request.
            force (bool): force production even if paper already exists.
            md5sum (str): md5sum of the file that was produced.

        Returns:
            aiohttp.web.Response: with status code as below.

        Status codes:
            200 OK: the info was recorded.
            400 Bad Request: only "manager" is allowed to do this.
            401 Unauthorized: invalid credientials.
            404 Not Found: paper number is outside valid range.
            409 Conflict: this paper has already been produced, so its
                unusual to be making it again. Maybe try `force=True`.
        """
        if not data["user"] == "manager":
            return web.Response(status=400)
        # force_flag = request.match_info["force"]
        paper_idx = request.match_info["papernum"]
        try:
            self.server.DB.produceTest(paper_idx)
        except IndexError:
            return web.Response(status=404)
        except ValueError:
            return web.Response(status=409)
        return web.Response(status=200)

    def setUpRoutes(self, router):
        router.add_put("/admin/bundle", self.declareBundle)
        router.add_put("/admin/testPages/{tpv}", self.uploadTestPage)
        router.add_put("/admin/hwPages", self.uploadHWPage)
        router.add_put("/admin/lPages", self.uploadLPage)
        router.add_put("/admin/unknownPages", self.uploadUnknownPage)
        router.add_put("/admin/collidingPages/{tpv}", self.uploadCollidingPage)
        router.add_put("/admin/missingTestPage/{tpv}", self.replaceMissingTestPage)
        router.add_put("/admin/missingHWQuestion", self.replaceMissingHWQuestion)
        router.add_delete("/admin/scannedPages", self.removeAllScannedPages)
        router.add_get("/admin/scannedTPage", self.getTPageImage)
        router.add_get("/admin/scannedHWPage", self.getHWPageImage)
        router.add_get("/admin/scannedLPage", self.getLPageImage)
        router.add_get("/admin/unknownPageNames", self.getUnknownPageNames)
        router.add_get("/admin/discardNames", self.getDiscardNames)
        router.add_get("/admin/collidingPageNames", self.getCollidingPageNames)
        router.add_get("/admin/unknownImage", self.getUnknownImage)
        router.add_get("/admin/discardImage", self.getDiscardImage)
        router.add_get("/admin/collidingImage", self.getCollidingImage)
        router.add_get("/admin/questionImages", self.getQuestionImages)
        router.add_get("/admin/testImages", self.getAllTestImages)
        router.add_get("/admin/checkTPage", self.checkTPage)
        router.add_delete("/admin/unknownImage", self.removeUnknownImage)
        router.add_delete("/admin/collidingImage", self.removeCollidingImage)
        router.add_put("/admin/unknownToTestPage", self.unknownToTestPage)
        router.add_put("/admin/unknownToExtraPage", self.unknownToExtraPage)
        router.add_put("/admin/collidingToTestPage", self.collidingToTestPage)
        router.add_put("/admin/discardToUnknown", self.discardToUnknown)
        router.add_put("/admin/hwPagesUploaded", self.processHWUploads)
        router.add_put("/admin/loosePagesUploaded", self.processLUploads)
        router.add_put("/admin/testPagesUploaded", self.processTUploads)
        router.add_put("/admin/populateDB", self.populateExamDatabase)
        router.add_get("/admin/pageVersionMap/{papernum}", self.getPageVersionMap)
        router.add_get("/admin/pageVersionMap", self.getGlobalPageVersionMap)
        router.add_put(
            "/admin/pdf_produced/{papernum}", self.notify_pdf_of_paper_produced
        )
