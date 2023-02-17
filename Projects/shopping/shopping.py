import csv
import sys

from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier

TEST_SIZE = 0.4


def main():

    # Check command-line arguments
    if len(sys.argv) != 2:
        sys.exit("Usage: python shopping.py data")

    # Load data from spreadsheet and split into train and test sets
    evidence, labels = load_data(sys.argv[1])
    X_train, X_test, y_train, y_test = train_test_split(
        evidence, labels, test_size=TEST_SIZE
    )

    # Train model and make predictions
    model = train_model(X_train, y_train)
    predictions = model.predict(X_test)
    sensitivity, specificity = evaluate(y_test, predictions)

    # Print results
    print(f"Correct: {(y_test == predictions).sum()}")
    print(f"Incorrect: {(y_test != predictions).sum()}")
    print(f"True Positive Rate: {100 * sensitivity:.2f}%")
    print(f"True Negative Rate: {100 * specificity:.2f}%")

def month_to_int(month):
    """
    This functions returns the number of a given month.
    """
    months = ["Jan", "Feb", "Mar", "Apr", "May", "June", "Jul", "Aug", "Sep", 
            "Oct", "Nov", "Dec"]
    
    return months.index(month)

def visitor_to_int(visitor_type):
    """
    returns 1 for returning visitors, and 0 for non-returning
    visitors
    """
    if visitor_type == "Returning_Visitor":
        return 1
    return 0

def bool_to_int(bl:str):
    """
    returns 0 if bl is "FALSE", 1 if otherwise
    """
    if bl == "FALSE":
        return 0
    return 1

def evidence_types(row):
    """
    This function converst all values in a given row of 
    evidence to have the right types.
    """
    typed_row = []

    for i in range(len(row)):
        # if column =  Administrative, Informational, ProductRelated, 
        # OperatingSystems, Browser, Region, or TrafficType,
        # convert to int
        if i in [0, 2, 4, 11, 12, 13, 14]:
            typed_row.append(int(row[i]))
        
        # convert to float
        elif i in [1, 3, 5, 6, 7, 8, 9]:
            typed_row.append(float(row[i]))
        
        # special case: month
        elif i == 10:
            typed_row.append(month_to_int(row[i]))
        
        # special case: visitor_type
        elif i == 15:
            typed_row.append(visitor_to_int(row[i]))
        
        elif i == 16:
            typed_row.append(bool_to_int(row[i]))
    
    return typed_row

def load_data(filename):
    """
    Load shopping data from a CSV file `filename` and convert into a list of
    evidence lists and a list of labels. Return a tuple (evidence, labels).

    evidence should be a list of lists, where each list contains the
    following values, in order:
        - Administrative, an integer
        - Administrative_Duration, a floating point number
        - Informational, an integer
        - Informational_Duration, a floating point number
        - ProductRelated, an integer
        - ProductRelated_Duration, a floating point number
        - BounceRates, a floating point number
        - ExitRates, a floating point number
        - PageValues, a floating point number
        - SpecialDay, a floating point number
        - Month, an index from 0 (January) to 11 (December)
        - OperatingSystems, an integer
        - Browser, an integer
        - Region, an integer
        - TrafficType, an integer
        - VisitorType, an integer 0 (not returning) or 1 (returning)
        - Weekend, an integer 0 (if false) or 1 (if true)

    labels should be the corresponding list of labels, where each label
    is 1 if Revenue is true, and 0 otherwise.
    """
    evidence = []
    labels = []

    with open(filename) as file:
        reader = csv.reader(file, delimiter=',')
        next(reader)

        for row in reader:
            evidence.append(evidence_types(row[:17]))
            labels.append(bool_to_int(row[17]))
        
    return evidence, labels


def train_model(evidence, labels):
    """
    Given a list of evidence lists and a list of labels, return a
    fitted k-nearest neighbor model (k=1) trained on the data.
    """
    model = KNeighborsClassifier(n_neighbors=1)
    model.fit(evidence, labels)

    return model
    
def evaluate(labels, predictions):
    """
    Given a list of actual labels and a list of predicted labels,
    return a tuple (sensitivity, specificity).

    Assume each label is either a 1 (positive) or 0 (negative).

    `sensitivity` should be a floating-point value from 0 to 1
    representing the "true positive rate": the proportion of
    actual positive labels that were accurately identified.

    `specificity` should be a floating-point value from 0 to 1
    representing the "true negative rate": the proportion of
    actual negative labels that were accurately identified.
    """
    actual_positive = 0
    identified_positive = 0

    actual_negative = 0
    identified_negative = 0

    for actual, predicted in zip(labels, predictions):
        # positive case
        if actual == 1:
            actual_positive += 1

            # if prediction is also positive
            if predicted == 1:
                identified_positive += 1

        # negative case    
        else:
            actual_negative += 1

            # if predictioin is also negative
            if predicted == 0:
                identified_negative += 1
    
    sensitivity = identified_positive / actual_positive
    specificity = identified_negative / actual_negative

    return (sensitivity, specificity)
        


if __name__ == "__main__":
    main()
