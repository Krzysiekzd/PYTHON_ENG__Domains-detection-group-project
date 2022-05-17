import numpy as np
import scipy.sparse.csgraph as sc


def connected_components(matrix):
    tmp = matrix.copy()
    tmp[tmp != 0] = 1
    return sc.connected_components(tmp)


def largest_value_within_components(matrix):
    res = connected_components(matrix)
    output = list()
    for component_id in range(0, res[0]):
        component_vertexes = np.where(res[1] == component_id)
        component_coordinates_reshaped = np.array(np.meshgrid(component_vertexes, component_vertexes)).T.reshape(-1,
                                                                                                                 2)
        component_coordinates_where_format = (
            component_coordinates_reshaped.T[0], component_coordinates_reshaped.T[1])
        values_within_component = matrix[component_coordinates_where_format]
        max_value_indice = np.argmax(values_within_component)

        max_value = values_within_component[max_value_indice]
        all_coordinates_with_max_value = np.where(values_within_component == max_value)
        coordinates = component_coordinates_reshaped[all_coordinates_with_max_value]
        if coordinates[0][0] != coordinates[0][1]:
            output.append((coordinates[0][0], coordinates[0][1]))
    return output
