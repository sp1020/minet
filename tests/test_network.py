import os
import logging
import unittest
from minet import network


class TestInteractionAnalysis(unittest.TestCase):
    def test_load_data(self):
        current_dir = os.path.dirname(__file__)

        nt = network.Network()
        nt.load_interaction_results(
            f'{current_dir}/data/conditional_occurrence_directionality/microbial_association_direction.tsv')

    def test_write_graph(self):
        current_dir = os.path.dirname(__file__)

        nt = network.Network()
        nt.load_interaction_results(
            f'{current_dir}/data/conditional_occurrence_directionality/microbial_association_direction.tsv')
        nt.write_graph(
            f'{current_dir}/data/conditional_occurrence_directionality/graph_test.xml')
