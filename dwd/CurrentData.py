from wetterdienst.provider.dwd.observation import (
    DwdObservationRequest,
    DwdObservationPeriod,
    DwdObservationResolution,
    DwdObservationParameter,
    DwdObservationDataset,
)
from wetterdienst import Settings


parameters = [
    DwdObservationParameter.HOURLY.TEMPERATURE_AIR_MEAN_200,
    # DwdObservationParameter.HOURLY.HUMIDITY,
]

values = (
    DwdObservationRequest(
        parameter=parameters, resolution=DwdObservationResolution.MINUTE_10, period=DwdObservationPeriod.NOW
    )
    .filter_by_station_id(station_id=[15000])
    .values.all()
)
print(values.df)
