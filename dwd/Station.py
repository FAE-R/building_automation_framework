from datetime import datetime

from wetterdienst.provider.dwd.observation import (
    DwdObservationDataset,
    DwdObservationPeriod,
    DwdObservationRequest,
    DwdObservationResolution,
)
from wetterdienst import Settings

# don't display real cache_dir, which might contain sensible information
s = Settings.default().to_dict()
s.update({"cache_dir": "abc"})


def station_example():
    """Retrieve stations_result of DWD that measure temperature."""
    stations = DwdObservationRequest(
        parameter=DwdObservationDataset.TEMPERATURE_AIR,
        resolution=DwdObservationResolution.HOURLY,
        period=DwdObservationPeriod.RECENT,
        start_date=datetime(2023, 4, 8),
        end_date=datetime(2023, 4, 9),
    )

    result = stations.filter_by_distance(
        latlon=(50.789510, 6.049363), distance=30)

    print(result.df)


if __name__ == "__main__":
    station_example()
