import pytest
from ska_sdc.common.models.exceptions import InvalidCatalogueException
from ska_sdc.sdc2.models.sdc2_score import Sdc2Score
from ska_sdc.sdc2.sdc2_scorer import Sdc2Scorer


class TestSdc2Scorer:
    def test_sdc2_scorer_from_txt(self, sub_path_sdc2, truth_path_sdc2):
        scorer = Sdc2Scorer.from_txt(sub_path_sdc2, truth_path_sdc2)
        assert scorer.is_scoring_complete() is False

        scorer.run(train=False, detail=True)
        sdc_score = scorer.score
        assert scorer.is_scoring_complete()
        assert isinstance(sdc_score, Sdc2Score)
        assert round(sdc_score.value, 6) == 1.459772

    def test_sdc2_scorer_from_df(self, sub_cat_sdc2, truth_cat_sdc2):
        scorer = Sdc2Scorer(sub_cat_sdc2, truth_cat_sdc2)
        assert scorer.is_scoring_complete() is False

        scorer.run(train=False, detail=True)
        sdc_score = scorer.score
        assert scorer.is_scoring_complete()
        assert isinstance(sdc_score, Sdc2Score)
        assert round(sdc_score.value, 6) == 1.459772

    def test_sdc2_scorer_from_txt_nohead(
        self, sub_path_sdc2_nohead, truth_path_sdc2_nohead
    ):
        # Check that reading catalogues from disk with missing headers produces
        # the expected error.
        with pytest.raises(InvalidCatalogueException):
            Sdc2Scorer.from_txt(
                sub_path_sdc2_nohead,
                truth_path_sdc2_nohead,
            )
