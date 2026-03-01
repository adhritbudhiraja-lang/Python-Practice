from pycaret.classification import * # To perform classification tasks using PyCaret
# Load available datasets list
from pycaret.datasets import get_data
dataSets = get_data('index')
print(dataSets)
# Use this to explore and select appropriate datasets for analysis
diabetesDataSet = get_data("diabetes")
s = setup(data=diabetesDataSet,target='Class varible')
rfModel = create_model('rf')
plot_model(rfModel,plot='confusion_matrix')
plot_model(rfModel)