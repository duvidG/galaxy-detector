import pandas as pd
from ska_sdc.sdc1.models.sdc1_score import Sdc1Score
from ska_sdc.sdc1.utils.create_score import create_sdc_score
from ska_sdc.sdc1.utils.sdc1_xmatch import Sdc1XMatch
from ska_sdc.sdc1.utils.sieve import process_kdtree_cand_df


class TestCreateScore(object):
    def test_create_score(self, sub_df_prep, truth_df_prep):
        cand_match_df = Sdc1XMatch(
            cat_sub=sub_df_prep, cat_truth=truth_df_prep, mode=0
        ).execute(func_name="crossmatch_kdtree")
        sieved_sub_df = process_kdtree_cand_df(cand_match_df, mode=0)

        n_det = len(sub_df_prep.index)
        sdc_score = create_sdc_score(
            sieved_sub_df, 1400, n_det, mode=0, train=False, detail=True
        )
        sdc_score_nodetail = create_sdc_score(
            sieved_sub_df, 1400, n_det, mode=0, train=False, detail=False
        )

        assert isinstance(sdc_score, Sdc1Score)
        assert round(sdc_score.value, 6) == 1.465619
        assert sdc_score.n_bad == 4
        assert sdc_score.n_det == n_det
        n_match = sdc_score.n_match
        assert n_match == 30
        assert sdc_score.n_false == n_det - n_match
        assert round(sdc_score.score_det, 6) == 16.465619
        assert round(sdc_score.acc_pc, 6) == 54.885395
        assert isinstance(sdc_score.match_df, pd.DataFrame)
        assert isinstance(sdc_score.scores_df, pd.DataFrame)

        assert isinstance(sdc_score_nodetail, Sdc1Score)
        assert round(sdc_score_nodetail.value, 6) == 1.465619
        assert sdc_score_nodetail.n_bad == 4
        assert sdc_score_nodetail.n_det == n_det
        n_match = sdc_score_nodetail.n_match
        assert n_match == 30
        assert sdc_score_nodetail.n_false == n_det - n_match
        assert round(sdc_score_nodetail.score_det, 6) == 16.465619
        assert round(sdc_score_nodetail.acc_pc, 6) == 54.885395
        assert sdc_score_nodetail.match_df is None
        assert sdc_score_nodetail.scores_df is None
