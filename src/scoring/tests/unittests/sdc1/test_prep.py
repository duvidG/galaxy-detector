import numpy as np
import pandas as pd
from ska_sdc.common.utils.cat_io import load_dataframe
from ska_sdc.common.utils.constants import expo_to_gauss, las_to_gauss
from ska_sdc.sdc1.dc_defns import CAT_COLUMNS, DEC_CENTRE, RA_CENTRE, TRAIN_LIM
from ska_sdc.sdc1.utils.prep import (
    calculate_conv_size,
    calculate_log_flux,
    calculate_pb_values,
    prepare_data,
    refine_area,
)


class TestPrepareData:
    def test_prepare_data(self, sub_path):
        df = load_dataframe(sub_path, columns=CAT_COLUMNS, skip_n=1)
        df_prep = prepare_data(df, 1400, train=False)

        expected_columns = CAT_COLUMNS + [
            "log_flux",
            "pb_corr_series",
            "a_flux",
            "size_max",
            "conv_size",
        ]
        assert list(df_prep.columns) == expected_columns
        assert isinstance(df_prep, pd.DataFrame)
        assert df_prep.isna().sum().sum() == 0

        # Check the index is sequential and uniform
        assert list((df_prep.index)) == list(range(len(df_prep.index)))

    def test_calculate_log_flux(self, truth_path):
        truth_cat_df = load_dataframe(truth_path, columns=CAT_COLUMNS)
        truth_cat_df_logflux = calculate_log_flux(truth_cat_df)

        assert "log_flux" in truth_cat_df_logflux.columns

        # Check first 10 rows are as expected:
        for row in truth_cat_df_logflux.head(10).itertuples():
            assert np.log10(row.flux) == row.log_flux

    def test_refine_area(self, truth_path):
        data_cat_freq = 1400

        cat_df = load_dataframe(truth_path, columns=CAT_COLUMNS)

        cat_df_no_train = refine_area(cat_df, data_cat_freq, train=False)
        cat_df_only_train = refine_area(cat_df, data_cat_freq, train=True)

        # Calculate a training-only sub-catalogue for specific comparison
        lims_freq = TRAIN_LIM.get(data_cat_freq, None)

        ra_min = lims_freq.get("ra_min")
        ra_max = lims_freq.get("ra_max")
        dec_min = lims_freq.get("dec_min")
        dec_max = lims_freq.get("dec_max")

        # Test truth catalog has 45 non-train rows, and 5 training rows
        assert len(cat_df_no_train.index) == 45
        assert len(cat_df_only_train.index) == 5
        assert (
            len(
                cat_df_no_train[
                    (cat_df_no_train["ra_core"] > ra_min)
                    & (cat_df_no_train["ra_core"] < ra_max)
                    & (cat_df_no_train["dec_core"] > dec_min)
                    & (cat_df_no_train["dec_core"] < dec_max)
                ].index
            )
            == 0
        )

    def test_calculate_pb_values(self):
        """
        Since this calculation involves a lookup in the primary beam table, the
        best way to test is to verify that the output is as expected for a
        small, known test dataset.
        """
        ra_vals = np.arange(RA_CENTRE - 1.5, RA_CENTRE + 1.5, 0.5)
        dec_vals = np.arange(DEC_CENTRE - 1.5, DEC_CENTRE + 1.5, 0.5)
        test_df = pd.DataFrame(
            {"ra_core": ra_vals, "dec_core": dec_vals, "flux": np.ones_like(ra_vals)}
        )

        test_df_pb = calculate_pb_values(test_df, 1400)
        assert isinstance(test_df_pb, pd.DataFrame)

        expected_aflux = [
            6.58000e-04,
            1.60390e-02,
            1.86827e-01,
            9.99358e-01,
            1.86827e-01,
            1.60390e-02,
        ]

        assert list(test_df_pb["a_flux"].round(8).values) == expected_aflux

    def test_calculate_conv_size(self):
        """
        Test by verifying test dataframes of consistent 'size' classes
        """
        b_maj_vals = np.array([1, 100, 200, 300])
        b_min_vals = np.array([1, 50, 200, 100])
        beam_size = 0.25

        test_df_1 = pd.DataFrame(
            {"b_maj": b_maj_vals, "b_min": b_min_vals, "size": np.ones_like(b_maj_vals)}
        )
        test_df_2 = pd.DataFrame(
            {
                "b_maj": b_maj_vals,
                "b_min": b_min_vals,
                "size": 2 * np.ones_like(b_maj_vals),
            }
        )
        test_df_3 = pd.DataFrame(
            {
                "b_maj": b_maj_vals,
                "b_min": b_min_vals,
                "size": 3 * np.ones_like(b_maj_vals),
            }
        )

        size_max_1 = np.maximum(b_min_vals, b_maj_vals) * las_to_gauss
        size_max_2 = np.maximum(b_min_vals, b_maj_vals)
        size_max_3 = np.maximum(b_min_vals, b_maj_vals) * expo_to_gauss

        expected_conv_size_1 = ((size_max_1 ** 2) + (beam_size ** 2)) ** 0.5
        expected_conv_size_2 = ((size_max_2 ** 2) + (beam_size ** 2)) ** 0.5
        expected_conv_size_3 = ((size_max_3 ** 2) + (beam_size ** 2)) ** 0.5

        test_df_conv_1 = calculate_conv_size(test_df_1, 1400)
        test_df_conv_2 = calculate_conv_size(test_df_2, 1400)
        test_df_conv_3 = calculate_conv_size(test_df_3, 1400)

        assert list(test_df_conv_1["conv_size"].values) == list(expected_conv_size_1)
        assert list(test_df_conv_2["conv_size"].values) == list(expected_conv_size_2)
        assert list(test_df_conv_3["conv_size"].values) == list(expected_conv_size_3)

    def test_remove_negatives(self, sub_path_errors):
        df = load_dataframe(sub_path_errors, columns=CAT_COLUMNS, skip_n=1)
        positive_cols = ["flux", "b_min", "b_maj", "core_frac"]

        # Check that the df has some negative values to be removed
        for col in positive_cols:
            assert (df[col] < 0.0).any()

        df_prep = prepare_data(df, 1400, train=False)

        # Check no more negative values remain in these columns
        for col in positive_cols:
            assert (df_prep[col] >= 0.0).all()
