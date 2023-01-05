#!/usr/bin/env python3

# SPDX-License-Identifier: AGPL-3.0-or-later
# Copyright (C) 2023 Andrew Rechnitzer

"""Simple script to build a list of random first/last names starting with 'Ex'.

Also constructs random 8 digit student numbers which do not clash with those in the existing demoClassList.csv file.

Re-generation of data requires the names_dataset which is (essentially) a big dump of names from facebook, and also the alphabet-detector module
"""


import csv
import json
from pathlib import Path
import random

# some simple translations of extra into other languages courtesy of google-translate
# and https://www.indifferentlanguages.com/words/extra
extra_last_names = [
    "Extra",
    "Ekstra",
    "Supplémentaire",
    "Aukalega",
    "Aparteko",
    "Ychwanegol",
    "A-bharrachd",
    "Breise",
    "Papildomai",
    "Dodatkowy",
    "Okwengeziwe",
    "Tlaleletšo",
    "Ziada",
    "Ylimääräinen",
]


# some common M/F first names taken from the names_dataset - generated using the code below
# from names_dataset import NameDataset
# from alphabet_detector import AlphabetDetector
# ad = AlphabetDetector()
# extra_first_names = []
# nameset = NameDataset()
# # get 10 most common names from each country in database - but only Latin-script (sorry)
# for loc, name_data in nameset.get_top_names(20).items():
#     # name_data = {'M': list, 'F': list}
#     rc = random.choice(name_data["M"])
#     if ad.only_alphabet_chars(rc, "LATIN"):
#         extra_first_names.append(rc)
#     rc = random.choice(name_data["F"])
#     if ad.only_alphabet_chars(rc, "LATIN"):
#         extra_first_names.append(rc)
# print(sorted(list(set(extra_first_names))))


extra_first_names = [
    "Abdiel",
    "Adel",
    "Adi",
    "Adissa",
    "Adriana",
    "Agron",
    "Agus",
    "Akmal",
    "Alaa",
    "Alan",
    "Alejandra",
    "Alejandro",
    "Aleksandr",
    "Alemtsehay",
    "Ali",
    "Allen",
    "Amira",
    "Amr",
    "Anabela",
    "Andrey",
    "Anila",
    "Ariel",
    "Aya",
    "Aysel",
    "Ayu",
    "Ayşe",
    "Björn",
    "Carine",
    "Carla",
    "Carlos",
    "Chang",
    "Cheng",
    "Chiara",
    "Choukri",
    "Claudio",
    "Claus",
    "Cristhian",
    "Devon",
    "Dimitra",
    "Elizabeth",
    "Fathmath",
    "Fatma",
    "Fernando",
    "Fiona",
    "Francis",
    "Frida",
    "Fábio",
    "Gelson",
    "Genesis",
    "Hanane",
    "Hawra",
    "Hernández",
    "Hiba",
    "Hilma",
    "Hüseyin",
    "Ifrah",
    "Ildikó",
    "Indah",
    "Inês",
    "Ivan",
    "Ivelina",
    "Javier",
    "Jemal",
    "Jenni",
    "Jesmond",
    "Jie",
    "Joana",
    "Joao",
    "Johan",
    "Jonas",
    "Josipa",
    "Juan",
    "Karel",
    "Kari",
    "Karin",
    "Katherine",
    "Khaled",
    "Kim",
    "Kitty",
    "Lavenia",
    "Laxmi",
    "Lebo",
    "Lebogang",
    "Lela",
    "Li",
    "Liline",
    "Linda",
    "Ling",
    "Luis",
    "Luka",
    "Maha",
    "Mahamadi",
    "Marcelina",
    "Marco",
    "Maria",
    "Markus",
    "Martha",
    "Marthese",
    "Marvín",
    "Mary",
    "Mary Grace",
    "María",
    "Masud",
    "Maxine",
    "Maya",
    "Małgorzata",
    "Mehdi",
    "Mekan",
    "Michalis",
    "Michel",
    "Miguel",
    "Mikael",
    "Milan",
    "Mohamed",
    "Mohammed",
    "Monika",
    "Monique",
    "Mouna",
    "Muhamad",
    "Muhammad",
    "Muhammed",
    "Munezero",
    "Nana",
    "Nargiza",
    "Neha",
    "Nicole",
    "Nikolay",
    "Nikos",
    "Nilsa",
    "Nishantha",
    "Niyonkuru",
    "Noel",
    "Noor",
    "Noriko",
    "Nur",
    "Or",
    "Peter",
    "Petra",
    "Philippe",
    "Rafał",
    "Raja",
    "Rajesh",
    "Ravi",
    "Renel",
    "Ricardo",
    "Richard",
    "Rodrigo",
    "Ryo",
    "Said",
    "Sam",
    "Sami",
    "Sanjida",
    "Sarah",
    "Shaik",
    "Sigríður",
    "Silvia",
    "Simona",
    "Siyabonga",
    "Snezana",
    "Solange",
    "Sophie",
    "Sri",
    "Steve",
    "Tamás",
    "Tanja",
    "Temo",
    "Thabang",
    "Thomas",
    "Trond",
    "Tural",
    "Valentina",
    "Valeria",
    "Vasile",
    "Victor",
    "Waisea",
    "Willem",
    "Yiota",
    "Yolani",
    "Yosiris",
    "Yves",
    "Zainab",
    "Zoila",
    "Špela",
]


sid = {}
dcl = Path("../plom/demoClassList.csv")
with open(dcl) as fh:
    red = csv.DictReader(fh)
    for row in red:
        sid[int(row["id"])] = row["name"]


N = 100
id_and_name = []
for (a, b) in zip(
    random.choices(extra_first_names, k=N), random.choices(extra_last_names, k=N)
):
    while True:
        id = random.randint(10**7, 10**8)
        if id not in sid:
            break
    id_and_name.append((f"{id}", f"{b}, {a}"))

print(json.dumps(id_and_name))
