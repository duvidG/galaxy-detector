.. role:: python(code)
    :language: python

sdc1
=============================

The original IDL code is available at: https://astronomers.skatelescope.org/ska-science-data-challenge-1/

To score a submission for SDC1, one should first instantiate a Scorer. This can be done via two methods depending on the format of the input data.

If your input catalogues are in text format, one should use the class method: :meth:`ska_sdc.sdc1.sdc1_scorer.Sdc1Scorer.from_txt`. For example:

.. code-block:: python

   from ska_sdc.sdc1 import sdc1_scorer

   sub_cat_path = "/path/to/submission/catalogue.txt"
   truth_cat_path = "/path/to/truth/catalogue.txt"

   scorer = sdc1_scorer.from_txt(sub_cat_path, truth_cat_path, freq=1400)

However, if your input catalogues are already dataframes, one should instantiate the constructor for :class:`ska_sdc.sdc1.sdc1_scorer.Sdc1Scorer` class directly:

.. code-block:: python

   from ska_sdc.sdc1 import sdc1_scorer

   scorer = sdc1_scorer(df1, df2, freq=1400)

where :python:`df1` and :python:`df2` are dataframes.

When the class has been instantiated, the :meth:`ska_sdc.sdc1.sdc1_scorer.Sdc1Scorer.run` method can be called to run the scoring pipeline:

.. code-block:: python

   result = scorer.run()

which returns an instance of the Score class :class:`ska_sdc.sdc1.models.sdc1_score.Sdc1Score` containing all the details related to the run.

.. toctree::
    sdc1_scorer
    sdc1_score
