#!/usr/bin/env python3

# Copyright (C) 2021 Andrew Rechnitzer
# Copyright (C) 2021 Colin B. Macdonald
# SPDX-License-Identifier: AGPL-3.0-or-later

"""Plom tools for pushing solution page image up to server"""
__copyright__ = "Copyright (C) 2021 Andrew Rechnitzer, Colin B. Macdonald et al"
__credits__ = "The Plom Project Developers"
__license__ = "AGPL-3.0-or-later"

import argparse
import os

from plom import __version__


def uploadSolutionImage(server, password, question, version, imageName):
    print(
        "Upload solution image to server for question {} version {}.".format(
            question, version
        )
    )


def getSolutionImage(server, password, question, version):
    from plom.solution import getSolutionImage

    img = getSolutionImage(question, version, server, password)
    if img is not None:
        with open("solution.{}.{}.png", "wb") as fh:
            fh.write(img)


def solutionStatus(server, password):
    from plom.solution import checkSolutionStatus

    checkSolutionStatus.checkStatus(server, password)


def clearLogin(server, password):
    from plom.solutions import clearManagerLogin

    clearManagerLogin.clearLogin(server, password)


parser = argparse.ArgumentParser(
    description=__doc__.split("\n")[0],
    epilog="\n".join(__doc__.split("\n")[1:]),
    formatter_class=argparse.RawDescriptionHelpFormatter,
)
parser.add_argument("--version", action="version", version="%(prog)s " + __version__)
sub = parser.add_subparsers(dest="command")

spU = sub.add_parser(
    "upload",
    help="Upload solution image to scanner",
    description="Upload solution image to scanner.",
)
spG = sub.add_parser(
    "get",
    help="Get solution image to scanner",
    description="Upload solution image to scanner.",
)
spS = sub.add_parser(
    "status",
    help="Get uploaded solution status",
    description="Get list of which question/versions have solution-images uploaded",
)
spC = sub.add_parser(
    "clear",
    help='Clear "manager" login',
    description='Clear "manager" login after a crash or other expected event.',
)

spU.add_argument(
    "q",
    action="store",
    help="The question to upload to",
)
spU.add_argument(
    "v",
    action="store",
    help="The version to upload to",
)
spU.add_argument("image", help="The image of the solution.")

spG.add_argument(
    "q",
    action="store",
    help="The question to get",
)
spG.add_argument(
    "v",
    action="store",
    help="The version to get",
)

for x in (spU, spG, spS, spC):
    x.add_argument("-s", "--server", metavar="SERVER[:PORT]", action="store")
    x.add_argument("-w", "--password", type=str, help='for the "scanner" user')


def main():
    args = parser.parse_args()

    if not hasattr(args, "server") or not args.server:
        try:
            args.server = os.environ["PLOM_SERVER"]
        except KeyError:
            pass
    if not hasattr(args, "password") or not args.password:
        try:
            args.password = os.environ["PLOM_SCAN_PASSWORD"]
        except KeyError:
            pass

    if args.command == "put":
        uploadSolutionImage(args.server, args.password, args.q, args.v, args.image)
    if args.command == "get":
        getSolutionImage(args.server, args.password, args.q, args.v)
    elif args.command == "status":
        solutionStatus(args.server, args.password)
    elif args.command == "clear":
        clearLogin(args.server, args.password)


if __name__ == "__main__":
    main()
