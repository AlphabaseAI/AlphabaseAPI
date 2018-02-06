# -*- coding: utf-8 -*-
#
"""

This simple example demonstrates how you can use the alphabase API (Python version).

You can also divide different functions (downloading, model training, and uploading) into different Python files.

For model training and predictions uploading, you should better calculate the accuracy (or logloss, AUC) of your
predictions first. Based on those metrics, you can choose the best ones to upload. Please do you best to automate
the whole process.

.. alphabase website:
   https://alphabase.ai/

"""


from os import path
from alphabaseAPI import AlphabaseAPI
from logisticRegression import LogRegr


# NEED TO BE CHANGED TO YOUR OWN INFO
# parameters needed for data downloading and predictions uploading
username = "iShares"
password = "ishares"
dest_dir = "/Users/iShares/Desktop/alphabase"


# initialize alphabase API
abai = AlphabaseAPI(dest_dir)


# dowload current round datasets
abai.download(username, password, unzip=True)


# TODO:
# can insert you machine learning models here
# to automate your model training process after data downloading

# model Examples
logRegr = LogRegr()

for i in range(4):
	logRegr.train_model(i)


# upload predictions after model training
for i in range(4):
	abai.upload(username, password, path.join(dest_dir, "abai_submission_" + str(i) + ".csv"))