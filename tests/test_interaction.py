"""
Tests for interaction analysis
"""

import os
import logging
import unittest
from minet import interaction_analysis


class TestInteractionAnalysis(unittest.TestCase):
    def test_load_feature_table(self):
        current_dir = os.path.dirname(__file__)

        analyzer = interaction_analysis.Analyzer()
        analyzer.load_feature_table(
            f'{current_dir}/data/conditional_occurrence_directionality/feature-table.tsv', depth=5000, prevalence=0.1)
        
    def test_evaluate_feature_association(self):
        current_dir = os.path.dirname(__file__)

        analyzer = interaction_analysis.Analyzer()
        analyzer.load_feature_table(
            f'{current_dir}/data/conditional_occurrence_directionality/feature-table.tsv', depth=1000, prevalence=0.5, preprocessing=True)
        analyzer.evaluate_feature_association(
            f'{current_dir}/data/conditional_occurrence_directionality/result.tsv')
