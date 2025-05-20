import unittest
from joblib import load
from scripts.random_forest_ import RandomForestRegressor_model

class TestDataCreation(unittest.TestCase):
    def setUp(self):
        self.model = load("models/random_forest_model.joblib")

    def same_model(self):
        RandomForestRegressor_model()