#!/usr/bin/env Rscript


###############################################################################################
##        Tutorial for alphabase.ai Competition (Basic Logistic Regression Model)            ##
###############################################################################################


require(magrittr)
require(data.table)
options(stringsAsFactors=FALSE)
args <- commandArgs(TRUE)


##################################
## Step 1. Load alphabase.ai data
print("Loading the data ...")

train <- fread("alphabase_dataset/train.csv") %>% as.data.frame # Load the training data provided by alphabase.ai with Target.
dim(train)                    # Investigate the training data.

test <- fread("alphabase_dataset/test.csv") %>% as.data.frame   # Load the competition data provided by alphabase.ai with ID.
dim(test)                     # Investigate the competition data.

##
#################################




##################################
## Step 2. Train the Logistic Regression Model

# Missing values imputation
# You can also use R packages, such as MICE, Amelia, to implement NA imputation.
print("Missing values imputation ...")
features <- colnames(train)[!grepl("_flag", colnames(train))]
features <- setdiff(features, "Target")
for (feature in features) {
    mean_train <- mean(train[, feature], na.rm=TRUE)
    train[is.na(train[, feature]), feature] <- mean_train
    test[is.na(test[, feature]), feature] <- mean_train
}

# Train the Model, ignoring the NA-flag features.
print("Training the LR model ...")
model <- glm(as.factor(Target) ~ ., data=train[, c(features, "Target")], family=binomial(link='logit'))
summary(model)                 # Inspect the model to learn about it.

##
#################################




##################################
## Step 3. Predict the Competition Data with the newly trained model
print("Predicting the Competition Data...")
predictions <- predict(model, test, type="response") # Predict the Target, getting the probability.
submissions <- cbind(ID=as.character(test$ID), Target=predictions)

##
#################################




##################################
## Step 4. Write the CSV File and Get Ready for Submission
print("Writing predictions to abai_submissions.csv")
write.csv(submissions, file=paste0("abai_submission_", args[1], ".csv"), quote=FALSE, row.names=FALSE)

##
#################################



###############################################################################################
##   Finish! You get your first model done! Upload to alphabase.ai and see your rank!        ##
###############################################################################################
