import numpy as np
from ska_sdc.sdc2.utils.sdc2_xmatch import Sdc2XMatch
from ska_sdc.sdc2.utils.xmatch_preprocessing import XMatchPreprocessing


class TestSdc2XMatch:
    def test_sdc2_xmatch(self, sub_cat_sdc2, truth_cat_sdc2, sdc2_config):
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

        assert list(cand_cat.columns) == [
            "id",
            "ra",
            "dec",
            "hi_size",
            "line_flux_integral",
            "central_freq",
            "pa",
            "i",
            "w20",
            "conv_size",
            "spectral_size",
            "id_t",
            "ra_t",
            "dec_t",
            "hi_size_t",
            "line_flux_integral_t",
            "central_freq_t",
            "pa_t",
            "i_t",
            "w20_t",
            "conv_size_t",
            "spectral_size_t",
        ]

        # Expect 27 matches between test sub and truth catalogues
        assert len(cand_cat.index) == 27

        # Verify that 3D distances for all matches are within the 'largest_size'

        # Add distance columns back to cand_cat_sub
        cand_cat_sub_id = cand_cat.set_index("id")
        cand_cat_truth_id = cand_cat.set_index("id_t")
        cat_sub_prep_id = cat_sub_prep.set_index("id")
        cat_truth_prep_id = cat_truth_prep.set_index("id")
        for col_name in [
            "largest_size",
            "ra_offset_physical",
            "dec_offset_physical",
            "d_a",
        ]:
            col_name_t = col_name + "_t"
            cand_cat_sub_id[col_name] = cat_sub_prep_id[col_name]
            cand_cat_truth_id[col_name_t] = cat_truth_prep_id[col_name]

            cand_cat[col_name] = cand_cat_sub_id[col_name].values
            cand_cat[col_name_t] = cand_cat_truth_id[col_name_t].values

        # Create new multi_d_dist column:
        cand_cat["multi_d_dist"] = np.sqrt(
            (cand_cat["ra_offset_physical"] - cand_cat["ra_offset_physical_t"]) ** 2
            + (cand_cat["dec_offset_physical"] - cand_cat["dec_offset_physical_t"]) ** 2
            + (cand_cat["d_a"] - cand_cat["d_a_t"]) ** 2
        )

        assert all(cand_cat["multi_d_dist"] < cand_cat["largest_size"])
