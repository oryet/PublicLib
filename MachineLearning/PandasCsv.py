import  pandas as pd
from sklearn.preprocessing import MinMaxScaler
import numpy


def readDataset(csvData):
    dataframe = pd.read_csv(csvData, usecols=[1])
    dataset = dataframe.values

    # 将整型变为float
    dataset = dataset.astype('float32')
    # 归一化 在下一步会讲解
    scaler = MinMaxScaler(feature_range=(0, 1))
    dataset = scaler.fit_transform(dataset)
    return dataset


# 对数据进行处理
def createTrainDataset(dataset, look_back):
#这里的look_back与timestep相同
    dataX, dataY = [], []
    for i in range(len(dataset)-look_back-1):
        a = dataset[i:(i+look_back)]
        dataX.append(a)
        dataY.append(dataset[i + look_back])
    return numpy.array(dataX),numpy.array(dataY)