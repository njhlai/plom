#!/usr/bin/env python3

# SPDX-License-Identifier: AGPL-3.0-or-later
# Copyright (C) 2021 Andrew Rechnitzer
# Copyright (C) 2021 Nicholas JH Lai

"""
Separate qr_coded pages from blank pages.

This script is helpful if you accidentally printed the exam
single-sdied. This script will separate blank pages from
qr-coded pages, which should be checked by someone after.

Provided as is, WITH all faults.
Please be sure you understand what's happening here before using it!
"""

import fitz
from pyzbar.pyzbar import decode, ZBarSymbol
from pathlib import Path
from PIL import Image
import sys
import tempfile

from plom.scan.scansToImages import processFileToBitmaps

if len(sys.argv) != 2:
    print("Requires a single pdf as argument.")
    quit()

input_file = Path(sys.argv[1])

qrd_pages = []
blank_pages = []
problematic_qrd_pages = []

qrd_file = input_file.parent / (input_file.stem + "_qrcoded.pdf")
blanks_file = input_file.parent / (input_file.stem + "_blanks.pdf")

with tempfile.TemporaryDirectory() as td:
    file_list = processFileToBitmaps(input_file, td, do_not_extract=True)
    for X in file_list:
        stem = X.name[:-4]  # name without the ".png"
        pn = int(stem.split("-")[-1])  # blah-XX.png - get the XX
        image = Image.open(X)
        qrlist = decode(image, symbols=[ZBarSymbol.QRCODE])
        if len(qrlist) > 0:
            print(f"# + Page {pn} has {len(qrlist)} codes")
            if len(qrlist) < 3:
                print(f"WARNING: page {pn} has only {len(qrlist)} codes, expected 3")
                problematic_qrd_pages.append(pn)
            qrd_pages.append(pn)
        else:
            print(f"# - Page {pn} is blank")
            blank_pages.append(pn)

inp = fitz.open(input_file)

if inp.page_count != len(qrd_pages) + len(blank_pages):
    print("There is a problem with total number of pages.")
    print(f"Original pdf has {inp.page_count}")
    print(
        f"But found {len(qrd_pages)} qr-coded pages and {len(blank_pages)} pages - ie {len(qrd_pages) + len(blank_pages)} pages."
    )
    print("EEK! stopping.")
    quit()


print(f"Saving qr-coded pages {qrd_pages} to {qrd_file}")
qr_out = fitz.open()
for pn in qrd_pages:
    n = pn - 1  # fitz starts from 0 not 1
    qr_out.insert_pdf(inp, from_page=n, to_page=n, start_at=-1)
qr_out.save(qrd_file)
qr_out.close()

print(f"Saving blank pages {blank_pages} to {blanks_file}")
blank_out = fitz.open()
for pn in blank_pages:
    n = pn - 1  # fitz starts from 0 not 1
    blank_out.insert_pdf(inp, from_page=n, to_page=n, start_at=-1)
blank_out.save(blanks_file)
blank_out.close()

unexpected_qrd_pages = list(filter(lambda x: (x - 1) % 2, qrd_pages))
unexpected_blank_pages = list(filter(lambda x: x % 2, blank_pages))

print(f"The original file had {inp.page_count} pages")
print(
    f"We found a total of {len(qrd_pages)} pages with qr-codes. This should be a multiple of the number of pages in your test."
)
print(
    f"All pages with qr-codes are now in {qrd_file} - these can be processed as usual."
)

print(
    f"A total of {len(problematic_qrd_pages)} possibly problematic pages with qr-codes: {problematic_qrd_pages}"
)

print(f"We found a total of {len(blank_pages)} pages without qr-codes.")
print(f"Pages without qr-codes are in {blanks_file} - these must be examined by hand.")

print(f"Unexpected qrd pages: {unexpected_qrd_pages}")
print(f"Unexpected blank pages: {unexpected_blank_pages}")

print(
    f"Please note down any pages of interest from {blanks_file} and extract those using **next script**"
)

inp.close()
