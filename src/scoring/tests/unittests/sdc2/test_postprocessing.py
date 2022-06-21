from ska_sdc.sdc2.utils.sdc2_xmatch import Sdc2XMatch
from ska_sdc.sdc2.utils.xmatch_postprocessing import XMatchPostprocessing
from ska_sdc.sdc2.utils.xmatch_preprocessing import XMatchPreprocessing


class TestPostprocessing:
    def test_postprocessing(self, sub_cat_sdc2, truth_cat_sdc2, sdc2_config):
        cat_sub_prep = XMatchPreprocessing(
            step_names=["ScaleAndCalculateLargestSize"]
        ).preprocess(cat=sub_cat_sdc2, config=sdc2_config)
        cat_truth_prep = XMatchPreprocessing(
            step_names=["ScaleAndCalculateLargestSize"]
        ).preprocess(cat=truth_cat_sdc2, config=sdc2_config)

        in_col = sdc2_config["general"]["sub_cat_column_names"].split(",")
        all_col = in_col + ["conv_size", "spectral_size"]
        cand_cat = Sdc2XMatch(
            cat_sub=cat_sub_prep, cat_truth=cat_truth_prep, all_col=all_col
        ).execute(func_name="crossmatch_kdtree")

        cand_cat_postp = XMatchPostprocessing(
            step_names=["CalculateMultidErr", "Sieve"]
        ).postprocess(cat=cand_cat, config=sdc2_config)

        assert len(cand_cat_postp.index) == 27

        expected_multid_err = [
            0.633894,
            0.814016,
            0.555634,
            0.852382,
            0.228276,
        ]

        assert (
            list(cand_cat_postp["multi_d_err"].head(5).round(6).values)
            == expected_multid_err
        )
