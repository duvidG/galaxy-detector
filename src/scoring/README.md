# Science Data Challenge Scoring API

This repository contains the code used to score submissions for SKA's Science Data Challenges (SDCs).

To date there are two such challenges, SDC1 (run in 2019) and SDC2 (running February-July 2021), and with each having similar methods of evaluating submissions.

Both SDCs challenged participants to identify and characterise sources in synthetic radio images. The source catalogues the participants produced (called the submission catalogues) can then be compared to the real source properties used in creating the synthetic images (called the truth catalogues) to determine which solutions achieve the best result.

Both SDC1 and SDC2 expose a different but consistent API to achieve this; an SdcScorer object is instantiated with submission and truth catalogues (file paths or `DataFrame`s), runs a scoring pipeline on these catalogues, and returns an `SdcScore` object which contains the key properties relating to the scoring of the catalogues.

Per-challenge documentation can be found in the relevant paths in the [parent repository](https://gitlab.com/ska-telescope/sdc/ska-sdc):

- ska_sdc
  - [sdc1](https://gitlab.com/ska-telescope/sdc/ska-sdc/-/tree/master/ska_sdc/sdc1)
  - [sdc2](https://gitlab.com/ska-telescope/sdc/ska-sdc/-/tree/master/ska_sdc/sdc2)

## Package Installation

The package is designed to be installed with the `pip` package manager:

```bash
pip install ska-sdc
```

This requires Python 3.6+ and has package dependencies which will be installed if not already present.

## Licence

Although this code is open-source under the 3-clause BSD licence, it is not released to the public until after each challenge is completed, since normal operation requires the truth catalogue to be available to the respective scoring pipeline.
