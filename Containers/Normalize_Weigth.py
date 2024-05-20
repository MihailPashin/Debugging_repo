from dependency_injector import containers, providers
from sklearn.preprocessing import MinMaxScaler
from Packages.Calculate_Weight.weight_ECB import DataNormalizer,DataBoundary,DataController

class NormalizerWeight_Container(containers.DeclarativeContainer):

    scaler = providers.Factory(MinMaxScaler, feature_range=(1, 9))
    entity = providers.Factory(DataNormalizer, scaler=scaler)
    control = providers.Factory(DataController, data_normalizer=entity)
    boundary = providers.Factory(DataBoundary, controller=control)
