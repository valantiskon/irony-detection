import ClassRead # Reads the input and the training sets
import numpy as np
from sklearn.model_selection import KFold
from sklearn.naive_bayes import BernoulliNB
from sklearn.metrics import roc_auc_score
from sklearn.metrics import confusion_matrix
from sklearn.metrics import precision_recall_fscore_support, accuracy_score

def BernoulliClass(train_A, words_of_tweets, extra_features, feature_selection, encoding, print_file):
    reading = ClassRead.Reader()  # Import the ClassRead.py file, to get the encoding

    x = np.array(words_of_tweets)
    y = train_A['label']

    # Initialize the roc-auc score running average list
    # Initialize a count to print the number of folds
    # Initialize metrics to print their average
    av_roc = 0.
    count = 0
    precision = 0
    accuracy = 0
    recall = 0
    f1score = 0

    # Initialize your 10 - cross vailidation
    # Set shuffle equals True to randomize your splits on your training data
    kf = KFold(n_splits=10, random_state=41, shuffle=True)

    # Set up for loop to run for the number of cross vals you defined in your parameter
    for train_index, test_index in kf.split(x):
        count += 1
        print('Fold #: ', count)

        with open(print_file, "a") as myfile: # Write above print into output file
            myfile.write('Fold #: ' + str(count) + '\n')

        # This indexs your train and test data for your cross validation and sorts them in random order, since we used shuffle equals True
        x_train, x_test = reading.get_enc(x[train_index], 1, y[train_index], train_index, extra_features, feature_selection, encoding, print_file), reading.get_enc(x[test_index], 0, y[test_index], test_index, extra_features, feature_selection, encoding, print_file)
        y_train, y_test = y[train_index], y[test_index]

#######################################################################################################################

        classifier = BernoulliNB()

        classifier.fit(x_train, y_train)
        y_pred = classifier.predict(x_test)

#######################################################################################################################

        # Your model is fit. Time to predict our output and test our training data
        print("Evaluating model...")

        with open(print_file, "a") as myfile: # Write above print into output file
            myfile.write("Evaluating model..." + '\n')

        roc = roc_auc_score(y_test, y_pred)

        # Print your ROC-AUC score for your kfold, and the running score average
        print('ROC: ', roc)
        av_roc += roc
        print('Continued Avg: ', av_roc / count)

        with open(print_file, "a") as myfile: # Write above print into output file
            myfile.write('ROC: ' + str(roc) + '\n' + 'Continued Avg: ' + str(av_roc / count) + '\n')

#######################################################################################################################

        y_pred = (y_pred > 0.5)

        # Creating the Confusion Matrix
        cm = confusion_matrix(y_test, y_pred)
        print(cm)

        with open(print_file, "a") as myfile: # Write above print into output file
            myfile.write(str(cm) + '\n')

        temp_accuracy = accuracy_score(y_test, y_pred)
        temp_precision, temp_recall, temp_f1_score, _ = precision_recall_fscore_support(y_test, y_pred,
                                                                                        average='binary')

        accuracy += temp_accuracy
        precision += temp_precision
        recall += temp_recall
        f1score += temp_f1_score

        print("Accuracy: ", temp_accuracy)
        print("Precision: ", temp_precision)
        print("Recall: ", temp_recall)
        print("F1 score: ", temp_f1_score)

    # Print average of metrics
    print("Average Precision: ", precision / 10)
    print("Average Accuracy: ", accuracy / 10)
    print("Average Recall: ", recall / 10)
    print("Average F1-score: ", f1score / 10)

    # Print your final average ROC-AUC score and organize your models predictions in a dataframe
    print('Average ROC:', av_roc / 10)

    with open(print_file, "a") as myfile:  # Write above print into output file
        myfile.write("Average Precision: " + str(precision / 10) + '\n' + "Average Accuracy: " + str(accuracy / 10) + '\n' + "Average Recall: " + str(recall / 10) + '\n' + "Average F1-score: " + str(f1score / 10) + '\n' + 'Average ROC:' + str(av_roc / 10) + '\n')