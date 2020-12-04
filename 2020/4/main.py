from typing import List, NamedTuple
import re

HAIR_REGEX = re.compile("^#[0-9a-f]{6}$")
EYE_COLORS = {"amb", "blu", "brn", "gry", "grn", "hzl", "oth"}
PASSPORT_ID_REGEX = re.compile("^[0-9]{9}$")

assert(HAIR_REGEX.match("#fffff") is None)
assert(HAIR_REGEX.match("#fffffff") is None)

def validate_year(value, low, high):
    return len(value) == 4 and \
       low <= int(value) <= high

class Passport(NamedTuple):
    byr: str = None
    iyr: str = None
    eyr: str = None
    hgt: str = None
    hcl: str = None
    ecl: str = None
    pid: str = None
    cid: str = None

    @staticmethod
    def parse(lines) -> "Passport":
        args = dict()
        for line in lines:
            for pair in line.split():
                key, value = pair.split(":")
                args[key] = value
        return Passport(**args)

    def is_valid(self):
        return self.byr is not None and \
            self.iyr is not None and \
            self.eyr is not None and \
            self.hgt is not None and \
            self.hcl is not None and \
            self.ecl is not None and \
            self.pid is not None

    def is_valid_strict(self):
        return self.is_valid() and \
            validate_year(self.byr, 1920, 2002) and \
            validate_year(self.iyr, 2010, 2020) and \
            validate_year(self.eyr, 2020, 2030) and \
            self.is_valid_height_strict() and \
            self.is_valid_hair_color_strict() and \
            self.is_valid_eye_color_strict() and \
            self.is_valid_pid_strict()

    def is_valid_height_strict(self):
        if len(self.hgt) < 2:
            return False

        units = self.hgt[-2:]
        height = int(self.hgt[:-2])
        if units == "cm":
            return 150 <= height <= 193
        if units == "in":
            return 59 <= height <= 76
        return False

    def is_valid_hair_color_strict(self):
        return HAIR_REGEX.match(self.hcl)

    def is_valid_eye_color_strict(self):
        return self.ecl in EYE_COLORS

    def is_valid_pid_strict(self):
        return PASSPORT_ID_REGEX.match(self.pid)

assert(not Passport().is_valid())
assert(Passport.parse(["pid:087499704 hgt:74in ecl:grn iyr:2012 eyr:2030 byr:1980 hcl:#623a2f"]).is_valid_strict())
assert(not Passport.parse(["eyr:1972 cid:100 hcl:#18171d ecl:amb hgt:170 pid:186cm iyr:2018 byr:1926"]).is_valid_strict())
assert(not Passport.parse(["iyr:2019 hcl:#602927 eyr:1967 hgt:170cm ecl:grn pid:012533040 byr:1946"]).is_valid_strict())
assert(not Passport.parse(["hcl:dab227 iyr:2012 ecl:brn hgt:182cm pid:021572410 eyr:2020 byr:1992 cid:277"]).is_valid_strict())
assert(not Passport.parse(["hgt:59cm ecl:zzz eyr:2038 hcl:74454a iyr:2023 pid:3556412378 byr:2007"]).is_valid_strict())


def split_lines_into_passports(lines):
    result = []
    current_passport = []
    for line in lines:
        if not line:
            result.append(current_passport)
            current_passport = []
        else:
            current_passport.append(line)
    if current_passport:
        result.append(current_passport)
    return result

TEST_LINES1 = [
    "ecl:gry pid:860033327 eyr:2020 hcl:#fffffd",
    "byr:1937 iyr:2017 cid:147 hgt:183cm",
    "",
    "iyr:2013 ecl:amb cid:350 eyr:2023 pid:028048884",
    "hcl:#cfa07d byr:1929"
]
EXPECTED_LINES1 = [
    [
        "ecl:gry pid:860033327 eyr:2020 hcl:#fffffd",
        "byr:1937 iyr:2017 cid:147 hgt:183cm"
    ],
    [
        "iyr:2013 ecl:amb cid:350 eyr:2023 pid:028048884",
        "hcl:#cfa07d byr:1929"
    ]
]
TEST_LINES2 = TEST_LINES1 + [""]


assert(split_lines_into_passports(TEST_LINES1) == EXPECTED_LINES1)
assert(split_lines_into_passports(TEST_LINES2) == EXPECTED_LINES1)

def validate_passports(lines):
    result = 0
    result_strict = 0
    for line_group in split_lines_into_passports(lines):
        passport = Passport.parse(line_group)
        if passport.is_valid():
            result += 1
        if passport.is_valid_strict():
            result_strict += 1
    return result, result_strict
    

def main():
    with open('in.txt') as infile:
        lines = [line.strip() for line in infile.readlines()]
        print(validate_passports(lines))


if __name__ == "__main__":
    main()
