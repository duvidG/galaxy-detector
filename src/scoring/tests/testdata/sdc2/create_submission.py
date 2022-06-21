# create a fake submission starting from the truth catalogue
# apply a flux threshold and introduce errors


import numpy as np
from astropy.table import Table

cat_file_name = "tests/testdata/sdc2/truth_sample/truth_sample.txt"
cat_truth = Table.read(cat_file_name, format="ascii")
print(cat_truth.columns)  # (to get the list of columns)

flux_thr = 0.0  # what should it be?

cat_truth = cat_truth[(cat_truth["line_flux_integral"] >= flux_thr)]
# need to change line flux perturbation to base on median not mean
cat = Table()
ngals = len(cat_truth["ra"])

cat["id"] = np.arange(ngals)

cat["ra"] = np.random.normal(loc=cat_truth["ra"], scale=0.001, size=ngals)

cat["dec"] = np.random.normal(loc=cat_truth["dec"], scale=0.001, size=ngals)

a = cat_truth["hi_size"].groups.aggregate(np.mean)  # 1% error on quantities
cat["hi_size"] = np.random.normal(loc=cat_truth["hi_size"], scale=0.1 * a, size=ngals)

a = cat_truth["line_flux_integral"].groups.aggregate(np.mean)  # 1% error on quantities
cat["line_flux_integral"] = np.random.normal(
    loc=cat_truth["line_flux_integral"], scale=0.01 * a, size=ngals
)

cat["central_freq"] = np.random.normal(
    loc=cat_truth["central_freq"], scale=0.001 * 1.0e9, size=ngals
)

a = cat_truth["pa"].groups.aggregate(np.mean)  # 1% error on quantities
cat["pa"] = np.random.normal(loc=cat_truth["pa"], scale=0.1 * a, size=ngals)

a = cat_truth["i"].groups.aggregate(np.mean)  # 1% error on quantities
cat["i"] = np.random.normal(loc=cat_truth["i"], scale=0.1 * a, size=ngals)

a = cat_truth["w20"].groups.aggregate(np.mean)  # 1% error on quantities
cat["w20"] = np.random.normal(loc=cat_truth["w20"], scale=0.001 * a, size=ngals)

shuffle = np.arange(len(cat))

np.random.shuffle(shuffle)


# cat = cat[shuffle]

cat.write(
    "tests/testdata/sdc2/submission_sample/submission_sample.txt",
    format="ascii",
    overwrite=True,
)
