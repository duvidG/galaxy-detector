.. role:: python(code)
    :language: python

sdc2
====

This is a skeleton framework for SDC2.

To score a submission for SDC2, one should first instantiate a Scorer. This can be done via two methods depending on the format of the input data.

If your input catalogues are in text format, one should use the class method: :meth:`ska_sdc.sdc2.sdc2_scorer.Sdc2Scorer.from_txt`. For example:

.. code-block:: python

   from ska_sdc.sdc2 import sdc2_scorer

   sub_cat_path = "/path/to/submission/catalogue.txt"
   truth_cat_path = "/path/to/truth/catalogue.txt"

   scorer = sdc2_scorer.from_txt(sub_cat_path, truth_cat_path)

However, if your input catalogues are already dataframes, one should instantiate the constructor for :class:`ska_sdc.sdc2.sdc2_scorer.Sdc2Scorer` class directly:

.. code-block:: python

   from ska_sdc.sdc2 import sdc2_scorer

   scorer = sdc2_scorer(df1, df2)

where :python:`df1` and :python:`df2` are dataframes.

When the class has been instantiated, the :meth:`ska_sdc.sdc2.sdc2_scorer.Sdc2Scorer.run` method can be called to run the scoring pipeline:

.. code-block:: python

   result = scorer.run()

which returns an instance of the Score class :class:`ska_sdc.sdc2.models.sdc2_score.Sdc2Score` containing all the details related to the run.

.. toctree::
    sdc2_scorer
    sdc2_score
    sdc2_stubs
