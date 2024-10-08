import sys
import json
import os
import pandas
import pickle
import tflite_runtime.interpreter as tflite
import numpy as np

dirpath = os.path.dirname(os.path.realpath(__file__))

cols = [
    "Sex",
    "Age",
    "Weight",
    "IsSmoking",
    "MaxDNSeverityCategory",
    "MinAbsLymph",
    "MaxAbsLeic",
    "MaxPlt",
    "MaxESR",
    "MaxCProtein",
    "MaxFerritin",
    "MaxDDimer",
    "MaxUrea",
    "MaxCommonProtein",
    "MaxGlucose",
    "MaxALT",
    "MaxAST",
    "MaxBilirubin",
    "MaxMNO",
    "MinProtrombIndex",
    "MaxFibrinogen",
    "MaxCreatinine",
    "MinHemoglobin",
    "MaxTemp",
    "MinSaturation",
    "MaxBP",
    "HasIBS",
    "HasMyocardInfarct",
    "HasONMK",
    "HasHypertonia",
    "HasHOBL",
    "HasDiabetes",
    "HasObesity",
    "HasHPN",
    "HasCancer",
    "HasHIV",
    "HasPneumo",
    "MaxKT",
    "HasAsthma",
    "CovidVac",
    "FluVac",
    "PneumococcusVac",
    "WasInResuscitation",
    "WasOnIVL"
]

category_cols = ['Sex', 'IsSmoking', 'HasIBS', 'HasMyocardInfarct', 'HasONMK', 'HasHypertonia', 'HasHOBL', 'HasDiabetes', 'HasObesity', 'HasHPN', 'HasCancer', 'HasHIV', 'HasPneumo', 'MaxKT', 'HasAsthma', 'CovidVac', 'FluVac', 'PneumococcusVac', 'WasInResuscitation', 'WasOnIVL']

class TFLiteModel:
    def __init__(self, model_path: str):
        self.interpreter = tflite.Interpreter(model_path)
        self.interpreter.allocate_tensors()

        self.input_details = self.interpreter.get_input_details()
        self.output_details = self.interpreter.get_output_details()

    def predict(self, *data_args):
        assert len(data_args) == len(self.input_details)
        for data, details in zip(data_args, self.input_details):
            data = np.float32(data)
            self.interpreter.set_tensor(details["index"], data)
        self.interpreter.invoke()
        return self.interpreter.get_tensor(self.output_details[0]["index"])

def load_object(filename):
    filename = dirpath + '/bin/' + filename    
    object = None
    with open(filename, 'rb') as f:
        object = pandas.read_pickle(f)
    return object

def load_ml_model(modelname):
    filename = dirpath + '/models/' + modelname + "/" + modelname + ".pickle"
    model = None
    with open(filename, 'rb') as f:
        model = pickle.load(f)
    return model

def encode_categorical(dataframe):    
    for col in category_cols:
        dataframe[col] = dataframe[col].astype('bool')

    category_cols.append('MaxDNSeverityCategory')
    data_category_cols = dataframe[category_cols]
    data_category_cols['MaxDNSeverityCategory'] = data_category_cols['MaxDNSeverityCategory'].astype('string')

    data_category_cols = pandas.get_dummies(data_category_cols, dtype='float64')
    dummies_df = load_object('dummies.pickle')
    data_category_cols = data_category_cols.reindex(columns = dummies_df.columns, fill_value=0).drop(columns=['IsDead'])
    
    return data_category_cols

def normalize_numeric(dataframe):
    numeric_cols = []
    for col in cols:
        if col not in category_cols:
            numeric_cols.append(col)

    data_numeric_cols = dataframe[numeric_cols]
    scaler = load_object('scaler.pickle')

    data_numeric_cols = pandas.DataFrame(
        scaler.transform(data_numeric_cols),
        index=data_numeric_cols.index,
        columns=data_numeric_cols.columns    
        )
    
    return data_numeric_cols

if __name__ == "__main__":
    hasEmptyData = json.loads(sys.argv[1])
    inputData = json.loads(sys.argv[2])

    data = pandas.DataFrame(inputData)

    for col in cols:
        data[col] = data[col].astype(float)

    category_data = encode_categorical(data)
    numeric_data = normalize_numeric(data)

    data_processed = category_data.join(numeric_data)
    data_processed = data_processed.astype(float)

    models = [
        'covidNet',
        'histgboost'
    ]
    predictions = []
    for model_name in models:
        if model_name == 'covidNet' and not hasEmptyData:
            model = TFLiteModel(dirpath + "/models/covidnet/covidnet.tflite")
            prediction = model.predict(data_processed)
            predictions.append({"model": model_name, "pred": prediction[:,0].tolist()})
        else:
            if model_name != 'histgboost' and hasEmptyData:
                continue            
            model = load_ml_model(model_name)
            prediction = model.predict_proba(data_processed)
            predictions.append({"model": model_name, "pred": prediction[:,1].tolist()})
    print(json.dumps(predictions))    

    sys.stdout.flush()