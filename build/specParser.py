import toml
import random


class SpecParser:
    def __init__(self):
        # read the whole spec toml file into a dict
        self.spec = toml.load("verifiedSpec.toml")

    def printSpec(self):
        """Print out the specification provided it is valid"""
        print("Verified test specification:")
        print("\tName of test = ", self.spec["name"])
        print("\tLong name of test = ", self.spec["longName"])
        print("\tNumber of source versions = ", self.spec["sourceVersions"])
        print(
            "\tPublic code (to prevent project collisions) = ", self.spec["publicCode"]
        )
        print("\tPrivate random seed (for randomisation) = ", self.spec["privateSeed"])
        print("\tNumber of tests to produce = ", self.spec["numberToProduce"])
        print(
            "\tNumber of those to be printed with names = ", self.spec["numberToName"]
        )
        print("\tNumber of pages = ", self.spec["totalPages"])
        print("\tIDpages = ", self.spec["idPages"]["pages"])
        print("\tDo not mark pages = ", self.spec["doNotMark"]["pages"])
        print("\tNumber of groups to mark = ", self.spec["numberOfGroups"])
        tot = 0
        for g in range(self.spec["numberOfGroups"]):
            gs = str(g + 1)
            tot += self.spec["group"][gs]["mark"]
            print(
                "\tGroup.{} = pages {} = selected as {} = worth {} marks".format(
                    gs,
                    self.spec["group"][gs]["pages"],
                    self.spec["group"][gs]["select"],
                    self.spec["group"][gs]["mark"],
                )
            )
        print("\tTest total = {} marks".format(tot))


