import assess.assess_results as ar
import plots.plots as p


def evaluate_results(algorithm_results, mtx, expected_results, show=True,
                     metrics_filepath=None,
                     images_filepath=None,
                     expected_filepath=None,
                     found_filepath=None,
                     R=100000):
    algorithm_tads_amount = len(algorithm_results)
    expected_tad_count = len(expected_results)
    algorithm_tads_mean_length = sum([i[1] - i[0] for i in algorithm_results]) / len(algorithm_results)
    expected_tads_mean_length = sum([i[1] - i[0] for i in expected_results]) / len(expected_results)
    matching_metric_results = ar.matching_metric(algorithm_results, expected_results)
    coverage_metric_result = ar.coverage_metric(algorithm_results, expected_results)
    print(f"Expected TADs count: {expected_tad_count}, found TADs count: {algorithm_tads_amount}")
    print(
        f"Expected TADs mean length: {expected_tads_mean_length}, found TADs mean length: {algorithm_tads_mean_length}")
    print(f"Matching metric: {sum(matching_metric_results) / len(matching_metric_results)}%")
    print(f"Coverage metric: {coverage_metric_result * 100}%")

    if show:
        p.show_correct_and_obtained_results(mtx, expected_results, algorithm_results)
    if metrics_filepath is not None:
        with open(metrics_filepath, 'w') as out:
            out.truncate()
            out.write(f"# : FOUND({algorithm_tads_amount}), EXPECTED({expected_tad_count})" + '\n')
            out.write(f"mean : FOUND({algorithm_tads_mean_length}), EXPECTED({expected_tads_mean_length})" + '\n')
            out.write(f"coverage : {coverage_metric_result * 100}%" + '\n')
            out.write(f"matching : {sum(matching_metric_results) / len(matching_metric_results)}%" + '\n')
    if images_filepath is not None:
        p.save_results_on_top_of_arrowhead(mtx, expected_results, algorithm_results, images_filepath)
    if expected_filepath is not None:
        with open(expected_filepath, 'w') as out:
            out.truncate()
            for tad in expected_results:
                out.write(f"{tad[0]}, {tad[1]}\n")
    if found_filepath is not None:
        with open(found_filepath, 'w') as out:
            out.truncate()
            for tad in algorithm_results:
                out.write(f"{tad[0] * R}, {tad[1] * R}\n")
