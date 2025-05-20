import unittest
from joblib import load
import numpy as np
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from scripts.random_forest_ import RandomForestRegressor_model

class TestDataCreation(unittest.TestCase):
    def setUp(self):
        self.model = load("models/random_forest_model.joblib")

    def test_model_prediction_shape(self):
        sample_input = np.array([[4944,803,0,0,0,1,0,0,1,0,0,0,0,0,0,0,0,0,0,1]])
        prediction = self.model.predict(sample_input)
        self.assertEqual(prediction.shape, (1,))

    def test_same_model(self):
        sample_input = np.array([[4944,803,0,0,0,1,0,0,1,0,0,0,0,0,0,0,0,0,0,1]])
        prediction = self.model.predict(sample_input)
        model2 = RandomForestRegressor_model()
        prediction1 = model2.predict(sample_input)
        self.assertEqual(prediction, prediction1)



if __name__ == "__main__":
    unittest.main()