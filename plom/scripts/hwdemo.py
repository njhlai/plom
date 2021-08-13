#!/usr/bin/env python3

# SPDX-License-Identifier: AGPL-3.0-or-later
# Copyright (C) 2020 Andrew Rechnitzer
# Copyright (C) 2020-2021 Colin B. Macdonald
# Copyright (C) 2020 Victoria Schuster

"""Plom script to start a demo server for homework submissions.

Instructions:
  * Run this script
  * In a new terminal, run the Plom Client and connect to localhost.
"""

__copyright__ = "Copyright (C) 2020-2021 Andrew Rechnitzer, Colin B. Macdonald et al"
__credits__ = "The Plom Project Developers"
__license__ = "AGPL-3.0-or-later"

import argparse
import os
from pathlib import Path
from shlex import split
import subprocess
import tempfile
from warnings import warn

from plom import __version__
from plom import Default_Port
from plom.server import PlomServer


parser = argparse.ArgumentParser(
    description=__doc__,
    formatter_class=argparse.RawDescriptionHelpFormatter,
)
parser.add_argument("--version", action="version", version="%(prog)s " + __version__)
parser.add_argument(
    "server_dir",
    nargs="?",
    help="""The directory containing the filespace to be used by this server.
        It will be created if it does not exist.
        You can specify "." to use the current directory.
        If omitted, a uniquely-named directory will be used.
    """,
)
parser.add_argument(
    "--port",
    type=int,
    help=f"Which port to use for the demo server ({Default_Port} if omitted)",
)


def main():
    args = parser.parse_args()
    print("Plom version {}".format(__version__))

    if not args.server_dir:
        args.server_dir = Path(tempfile.mkdtemp(prefix="Plom_Demo_", dir=Path.cwd()))
    args.server_dir = Path(args.server_dir)
    print(f'Using directory "{args.server_dir}" for the demo')
    if not args.server_dir.exists():
        print(f'Creating directory "{args.server_dir}"')

    is_empty = not any(args.server_dir.iterdir())
    if not is_empty:
        warn(f"Target directory {args.server_dir} is not empty")
    for f in (
        "specAndDatabase",
        "serverConfiguration",
        "archivedPDFs",
        "pageImages",
        "scanPNGs",
        "pages",
    ):
        if (args.server_dir / f).exists():
            raise RuntimeError(
                f'Directory "{args.server_dir/f}" must not exist for this demo'
            )

    prev = Path.cwd()
    try:
        os.chdir(args.server_dir)
        if args.port:
            subprocess.check_call(split(f"plom-server init --port {args.port}"))
        else:
            subprocess.check_call(split("plom-server init"))
        subprocess.check_call(split("plom-server users --demo"))
        subprocess.check_call(split("plom-build new --demo"))
    finally:
        os.chdir(prev)

    background_server = PlomServer(basedir=args.server_dir)

    assert background_server.process_is_running(), "has the server died?"
    assert background_server.ping_server(), "cannot ping server, something gone wrong?"
    print("Server seems to be running, so we move on to uploading")

    if args.port:
        server = f"localhost:{args.port}"
    else:
        server = "localhost"
    subprocess.check_call(split(f"plom-build class --demo -w 1234 -s {server}"))
    subprocess.check_call(split(f"plom-build rubric --demo -w 1234 -s {server}"))
    prev = Path.cwd()
    try:
        os.chdir(args.server_dir)
        subprocess.check_call(split(f"plom-build make -w 1234 -s {server}"))
    finally:
        os.chdir(prev)

    print("Uploading fake scanned data to the server")
    try:
        os.chdir(args.server_dir)
        # this creates two batches of fake hw - prefixes = hwA and hwB
        subprocess.check_call(split(f"plom-fake-hwscribbles -w 1234 -s {server}"))

        print("Processing some individually")
        # TODO: this is fragile, should not hardcode these student numbers!
        subprocess.check_call(
            split(
                f"plom-hwscan process submittedHWByQ/semiloose.11015491._.pdf 11015491 -q 1,2,3 -w 4567 -s {server}"
            )
        )
        subprocess.check_call(
            split(
                f"plom-hwscan process submittedHWByQ/semiloose.11135153._.pdf 11135153 -q 1,2,3 -w 4567 -s {server}"
            )
        )

        print("Processing all hw by question submissions.")
        subprocess.check_call(split(f"plom-hwscan allbyq -w 4567 -y -s {server}"))
        print("Replacing all missing questions.")
        subprocess.check_call(split(f"plom-hwscan missing -w 4567 -y -s {server}"))
        # print(">> TODO << process loose pages")
    finally:
        os.chdir(prev)

    assert background_server.process_is_running(), "has the server died?"
    assert background_server.ping_server(), "cannot ping server, something gone wrong?"
    print("Server seems to still be running: demo setup is complete")

    print('\n*** Now run "plom-client" ***\n')
    print(f"  * Server currently running under PID {background_server.pid}\n")
    # TODO: output account info directly, perhaps just "user*"?
    print('  * See "userListRaw.csv" for account info\n')
    # print("  * Press Ctrl-C to stop this demo")
    # background_server.wait()
    input("Press enter when you want to stop the server...")
    background_server.stop()
    print("Server stopped, goodbye!")


if __name__ == "__main__":
    main()
