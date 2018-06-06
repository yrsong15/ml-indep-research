import numpy
from classifiers import create_decision_tree, create_random_forest, calculate_model_accuracy, calculate_confusion_matrix
from data import get_minecraft, get_first_n_samples
from sklearn.linear_model import LogisticRegression

def minecraft_confusion_matrix(featuretype='histogram'):
    data_train, data_test, target_train, target_test = get_minecraft(featuretype)
    model = create_decision_tree()

    model.fit(data_train, target_train)

    predict_train = model.predict(data_train)
    predict_test = model.predict(data_test)

    accuracy_train, accuracy_test = calculate_model_accuracy(predict_train, predict_test, target_train, target_test)
    print('Training accuracy: {0:3f}, Test accuracy: {1:3f}'.format(accuracy_train, accuracy_test))

    cfm = calculate_confusion_matrix(predict_test,target_test)
    print "Confusion matrix"
    print cfm

    for q in range(1,3):
        for p in range(0,q):
            #compute confusion between classes p and q
            index_pq = [i for i,v in enumerate(target_train) if v in [p,q]]
            modelpq = create_decision_tree()
            # fit model to the data only involving classes p and q
            modelpq.fit([data_train[i] for i in index_pq], [target_train[i] for i in index_pq])
            testindex_pq = [i for i,v in enumerate(target_test) if v in [p,q]]
            # calculate and print the accuracy
            predict_train_pq = modelpq.predict([data_train[i] for i in index_pq])
            predict_test_pq = modelpq.predict([data_test[i] for i in testindex_pq])
            accuracy_pq = calculate_model_accuracy(predict_train_pq, predict_test_pq, 
                [target_train[i] for i in index_pq], 
                [target_test[i] for i in testindex_pq])[1]

            print "One-vs-one accuracy between classes",p,"and",q,":",accuracy_pq

    return model, predict_train, predict_test, accuracy_train, accuracy_test



def minecraft_decision_tree():
    results = []
    model = None

    # Get the Minecraft dataset using get_minecraft() and create a decision tree
    data_train, data_test, target_train, target_test = get_minecraft('histogram')
    model = create_decision_tree()

    for n in [50, 100, 150, 200, 250]:
        # Fit the model using a subset of the training data of size n
        nData, nTarget = get_first_n_samples(data_train, target_train,n)
        model.fit(nData, nTarget)

        # use the model to fit the training data and predict labels for the training and test data
        predict_train = model.predict(nData)
        # nDataTest, nTargetTest = get_first_n_samples(data_test, target_test,n)
        predict_test = model.predict(data_test)

        # Calculate the accuracys of the model (use the training data that fit the model in the current iteration)
        accuracy_train_n, accuracy_test = calculate_model_accuracy(predict_train, predict_test, nTarget, target_test)

        results.append((n, accuracy_train_n, accuracy_test))

    print(results)
    return model, results


def minecraft_random_forest():
    results = []
    model = None

    # Get the Minecraft dataset
    data_train, data_test, target_train, target_test = get_minecraft('histogram')
    for n_estimators in [2, 5, 10, 20, 30]:
        # create a random forest classifier with n_estimators estimators
        model = create_random_forest(n_estimators)
        # use the model to fit the training data and predict labels for the training and test data
        model.fit(data_train, target_train)
        predict_train = model.predict(data_train)
        predict_test = model.predict(data_test)
        
        # TODO: calculate the accuracies of the models and add them to the results
        accuracy_train, accuracy_test = calculate_model_accuracy(predict_train, predict_test, target_train, target_test)
        results.append((n_estimators, accuracy_train, accuracy_test))
    print(results)
    return model, results


def log_regression(featuretype='histogram'):
    # model = None

    data_train, data_test, target_train, target_test = get_minecraft(featuretype)
    model = LogisticRegression()

    # Fit the model to the data using its fit method
    model.fit(data_train, target_train)

    # Use the model's predict method to predict labels for the training and test sets
    predict_train = model.predict(data_train)
    predict_test = model.predict(data_test)

    accuracy_train, accuracy_test = calculate_model_accuracy(predict_train, predict_test, target_train, target_test)
    print('Training accuracy: {0:3f}, Test accuracy: {1:3f}'.format(accuracy_train, accuracy_test))

    cfm = calculate_confusion_matrix(predict_test,target_test)
    print "Confusion matrix"
    print cfm

    for q in range(1,3):
        for p in range(0,q):
            #compute confusion between classes p and q
            index_pq = [i for i,v in enumerate(target_train) if v in [p,q]]
            modelpq = create_decision_tree()
            # fit model to the data only involving classes p and q
            modelpq.fit([data_train[i] for i in index_pq], [target_train[i] for i in index_pq])
            testindex_pq = [i for i,v in enumerate(target_test) if v in [p,q]]
            # calculate and print the accuracy
            predict_train_pq = modelpq.predict([data_train[i] for i in index_pq])
            predict_test_pq = modelpq.predict([data_test[i] for i in testindex_pq])
            accuracy_pq = calculate_model_accuracy(predict_train_pq, predict_test_pq, 
                [target_train[i] for i in index_pq], 
                [target_test[i] for i in testindex_pq])[1]

            print "One-vs-one accuracy between classes",p,"and",q,":",accuracy_pq

    return model, predict_train, predict_test, accuracy_train, accuracy_test

