from ska_sdc.sdc1.utils.sdc1_xmatch import Sdc1XMatch
from ska_sdc.sdc1.utils.sieve import calc_multid_err, process_kdtree_cand_df


class TestSieve(object):
    def test_sieve(self, sub_df_prep, truth_df_prep):
        cand_match_df = Sdc1XMatch(
            cat_sub=sub_df_prep, cat_truth=truth_df_prep, mode=0
        ).execute(func_name="crossmatch_kdtree")

        # Prior to sieve, there will be duplicates in both id and id_t columns
        assert any(cand_match_df["id"].value_counts() > 1)
        assert any(cand_match_df["id_t"].value_counts() > 1)

        sieved_sub_df = process_kdtree_cand_df(cand_match_df, mode=0)

        # After sieving, all id and id_t values will be unique
        assert all(sieved_sub_df["id"].value_counts() == 1)
        assert all(sieved_sub_df["id_t"].value_counts() == 1)

        assert "multi_d_err" in sieved_sub_df.columns

    def test_calc_multid_err(self, sub_df_prep, truth_df_prep):
        cand_match_df = Sdc1XMatch(
            cat_sub=sub_df_prep, cat_truth=truth_df_prep, mode=0
        ).execute(func_name="crossmatch_kdtree")

        cand_match_df_multid = calc_multid_err(cand_match_df, mode=0)

        # Check 5 values against known outputs; checked values should span all possible
        # size_id values
        assert list(cand_match_df_multid["multi_d_err"].tail().round(6).values) == [
            1.216788,
            0.535393,
            1.742147,
            2.680310,
            2.497556,
        ]
