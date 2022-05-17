import matplotlib.pyplot as plt
import seaborn as sns
from matplotlib.colors import TwoSlopeNorm, LogNorm


DEFAULT_DPI = 600

def show_arrowhead_matrix(A):
    plot = sns.heatmap(A, cmap=sns.color_palette("vlag", as_cmap=True), center=0)
    plt.show()


def show_initial_matrix(A):
    plot = sns.heatmap(A, cmap='YlOrRd')
    plt.show()


def show_unfiltered_corner_score_matrix(S):
    cmap = sns.diverging_palette(240, 10, s=99, as_cmap=True)
    divnorm = TwoSlopeNorm(vmin=S.min(), vcenter=0, vmax=S.max())
    plot = sns.heatmap(S, cmap=cmap, norm=divnorm)
    plt.show()


def show_results_on_top_of_data(data, results):
    plot = sns.heatmap(data, cmap='YlOrRd')
    display_tads(results)

    plt.show()


def show_results_on_unfiltered_corner_scores(data, results):
    cmap = sns.diverging_palette(240, 10, s=99, as_cmap=True)
    divnorm = TwoSlopeNorm(vmin=data.min(), vcenter=0, vmax=data.max())
    plot = sns.heatmap(data, cmap=cmap, norm=divnorm)
    display_tads(results)

    plt.show()


def display_tads(tads, color='C0'):
    for t in tads:
        plt.hlines(t[0], t[0], t[1], colors=color)
        plt.vlines(t[0], t[0], t[1], colors=color)
        plt.hlines(t[1], t[0], t[1], colors=color)
        plt.vlines(t[1], t[0], t[1], colors=color)


def show_results_on_top_of_arrowhead(arrowhead_matrix, results):
    plot = sns.heatmap(arrowhead_matrix, cmap=sns.color_palette("vlag", as_cmap=True), center=0)
    display_tads(results)
    plt.show()


def save_results_on_top_of_arrowhead(data, correct, obtained, save_filepath):
    plt.clf()
    plot = sns.heatmap(data, cmap='YlOrRd', norm=LogNorm())
    display_tads(correct, 'g')
    display_tads(obtained)
    plt.savefig(save_filepath, dpi=DEFAULT_DPI)


def show_correct_and_obtained_results(data, correct, obtained):
    plt.clf()
    plot = sns.heatmap(data, cmap='YlOrRd', norm=LogNorm())
    display_tads(correct, 'g')
    display_tads(obtained)
    plt.show()
