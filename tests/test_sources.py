#!/usr/bin/env python3

# (C) Copyright 2020 ECMWF.
#
# This software is licensed under the terms of the Apache Licence Version 2.0
# which can be obtained at http://www.apache.org/licenses/LICENSE-2.0.
# In applying this licence, ECMWF does not waive the privileges and immunities
# granted to it by virtue of its status as an intergovernmental organisation
# nor does it submit to any jurisdiction.
#

import sys
from climetlab import load_source, source
import pytest


def test_file_source_1():
    load_source("file", "docs/examples/test.grib")


@pytest.mark.skipif(sys.version_info < (3, 7), reason="Version 3.7 or greater needed")
def test_file_source_2():
    source.file("docs/examples/test.grib")


def zarr_not_installed():
    try:
        import zarr
        import s3fs

        return False
    except ImportError:
        return True


@pytest.mark.skipif(zarr_not_installed(), reason="Zarr or S3FS not installed")
def test_zarr_source_1():
    source = load_source(
        "zarr-s3",
        "https://storage.ecmwf.europeanweather.cloud/s2s-ai-competition/data/reference-set/0.1.20/zarr/rt-20200102.zarr",
    )
    ds = source.to_xarray()
    assert len(ds.forecast_time) == 1

@pytest.mark.skipif(zarr_not_installed(), reason="Zarr or S3FS not installed")
def test_zarr_source_2():
    import numpy as np
    from climetlab.utils.dates import to_datetimes_list
    import datetime
    source = load_source(
        "zarr-s3",
        ["https://storage.ecmwf.europeanweather.cloud/s2s-ai-competition/data/reference-set/0.1.20/zarr/rt-20200109.zarr",
        "https://storage.ecmwf.europeanweather.cloud/s2s-ai-competition/data/reference-set/0.1.20/zarr/rt-20200102.zarr"],
    )
    ds = source.to_xarray()
    assert len(ds.forecast_time) == 2
    dates = ds.forecast_time.values #.tolist()
    dates = to_datetimes_list([dates[0], dates[1]])
    assert dates[0] == datetime.datetime(2020,1,2)
    assert dates[1] == datetime.datetime(2020,1,9)
#    assert str(dates[0]) == datetime.datetime(2020,1,2)
#    assert str(dates[1]) == datetime.datetime(2020,1,9)
