import pandas as pd
import numpy as np

from sklearn.preprocessing import OneHotEncoder
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier

class RoadModel:
    """
    RoadModel is a singleton class that loads the CSV data of road segments,
    cleans it, trains a classification model on 'pci23_d',
    and provides a predict() method for new road segments.
    """
    
    _instance = None
    
    def __init__(self):
        self.model = None
        self.dt = None
        self.encoder_paveclass = None
        self.encoder_funclass = None
        
        self.features = [
            'pwidth', 
            'pav_length',
        ]
        
        self.target = 'pci23_d'
        self.road_data = pd.read_csv('datasets/streetsRepairLineSegments/sd_paving_segs_datasd.csv')
        
    def _clean(self):
        keep_cols = ['pwidth', 'pav_length', 'paveclass', 'funclass', 'pci23_d']
        self.road_data = self.road_data[keep_cols]
        self.road_data.dropna(subset=keep_cols, inplace=True)

        cat_cols = ['paveclass', 'funclass']
        self.encoder_paveclass = OneHotEncoder(handle_unknown='ignore')
        self.encoder_funclass = OneHotEncoder(handle_unknown='ignore')

        paveclass_encoded = self.encoder_paveclass.fit_transform(self.road_data[['paveclass']]).toarray()
        paveclass_cats = [f"paveclass_{c}" for c in self.encoder_paveclass.categories_[0]]
        paveclass_df = pd.DataFrame(paveclass_encoded, columns=paveclass_cats)
        
        funclass_encoded = self.encoder_funclass.fit_transform(self.road_data[['funclass']]).toarray()
        funclass_cats = [f"funclass_{c}" for c in self.encoder_funclass.categories_[0]]
        funclass_df = pd.DataFrame(funclass_encoded, columns=funclass_cats)

        self.road_data.reset_index(drop=True, inplace=True)
        paveclass_df.reset_index(drop=True, inplace=True)
        funclass_df.reset_index(drop=True, inplace=True)

        self.road_data = pd.concat([self.road_data, paveclass_df, funclass_df], axis=1)
        self.road_data.drop(columns=cat_cols, inplace=True)
        self.features.extend(paveclass_cats + funclass_cats)
    
    def _train(self):
        X = self.road_data[self.features]
        y = self.road_data[self.target]

        # Increase max_iter to address convergence warning
        self.model = LogisticRegression(max_iter=1500)
        self.model.fit(X, y)

        self.dt = DecisionTreeClassifier()
        self.dt.fit(X, y)

        print("[RoadModel] Training complete.")

    @classmethod
    def get_instance(cls):
        if cls._instance is None:
            cls._instance = cls()
            cls._instance._clean()
            cls._instance._train()
        return cls._instance

    def predict(self, road_features):
        road_df = pd.DataFrame([road_features])
        
        if 'paveclass' in road_df.columns:
            paveclass_encoded = self.encoder_paveclass.transform(road_df[['paveclass']]).toarray()
            paveclass_cats = [f"paveclass_{c}" for c in self.encoder_paveclass.categories_[0]]
            paveclass_df = pd.DataFrame(paveclass_encoded, columns=paveclass_cats)
            road_df = pd.concat([road_df.reset_index(drop=True), paveclass_df], axis=1)
            road_df.drop(columns=['paveclass'], inplace=True)

        if 'funclass' in road_df.columns:
            funclass_encoded = self.encoder_funclass.transform(road_df[['funclass']]).toarray()
            funclass_cats = [f"funclass_{c}" for c in self.encoder_funclass.categories_[0]]
            funclass_df = pd.DataFrame(funclass_encoded, columns=funclass_cats)
            road_df = pd.concat([road_df.reset_index(drop=True), funclass_df], axis=1)
            road_df.drop(columns=['funclass'], inplace=True)
        
        for col in self.features:
            if col not in road_df.columns:
                road_df[col] = 0
        
        road_df = road_df[self.features]
        
        prob_array = self.model.predict_proba(road_df)[0]
        classes = self.model.classes_
        class_probabilities = {cls: float(prob) for cls, prob in zip(classes, prob_array)}
        
        predicted_class = self.model.predict(road_df)[0]
        
        return {
            "predicted_class": predicted_class,
            "probabilities": class_probabilities
        }

    def feature_importances(self):
        importances = self.dt.feature_importances_
        return {feature: importance for feature, importance in zip(self.features, importances)}

def initRoads():
    RoadModel.get_instance()

def testRoads():
    sample = {
        "pwidth": 36,
        "pav_length": 400.6361,
        "paveclass": "AC Improved",
        "funclass": "CL 2 LANE SUB-COLLECTOR"
    }
    rm = RoadModel.get_instance()
    result = rm.predict(sample)
    print("Prediction Test:", result)
    print("Feature Importances:", rm.feature_importances())
