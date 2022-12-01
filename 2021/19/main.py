from typing import List, NamedTuple, Set


def aex(want, got, prefix=""):
    if got != want:
        print(f"{prefix}got {got}, expected {want}")


def assrt(want, f, *args, **kwargs):
    got = f(*args, **kwargs)
    if got != want:
        aex(want, got, prefix=f"{f.__qualname__}: ")


def read_input():
    with open("in.txt") as infile:
        lines = [line.strip() for line in infile.readlines()]
        return parse_input(lines)


def parse_input(lines):
    result = []
    i = 0
    while i < len(lines):
        i += 1
        beacons = []
        while i < len(lines) and lines[i]:
            beacons.append(tuple(int(x) for x in lines[i].split(",")))
            i += 1
        i += 1
        result.append(beacons)
    return result


TRANSFORMATIONS = [
    # Main diagonal.
    [
        [1, 0, 0],
        [0, 1, 0],
        [0, 0, 1],
    ],
    [
        [-1, 0, 0],
        [0, -1, 0],
        [0, 0, 1],
    ],
    [
        [1, 0, 0],
        [0, -1, 0],
        [0, 0, -1],
    ],
    [
        [-1, 0, 0],
        [0, 1, 0],
        [0, 0, -1],
    ],
    # 1
    [
        [1, 0, 0],
        [0, 0, -1],
        [0, 1, 0],
    ],
    [
        [-1, 0, 0],
        [0, 0, 1],
        [0, 1, 0],
    ],
    [
        [1, 0, 0],
        [0, 0, 1],
        [0, -1, 0],
    ],
    [
        [-1, 0, 0],
        [0, 0, -1],
        [0, -1, 0],
    ],
    # 2
    [
        [0, -1, 0],
        [-1, 0, 0],
        [0, 0, -1],
    ],
    [
        [0, 1, 0],
        [1, 0, 0],
        [0, 0, -1],
    ],
    [
        [0, 1, 0],
        [-1, 0, 0],
        [0, 0, 1],
    ],
    [
        [0, -1, 0],
        [1, 0, 0],
        [0, 0, 1],
    ],
    # 3
    [
        [0, 1, 0],
        [0, 0, 1],
        [1, 0, 0],
    ],
    [
        [0, -1, 0],
        [0, 0, -1],
        [1, 0, 0],
    ],
    [
        [0, 1, 0],
        [0, 0, -1],
        [-1, 0, 0],
    ],
    [
        [0, -1, 0],
        [0, 0, 1],
        [-1, 0, 0],
    ],
    # 4
    [
        [0, 0, 1],
        [1, 0, 0],
        [0, 1, 0],
    ],
    [
        [0, 0, -1],
        [1, 0, 0],
        [0, -1, 0],
    ],
    [
        [0, 0, 1],
        [-1, 0, 0],
        [0, -1, 0],
    ],
    [
        [0, 0, -1],
        [-1, 0, 0],
        [0, 1, 0],
    ],
    # Secondary diagonal
    [
        [0, 0, -1],
        [0, 1, 0],
        [1, 0, 0],
    ],
    [
        [0, 0, 1],
        [0, -1, 0],
        [1, 0, 0],
    ],
    [
        [0, 0, 1],
        [0, 1, 0],
        [-1, 0, 0],
    ],
    [
        [0, 0, -1],
        [0, -1, 0],
        [-1, 0, 0],
    ],
]

assert len(TRANSFORMATIONS) == 24


def transform(vec, transformation):
    return tuple(sum(x * v for x, v in zip(row, vec)) for row in transformation)


TEST_VEC = (1, 2, 3)
assert transform(TEST_VEC, TRANSFORMATIONS[0]) == TEST_VEC
assert transform(TEST_VEC, TRANSFORMATIONS[1]) == (-1, -2, 3)
assert transform(TEST_VEC, TRANSFORMATIONS[-1]) == (-3, -2, -1)


def produce_orientations(beacons):
    result = [
        [transform(beacon, transformation) for beacon in beacons]
        for transformation in TRANSFORMATIONS
    ]
    assert len(result) == 24
    return result


def transfer_points(points, start, end):
    return {
        tuple(p + end[i] - start[i] for i, p in enumerate(point)) for point in points
    }


ORIENTATION_TEST_INPUT = parse_input(
    [
        line.strip()
        for line in """--- scanner 0 ---
-1,-1,1
-2,-2,2
-3,-3,3
-2,-3,1
5,6,-4
8,0,7

--- scanner 0 ---
1,-1,1
2,-2,2
3,-3,3
2,-1,3
-5,4,-6
-8,-7,0

--- scanner 0 ---
-1,-1,-1
-2,-2,-2
-3,-3,-3
-1,-3,-2
4,6,5
-7,0,8

--- scanner 0 ---
1,1,-1
2,2,-2
3,3,-3
1,3,-2
-4,-6,5
7,0,8

--- scanner 0 ---
1,1,1
2,2,2
3,3,3
3,1,2
-6,-4,-5
0,7,-8""".split(
            "\n"
        )
    ]
)


def orientations_test():
    orientations = {tuple(o) for o in produce_orientations(ORIENTATION_TEST_INPUT[0])}
    assert {tuple(o) for o in ORIENTATION_TEST_INPUT}.issubset(orientations)


orientations_test()

MIN_INTERSECTION = 12


