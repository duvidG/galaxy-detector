import pandas as pd
from ska_sdc.sdc2.utils.xmatch_preprocessing import XMatchPreprocessing


class TestPreprocessing:
    def test_scale_and_calculate_largest_size(self, sdc2_config):
        test_cat = pd.DataFrame(
            {
                "id": [0],
                "ra": [180.0],
                "dec": [-30.0],
                "hi_size": [1.0],
                "line_flux_integral": [5.0],
                "central_freq": [1.0e9],
                "pa": [270.0],
                "i": [45.0],
                "w20": [100.0],
            }
        )

        test_cat_prep = XMatchPreprocessing(
            step_names=["ScaleAndCalculateLargestSize"]
        ).preprocess(cat=test_cat, config=sdc2_config)

        assert list(test_cat_prep["largest_size"].round(8).values) == [0.55305336]

        assert list(test_cat_prep.columns) == [
            "id",
            "ra",
            "dec",
            "hi_size",
            "line_flux_integral",
            "central_freq",
            "pa",
            "i",
            "w20",
            "d_a",
            "ra_offset_physical",
            "dec_offset_physical",
            "conv_size",
            "physical_conv_size",
            "spectral_size",
            "physical_spectral_size",
            "largest_size",
        ]
