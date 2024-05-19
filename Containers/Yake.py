from dependency_injector import containers, providers
from Packages.Yake_KeyWords_Extract.yake import YakeExtractor, YakeBoundary, YakeControl

class Yake_Container(containers.DeclarativeContainer):
    extractor = providers.Factory(YakeExtractor)
    control = providers.Factory(YakeControl, extractor=extractor)
    boundary = providers.Factory(YakeBoundary, control=control)