class FoundScanner(NamedTuple):
    position: tuple
    beacons: Set[tuple]


def find_scanners(data) -> List[FoundScanner]:
    known_scanners = [FoundScanner(position=(0, 0, 0), beacons=set(data[0]))]
    known_scanners_idxs = {0}
    updated_known = True
    while updated_known:
        print(f"{len(known_scanners_idxs)}/{len(data)} known")
        updated_known = False
        for i, scanner in enumerate(data):
            if i in known_scanners_idxs:
                continue
            found = False
            for known_scanner in known_scanners:
                if found:
                    break
                for orientation in produce_orientations(scanner):
                    if found:
                        break
                    for known_point in known_scanner.beacons:
                        if found:
                            break
                        for point in orientation:
                            # Assume that point and known_point are the same point between a known scanner and an orientation of an unknown one,
                            # check if there at least 12 common points in total.
                            transferred = transfer_points(
                                orientation, point, known_point
                            )
                            if (
                                len(known_scanner.beacons.intersection(transferred))
                                >= MIN_INTERSECTION
                            ):
                                new_scanner = FoundScanner(
                                    position=tuple(
                                        x1 - x2 for x1, x2 in zip(known_point, point)
                                    ),
                                    beacons=transferred,
                                )
                                known_scanners.append(new_scanner)
                                known_scanners_idxs.add(i)
                                found = True
                                updated_known = True
                                break

    aex(len(data), len(known_scanners))
    return known_scanners


def solve1_with_scanners(scanners: List[FoundScanner]) -> int:
    result = set()
    for scanner in scanners:
        result = result | scanner.beacons
    return len(result)


TEST_INPUT = parse_input(
    [
        line.strip()
        for line in """--- scanner 0 ---
404,-588,-901
528,-643,409
-838,591,734
390,-675,-793
-537,-823,-458
-485,-357,347
-345,-311,381
-661,-816,-575
-876,649,763
-618,-824,-621
553,345,-567
474,580,667
-447,-329,318
-584,868,-557
544,-627,-890
564,392,-477
455,729,728
-892,524,684
-689,845,-530
423,-701,434
7,-33,-71
630,319,-379
443,580,662
-789,900,-551
459,-707,401

--- scanner 1 ---
686,422,578
605,423,415
515,917,-361
-336,658,858
95,138,22
-476,619,847
-340,-569,-846
567,-361,727
-460,603,-452
669,-402,600
729,430,532
-500,-761,534
-322,571,750
-466,-666,-811
-429,-592,574
-355,545,-477
703,-491,-529
-328,-685,520
413,935,-424
-391,539,-444
586,-435,557
-364,-763,-893
807,-499,-711
755,-354,-619
553,889,-390

--- scanner 2 ---
649,640,665
682,-795,504
-784,533,-524
-644,584,-595
-588,-843,648
-30,6,44
-674,560,763
500,723,-460
609,671,-379
-555,-800,653
-675,-892,-343
697,-426,-610
578,704,681
493,664,-388
-671,-858,530
-667,343,800
571,-461,-707
-138,-166,112
-889,563,-600
646,-828,498
640,759,510
-630,509,768
-681,-892,-333
673,-379,-804
-742,-814,-386
577,-820,562

--- scanner 3 ---
-589,542,597
605,-692,669
-500,565,-823
-660,373,557
-458,-679,-417
-488,449,543
-626,468,-788
338,-750,-386
528,-832,-391
562,-778,733
-938,-730,414
543,643,-506
-524,371,-870
407,773,750
-104,29,83
378,-903,-323
-778,-728,485
426,699,580
-438,-605,-362
-469,-447,-387
509,732,623
647,635,-688
-868,-804,481
614,-800,639
595,780,-596

--- scanner 4 ---
727,592,562
-293,-554,779
441,611,-461
-714,465,-776
-743,427,-804
-660,-479,-426
832,-632,460
927,-485,-438
408,393,-506
466,436,-512
110,16,151
-258,-428,682
-393,719,612
-211,-452,876
808,-476,-593
-575,615,604
-485,667,467
-680,325,-822
-627,-443,-432
872,-547,-609
833,512,582
807,604,487
839,-516,451
891,-625,532
-652,-548,-490
30,-46,-14
""".split(
            "\n"
        )
    ]
)

assert TEST_INPUT[0][0] == (404, -588, -901)
assert TEST_INPUT[0][-1] == (459, -707, 401)
assert TEST_INPUT[1][0] == (686, 422, 578)

assert produce_orientations(TEST_INPUT[1])[0] == TEST_INPUT[1]


TEST_FOUND_SCANNERS = find_scanners(TEST_INPUT)
assrt(79, solve1_with_scanners, TEST_FOUND_SCANNERS)


def manhattan(a, b):
    return sum(abs(x1 - x2) for x1, x2 in zip(a, b))


def solve2_with_scanners(scanners: List[FoundScanner]) -> int:
    result = 0
    for i, a in enumerate(scanners):
        for j in range(i + 1, len(scanners)):
            result = max(result, manhattan(a.position, scanners[j].position))
    return result


assrt(3621, solve2_with_scanners, TEST_FOUND_SCANNERS)


def main():
    data = read_input()
    scanners = find_scanners(data)
    print(solve1_with_scanners(scanners))
    print(solve2_with_scanners(scanners))


if __name__ == "__main__":
    main()
