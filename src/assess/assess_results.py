import random

import numpy as np


def coverage_metric(obtained, expected):
    max_value = 0
    for t in obtained:
        max_value = t[1] if t[1] > max_value else max_value
    for t in expected:
        max_value = t[1] if t[1] > max_value else max_value
    max_value = int(max_value)

    obtained_pixels = np.zeros(shape=(max_value + 1, max_value + 1), dtype=int)
    expected_pixels = np.zeros(shape=(max_value + 1, max_value + 1), dtype=int)
    for t in obtained:
        for a in range(int(t[0]), int(t[1])):
            for b in range(a + 1, int(t[1] + 1)):
                obtained_pixels[a, b] = 1

    for t in expected:
        for a in range(int(t[0]), int(t[1])):
            for b in range(a + 1, int(t[1]) + 1):
                expected_pixels[a, b] = 1

    expected_count = np.count_nonzero(expected_pixels)
    obtained_count = np.count_nonzero(obtained_pixels)
    expected_pixels -= obtained_pixels
    not_shared_pixels = np.count_nonzero(expected_pixels)
    common_pixels = (expected_count + obtained_count - not_shared_pixels) // 2
    all_pixels = common_pixels + not_shared_pixels
    return (common_pixels + 0.0) / all_pixels if all_pixels > 0 else 0


def matching_metric(data_to_assess, reference_data):
    best_matches = []
    for found_tad in data_to_assess:
        found_tad_length = found_tad[1] - found_tad[0]
        matches = [0]
        for reference_tad in reference_data:
            reference_tad_length = reference_tad[1] - reference_tad[0]
            if reference_tad[0] <= found_tad[0] <= found_tad[1] <= reference_tad[1]:
                # found_tad is contained in reference_tad
                matches.append(100)
            elif found_tad[0] <= reference_tad[0] <= reference_tad[1] <= found_tad[1]:
                # found_tad covers whole reference_tad
                matches.append(reference_tad_length / found_tad_length * 100)
            elif found_tad[0] <= reference_tad[0] <= found_tad[1] <= reference_tad[1]:
                # found_tad is moved to the left if it goes to reference_tad
                matches.append((found_tad[1] - reference_tad[0]) / found_tad_length * 100)
            elif reference_tad[0] <= found_tad[0] <= reference_tad[1] <= found_tad[1]:
                # found_tad is moved to the right if it goes to reference_tad
                matches.append((reference_tad[1] - found_tad[0]) / found_tad_length * 100)
        best_matches.append(max(matches))
    return best_matches


if __name__ == '__main__':
    results = [(0, 5)]
    reference = [(0, 12)]
    while results[-1][1] != 1000:
        rand = random.randint(2, 15)
        results.append((results[-1][1], results[-1][1] + rand if results[-1][1] + rand < 1000 else 1000))
    while reference[-1][1] != 1000:
        rand = random.randint(2, 15)
        reference.append((reference[-1][1], reference[-1][1] + rand if reference[-1][1] + rand < 1000 else 1000))

    print(results)
    print(reference)
    evaluated_tads = matching_metric(results, reference)
    print(evaluated_tads)
    print('Matching metric - {}%'.format(
        sum(evaluated_tads) / len(evaluated_tads)))
