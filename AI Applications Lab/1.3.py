from pycaret.datasets import get_data
from pycaret.classification import *
import numpy
dataSets = get_data('index')
print(dataSets)
diabetesDataSet = get_data("diabetes")
rfModel = create_model('rf')
plot_model(rfModel,plot='confusion_matrix')
plot_model(rfModel)