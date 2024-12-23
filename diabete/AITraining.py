from pycaret.classification import *
import pandas as pd

data = pd.read_csv("diabetes.csv")

clf = setup(data, target ="Outcome", session_id = 123)

best_model = compare_models()
save_model(best_model,"bestModel")
