import unittest

from evm_ranking import mean_from_experts, calc_weights_EVM
from gmm_ranking import geometric_mean, remap_from_1_9_17_to_1over9_1_9, weights_of_attributes


class TestAHP(unittest.TestCase):

    def test_AIJ(self):
        expected = [[1.0, 3.175, 0.481, 1.260], [0.315, 1.0, 5.0, 0.579], [2.080, 0.200, 1.0, 1.326],
                    [0.794, 1.726, 0.754, 1.0]]
        list_matrix = [[[1, 4, 4, 2], [0.25, 1, 5, 7], [0.25, 0.2, 1, 2], [0.5, 0.14285714285714285, 0.5, 1]],
                       [[1, 4, 0.16666666666666666, 1], [0.25, 1, 5, 0.16666666666666666], [6.0, 0.2, 1, 7],
                        [1.0, 6.0, 0.14285714285714285, 1]],
                       [[1, 2, 0.16666666666666666, 1], [0.5, 1, 5, 0.16666666666666666],
                        [6.0, 0.2, 1, 0.16666666666666666], [1.0, 6.0, 6.0, 1]]]
        result = mean_from_experts(list_matrix)
        result = [[round(result[i][j], 3) for j in range(len(result[0]))] for i in range(len(result))]
        self.assertEqual(expected, result)

    def test_EVM(self):
        expected = [[0.34, 0.35, 0.3], [0.35, 0.37, 0.28], [0.18, 0.28, 0.54], [0.39, 0.47, 0.14]]
        list_matrix = [[7.5504, 7.74, 6.7072], [6.5607999999999995, 6.994400000000001, 5.368],
                       [2.84, 4.28, 8.386666666666667], [5.20472, 6.17192, 1.81752]]
        result = calc_weights_EVM(list_matrix)
        self.assertEqual(expected, result)

    def test_GMM(self):
        expected = [0.083, 0.114, 0.350, 0.453]
        list_matrix = [[1, 0.25, 0.25, 0.5], [4, 1, 0.2, 0.14285714285714285], [4, 5, 1, 0.5], [2, 7, 2, 1]]
        result = geometric_mean(list_matrix)
        result = [round(result[i], 3) for i in range(len(result))]
        self.assertEqual(expected, result)

    def test_value_mapper(self):
        expected = [0.111, 0.125, 0.143, 0.167, 0.2, 0.25, 0.333, 0.5, 1, 2, 3, 4, 5, 6, 7, 8, 9]
        result = []
        for i in range(1, 18):
            result.append(round(remap_from_1_9_17_to_1over9_1_9(i), 3))
        self.assertEqual(expected, result)

    def test_normalize(self):
        mtx = [[0.24608130495730848, 0.24608130495730854, 0.24608130495730854, 0.2460813049573085],
               [0.19645630082739804, 0.1964563008273981, 0.1964563008273981, 0.19645630082739807],
               [0.2750520368718406, 0.27505203687184065, 0.27505203687184065, 0.2750520368718406],
               [0.28241035734345277, 0.2824103573434528, 0.2824103573434528, 0.28241035734345277]]
        result = weights_of_attributes(mtx)
        self.assertEqual(1, round(sum(result), 1))
