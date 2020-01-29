from aiohttp import web, MultipartWriter, MultipartReader
import json
import os


class UserInitHandler:
    def __init__(self, plomServer):
        self.server = plomServer

    # @routes.get("/Version")
    async def version(self, request):
        return web.Response(
            text="Running Plom server version {} with API {}".format(
                self.server.Version, self.server.API
            ),
            status=200,
        )

    # @routes.delete("/users/{user}")
    async def closeUser(self, request):
        data = await request.json()
        user = request.match_info["user"]
        if data["user"] != request.match_info["user"]:
            return web.Response(status=400)  # malformed request.
        elif self.server.validate(data["user"], data["token"]):
            self.server.closeUser(data["user"])
            return web.Response(status=200)
        else:
            return web.Response(status=401)

    # @routes.delete("/authorisation")
    async def clearAuthorisation(self, request):
        data = await request.json()
        # manager to auth with their token - unless trying to clear self.
        if data["user"] == "manager" and data["userToClear"] != "manager":
            if self.server.validate(data["user"], data["token"]):
                self.server.closeUser(data["userToClear"])
                print("Manager force-logout user {}".format(data["userToClear"]))
                return web.Response(status=200)
        else:  # everyone else has to check their pwd
            if self.server.authority.checkPassword(data["user"], data["password"]):
                print("User {} force-logout self".format(data["user"]))
                self.server.closeUser(data["user"])
                return web.Response(status=200)
        return web.Response(status=401)

    # @routes.put("/users/{user}")
    async def giveUserToken(self, request):
        data = await request.json()
        user = request.match_info["user"]

        rmsg = self.server.giveUserToken(data["user"], data["pw"], data["api"])
        if rmsg[0]:
            return web.json_response(rmsg[1], status=200)  # all good, return the token
        elif rmsg[1].startswith("API"):
            return web.json_response(
                rmsg[1], status=400
            )  # api error - return the error message
        elif rmsg[1].startswith("UHT"):
            return web.json_response(rmsg[1], status=409)  # user has token already.
        else:
            return web.Response(status=401)  # you are not authorised

    # @routes.put("/admin/reloadUsers")
    async def adminReloadUsers(self, request):
        data = await request.json()

        rmsg = self.server.reloadUsers(data["pw"])
        # returns either True (success) or False (auth-error)
        if rmsg:
            return web.json_response(status=200)  # all good
        else:
            return web.Response(status=401)  # you are not authorised

    async def InfoGeneral(self, request):
        rmsg = self.server.InfoGeneral()
        if rmsg[0]:
            return web.json_response(rmsg[1:], status=200)
        else:  # this should not happen
            return web.Response(status=404)

    # @routes.get("/info/shortName")
    async def InfoShortName(self, request):
        rmsg = self.server.InfoShortName()
        if rmsg[0]:
            return web.Response(text=rmsg[1], status=200)
        else:  # this should not happen
            return web.Response(status=404)

    def setUpRoutes(self, router):
        router.add_get("/Version", self.version)
        router.add_delete("/users/{user}", self.closeUser)
        router.add_put("/users/{user}", self.giveUserToken)
        router.add_put("/admin/reloadUsers", self.adminReloadUsers)
        router.add_get("/info/shortName", self.InfoShortName)
        router.add_get("/info/general", self.InfoGeneral)
        router.add_delete("/authorisation", self.clearAuthorisation)
