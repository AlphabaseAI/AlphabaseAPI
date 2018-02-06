# -*- coding: utf-8 -*-
#
"""
    
Tutorial for alphabase.ai Competition (Basic Logistic Regression Model)

prerequisites: sklearn, pandas, numpy
install the required packages by 'pip install sklearn, pandas, numpy'

.. alphabase website:
   https://alphabase.ai/

"""


import pandas as pd
import numpy as np
from sklearn.preprocessing import Imputer
from sklearn.linear_model import LogisticRegression
from sklearn.cross_validation import train_test_split


class LogRegr:

    def train_model(self, model_num, drop_ratio=.1):
        ##################################
        ## Step 1. Load alphabase.ai data
        print("Loading the data ...")
        # Load the data from the CSV files
        train = pd.read_csv('train.csv', header=0)  # Load the training data provided by alphabase.ai with Target.
        test = pd.read_csv('test.csv', header=0)    # Load the competition data provided by alphabase.ai with ID.
        
        ##
        #################################
        ##################################
        ## Step 2. Train the Logistic Regression Model
        # Prepare data, ignoring the NA-flag features
        target = train['Target']
        train = np.array(train)[:, :87]
        X_train, X_drop, Y, Y_drop = train_test_split(train, target, test_size=drop_ratio)
        ID = test['ID']
        X_test = np.array(test)[:, 1:88]
        
        # Missing values imputation
        print("Missing values imputation ...")
        imp = Imputer(missing_values='NaN', strategy='mean', axis=0)
        imp.fit(X_train)
        X_train = imp.transform(X_train)
        X_test = imp.transform(X_test)
        
        ## Create a Logistic Regression Model.
        print("Training the LR model ...")
        model = LogisticRegression(n_jobs=-1)
        model.fit(X_train, Y)
        
        ##
        #################################
        ##################################
        ## Step 3. Predict the Competition Data with the newly trained model
        print("Predicting the Competition Data...")
        y_test = model.predict_proba(X_test) # Predict the Target, getting the probability.
        pred = y_test[:, 1]                  # Get the probabilty of being 1.
        pred_df = pd.DataFrame(data={'Target': pred})
        submissions = pd.DataFrame(ID).join(pred_df)
        
        ##
        #################################
        ##################################
        ## Step 4. Write the CSV File and Get Ready for Submission
        # Save the predictions out to a CSV file
        print("Saving predictions...")
        submissions.to_csv("abai_submission_" + str(model_num) + ".csv", index=False)

        ##
        #################################