class SpecVerifier:
    def __init__(self):
        # read the whole spec toml file into a dict - it will have single key = "plom" with value being a dict
        self.spec = toml.load("testSpec.toml")

    def verifySpec(self):
        # check that spec contains required attributes
        self.check_keys()
        self.check_name_and_production_numbers()
        lastPage = self.spec["totalPages"]
        self.check_IDPages(lastPage)
        self.check_doNotMark(lastPage)

        print("Checking groups")
        for g in range(self.spec["numberOfGroups"]):
            self.check_group(str(g + 1), lastPage)

        self.check_pages()

    def checkCodes(self):
        # now check and set public and private codes
        if "privateCode" in self.spec:
            print("WARNING - privateSeed is already set. Not replacing this.")
        else:
            print("Assigning a privateSeed to the spec - check")
            self.spec["privateSeed"] = str(random.randrange(0, 10 ** 16)).zfill(16)

        if "publicCode" in self.spec:
            print("WARNING - publicCode is already set. Not replacing this.")
        else:
            print("Assigning a publicCode to the spec - check")
            self.spec["publicCode"] = str(random.randrange(0, 10 ** 6)).zfill(6)

    def saveVerifiedSpec(self):
        print('Saving the verified spec to "verifiedSpec.toml"')
        with open("verifiedSpec.toml", "w+") as fh:
            toml.dump(self.spec, fh)

    # a couple of useful functions
    def isPositiveInt(self, s):
        try:
            n = int(s)
            if n > 0:
                return True
            else:
                return False
        except ValueError:
            return False

    def isContiguousListPosInt(self, l, lastPage):
        # check it is a list
        if type(l) is not list:
            return False
        # check each entry is 0<n<=lastPage
        for n in l:
            if not self.isPositiveInt(n):
                return False
            if n > lastPage:
                return False
        # check it is contiguous
        sl = set(l)
        for n in range(min(sl), max(sl) + 1):
            if n not in sl:
                return False
        # all tests passed
        return True

    # define all the specification checks
    def check_keys(self):
        print("Check specification keys")
        # check it contains required keys
        for x in [
            "name",
            "longName",
            "sourceVersions",
            "totalPages",
            "numberToProduce",
            "numberToName",
            "numberOfGroups",
            "idPages",
            "doNotMark",
        ]:
            if x not in self.spec:
                print('Specification error - must contain "{}" but does not.'.format(x))
                exit(1)
            else:
                print('\tcontains "{}" - check'.format(x))
        # check it contains at least 1 group to mark
        if "1" in self.spec["group"]:
            print('\tcontains at least 1 group (ie "plom.1") - check')
        else:
            print(
                "Specification error - must contain at least 1 group to mark but does not."
            )
            exit(1)

    def check_name_and_production_numbers(self):
        print("Check specification name and numbers")
        # check name is alphanumeric and non-zero length
        print("\tChecking names")
        if self.spec["name"].isalnum() and len(self.spec["name"]) > 0:
            print('\t\tname "{}" has non-zero length - check'.format(self.spec["name"]))
            print(
                '\t\tname "{}" is alphanumeric string - check'.format(self.spec["name"])
            )
        else:
            print(
                "Specification error - Test name must be an alphanumeric string of non-zero length."
            )
            exit(1)

        if (
            all(x.isalnum() or x.isspace() for x in self.spec["longName"])
            and len(self.spec["longName"]) > 0
        ):
            print(
                '\t\tName "{}" has non-zero length - check'.format(
                    self.spec["longName"]
                )
            )
            print(
                '\t\tName "{}" is alphanumeric string - check'.format(
                    self.spec["longName"]
                )
            )
        else:
            print(
                "Specification error - Test longName must be an alphanumeric string of non-zero length."
            )
            exit(1)

        print("\tChecking production numbers")
        # all should be positive integers
        for x in [
            "sourceVersions",
            "totalPages",
            "numberToProduce",
            "numberToName",
            "numberOfGroups",
        ]:
            if self.isPositiveInt(self.spec[x]):
                print(
                    '\t\t"{}" = {} is positive integer - check'.format(x, self.spec[x])
                )
            else:
                print('Specification error - "{}" must be a positive integer.')
                exit(1)
        # have to produce more papers than named papers - preferably with some margin of spares
        if self.spec["numberToProduce"] < self.spec["numberToName"]:
            print(
                "Specification error - You are producing fewer papers {} than you wish to name {}. Produce more papers.".format(
                    self.spec["numberToProduce"], self.spec["numberToName"]
                )
            )
            exit(1)
        else:
            print(
                "\t\tTotal number of papers is larger than number of named papers - check"
            )
            if self.spec["numberToProduce"] < 1.05 * self.spec["numberToName"]:
                print(
                    "WARNING = you are not producing less than 5\% un-named papers. We recommend that you produce more un-named papers"
                )
            else:
                print("\t\tProducing sufficient spare papers - check")

        for k in range(self.spec["numberOfGroups"]):
            if str(k + 1) in self.spec["group"]:
                print(
                    "\t\tFound group {} of {} - check".format(
                        k + 1, self.spec["numberOfGroups"]
                    )
                )
            else:
                print("Specification error - could not find group {} ".format(k + 1))
                exit(1)

    def check_IDPages(self, lastPage):
        print("Checking IDpages")
        if "pages" not in self.spec["idPages"]:
            print('IDpages error - could not find "pages" key')
            exit(1)
        if not self.isContiguousListPosInt(self.spec["idPages"]["pages"], lastPage):
            print(
                'IDpages error - "pages" = {} should be a list of positive integers in range'.format(
                    self.spec["idPages"]["pages"]
                )
            )
            exit(1)
        else:
            print("\t\tIDpages is contiguous list of positive integers - check")
        # check that page 1 is in there.
        if self.spec["idPages"]["pages"][0] != 1:
            print(
                "Warning - page 1 is not part if your ID pages - are you sure you want to do this?"
            )

    def check_doNotMark(self, lastPage):
        print("Checking DoNotMark-pages")
        if "pages" not in self.spec["doNotMark"]:
            print('DoNotMark pages error - could not find "pages" key')
            exit(1)
        if type(self.spec["doNotMark"]["pages"]) is not list:
            print(
                'DoNotMark pages error - "pages" = {} should be a list of positive integers'.format(
                    self.spec["doNotMark"]["pages"]
                )
            )
            exit(1)
        # should be a list of positive integers
        for n in self.spec["doNotMark"]["pages"]:
            if self.isPositiveInt(n) and n < lastPage:
                pass
            else:
                print(
                    'DoNotMark pages error - "pages" = {} should be a list of positive integers in range'.format(
                        self.spec["doNotMark"]["pages"]
                    )
                )
                exit(1)
        print("\t\tDoNotMark pages is list of positive integers - check")

    def check_group(self, g, lastPage):
        print("\tChecking group.{}".format(g))
        # each group has keys
        for x in ["pages", "select", "mark"]:
            if x not in self.spec["group"][g]:
                print("Group error - could not find {} key".format(x))
                exit(1)
        # check pages is contiguous list of positive integers
        if self.isContiguousListPosInt(self.spec["group"][g]["pages"], lastPage):
            print(
                "\t\tpages {} is list of contiguous positive integers - check".format(
                    self.spec["group"][g]["pages"]
                )
            )
        else:
            print(
                "Group error - pages {} is not list of contiguous positive integers".format(
                    self.spec["group"][g]["pages"]
                )
            )
            exit(1)
        # check mark is positive integer
        if self.isPositiveInt(self.spec["group"][g]["mark"]):
            print(
                "\t\tmark {} is positive integer - check".format(
                    self.spec["group"][g]["mark"]
                )
            )
        else:
            print(
                "Group error - mark {} is not a positive integer".format(
                    self.spec["group"][g]["mark"]
                )
            )
            exit(1)
        # check select is "fixed" or "shuffle"
        if self.spec["group"][g]["select"] in ["fixed", "shuffle"]:
            print('\t\tselect is "fixed" or "shuffle" - check')
        else:
            print(
                'Group error - select {} is not "fixed" or "shuffle"'.format(
                    self.spec["group"][g]["select"]
                )
            )
            exit(1)

    def check_pages(self):
        print("Checking all pages used exactly once:")
        pageUse = {k + 1: 0 for k in range(self.spec["totalPages"])}
        for p in self.spec["idPages"]["pages"]:
            pageUse[p] += 1
        for p in self.spec["doNotMark"]["pages"]:
            pageUse[p] += 1
        for g in range(self.spec["numberOfGroups"]):
            for p in self.spec["group"][str(g + 1)]["pages"]:
                pageUse[p] += 1
        for p in range(1, self.spec["totalPages"] + 1):
            if pageUse[p] != 1:
                print("Page Use error - page {} used {} times".format(p, pageUse[p]))
                exit(1)
            else:
                print("\tPage {} used once - check".format(p))
