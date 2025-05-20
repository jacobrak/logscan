import unittest
from joblib import load
import numpy as np
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from scripts.random_forest_ import RandomForestRegressor_model
import pandas as pd
from scripts.train_test_spliting import prepare_data

X_train, X_test, y_train, y_test = prepare_data()

columns = ['bytes', 'request_type_dummy', 'endpoint_dummy', 'is_error',
       'os_Mac OS X', 'os_Windows', 'os_iOS', 'd_Mac',
       'd_OnePlus ONEPLUS A6000', 'd_Other', 'd_iPhone', 'b_Chrome Mobile',
       'b_Edge', 'b_Edge Mobile', 'b_Firefox', 'b_Firefox Mobile',
       'b_Mobile Safari', 'b_Opera', 'b_Opera Mobile', 'b_Safari']
sample_input = pd.DataFrame(
    [[4944,803,0,0,0,1,0,0,1,0,0,0,0,0,0,0,0,0,0,1]],
    columns=columns
)

class TestDataCreation(unittest.TestCase):
    def setUp(self):
        self.model = load("models/random_forest_model.joblib")

    def test_model_prediction_shape(self):
        prediction = self.model.predict(sample_input)
        self.assertEqual(prediction.shape, (1,))

    def test_same_model(self):
        prediction = self.model.predict(sample_input)
        model2 = RandomForestRegressor_model()
        prediction1 = model2.predict(sample_input)
        self.assertEqual(prediction, prediction1)
    
    def test_model_acc(self):
        score = self.model.score(X_test, y_test)
        self.assertGreater(score, 0.5)
        
if __name__ == "__main__":
    unittest.main()