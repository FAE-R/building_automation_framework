from wetterdienst import Settings
from wetterdienst.provider.dwd.mosmix import (
    DwdForecastDate,
    DwdMosmixRequest,
    DwdMosmixType,
)


def mosmix_example():
    """Retrieve Mosmix mosmix data by DWD."""
    # A. MOSMIX-L -- Specific stations_result - each station with own file
    settings = Settings(ts_shape=True, ts_humanize=True)

    # B. MOSMIX-L -- All stations_result - specified stations_result are extracted.
    Settings.tidy = True
    Settings.humanize = True

    # C. MOSMIX-S -- All stations_result - specified stations_result are extracted.

    request = DwdMosmixRequest(
        parameter=["TTT"],
        start_issue=DwdForecastDate.LATEST,  # automatically set if left empty
        mosmix_type=DwdMosmixType.SMALL,
    )

    stations = request.filter_by_station_id(
        station_id=["10500"],
    )

    response = next(stations.values.query())

    output_section(response.stations.df)
    output_section(response.df.head())


def output_section(data):
    print(data)


if __name__ == "__main__":
    mosmix_example()
