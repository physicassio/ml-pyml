pyml is an interactive machine learning program in python 3. It is an experimental tool for automating processes of performing
logistic and linear regressions of datasets in csv files. It is capable of performing linear regression with arbitrary order
polynomial features (the program itself learns exponents for the features). Pyml is also capable of exporting the results
into json files and it keeps always the best result (accuracy), in case of logistic regressions. Apart from computing regressions,
it also allows the user to visualize the data before computations and also shows regression curves after computations are done.
All of this is done interactively in a extremely intuitive manner.



It works on linux systems with python 3.7 installed and uses only a few libraries, all of which are listed in the requirements.txt
file. All one needs to do is clone into its repository

$git clone https://www.github.com/physicassio/pyml

cd into the cloned directory, install dependencies

$pip3 install -r requirements.txt

and run it

$python3 pyml.py

All the fun thereafter is pure intuition.

Feel free to report issues/bugs, recommend improvements and contribute.
