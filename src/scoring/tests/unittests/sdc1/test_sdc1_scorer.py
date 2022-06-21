from ska_sdc.sdc1.models.sdc1_score import Sdc1Score
from ska_sdc.sdc1.sdc1_scorer import Sdc1Scorer


class TestSdc1Scorer:
    def test_scorer_from_txt(self, sub_path, truth_path):
        scorer = Sdc1Scorer.from_txt(sub_path, truth_path, freq=1400)
        assert scorer.is_scoring_complete() is False

        scorer.run(mode=0, train=False, detail=True)
        sdc_score = scorer.score
        assert scorer.is_scoring_complete()
        assert isinstance(sdc_score, Sdc1Score)
        assert round(sdc_score.value, 6) == 1.465619

    def test_scorer_from_df(self, sub_df, truth_df):
        scorer = Sdc1Scorer(sub_df, truth_df, freq=1400)
        assert scorer.is_scoring_complete() is False

        scorer.run(mode=0, train=False, detail=True)
        sdc_score = scorer.score
        assert scorer.is_scoring_complete()
        assert isinstance(sdc_score, Sdc1Score)
        assert round(sdc_score.value, 6) == 1.465619
