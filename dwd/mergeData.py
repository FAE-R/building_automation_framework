from wetterdienst import Settings
import pandas as pd
from wetterdienst.provider.dwd.mosmix import (
    DwdForecastDate,
    DwdMosmixRequest,
    DwdMosmixType,
)
from wetterdienst.provider.dwd.observation import (
    DwdObservationRequest,
    DwdObservationPeriod,
    DwdObservationResolution,
    DwdObservationParameter,
    DwdObservationDataset,
)
# import matplotlib.pyplot as plt
import datetime


def merge(parameters):
    ############ Retrieve Mosmix mosmix data by DWD ###############################

    request = DwdMosmixRequest(
        parameter=["TTT"],
        start_issue=DwdForecastDate.LATEST,  # automatically set if left empty
        mosmix_type=DwdMosmixType.SMALL,
    )

    stations = request.filter_by_station_id(
        station_id=["10505"],  # aachen-orsbach
    )

    response = next(stations.values.query())

    df_mosmix = response.df.set_index("date")

    df_mosmix = df_mosmix.resample('10T')['value'].last()

    df_mosmix = df_mosmix.interpolate(
        method='linear')

    ############# current ############################################################

    values = (
        DwdObservationRequest(
            parameter=parameters, resolution=DwdObservationResolution.MINUTE_10, period=DwdObservationPeriod.NOW
        )
        .filter_by_station_id(station_id=[15000])  # aachen-orsbach
        .values.all()
    )

    df_now = values.df.set_index("date")

    df_now = df_now["value"].interpolate(
        method='linear')

    ########### merge data ################################################################

    df = pd.concat([df_now, df_mosmix]).sort_index()

    df = df.resample('10T').interpolate(method='linear')

    df = df.loc[datetime.datetime.now(datetime.timezone.utc) - datetime.timedelta(hours=1):datetime.datetime.now(datetime.timezone.utc) +
                datetime.timedelta(hours=10)]

    if parameters[0] == DwdObservationParameter.MINUTE_10.TEMPERATURE_AIR_MIN_200:
        df = df - 273.15

    return df


if __name__ == "__main__":
    parameters = [
        # DwdObservationParameter.MINUTE_10.TEMPERATURE_AIR_MIN_200,
        DwdObservationParameter.MINUTE_10.HUMIDITY,
        # DwdObservationParameter.MINUTE_10.RADIATION_GLOBAL,
    ]

    data = merge(parameters)
    print(data)
    index_list = data.index.tolist()
    value_list = data.values.tolist()

    for i in range(len(index_list)):
        msg = {
            "table_id": "weather_temperature",
            "timestamp": index_list[i],  # .strftime('%Y-%m-%dT%H:%M:%S'),
            "value": value_list[i]
        }
        print(msg)

    # plt.plot(df_now)
    # plt.plot(df_mosmix)
    # plt.plot(df)

    # plt.show()
