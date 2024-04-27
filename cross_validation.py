from knn import nn
from nb import calc_mean_std, nb_test_one_outcome
import pprint

pp = pprint


def partition(training_file):
    data_f = open(training_file, "r")
    parts = []
    fold = []

    # Partition the dataset along the folds.
    for line in data_f:
        if "fold" in line:
            # End the previous fold and start a new fold.
            if len(fold) > 0:
                parts.append(fold)
            fold = []
        elif line.strip() == "":
            pass  # noop
        else:
            # Add the current line into the current fold.
            fold.append(line.strip().split(","))

    # Add the last fold into the list of partitions.
    if len(fold) > 0:
        parts.append(fold)
    data_f.close()

    return parts


def validate_nn(training_file, k):
    parts = partition(training_file)

    if len(parts) == 0:
        return 0
    
    partition_num = len(parts)
    col_num = len(parts[0][0]) - 1

    average = 0
    for i in range(partition_num):
        
        data = []
        for j in range(partition_num):
            if not i == j:
                data.extend(parts[j])
        tests = parts[i]

        correct = 0
        for t in tests:
            result = nn(t[:-1], data, col_num, k)
            
            if result == t[-1]:
                correct += 1
        average += correct / float(len(tests))

    return average / partition_num

def validate_bayes(training_file):
    parts = partition(training_file)
    
    if len(parts) == 0:
        return 0

    partition_num = len(parts)
    col_num = len(parts[0][0]) - 1

    average = 0
    for i in range(partition_num):
        
        data = []
        for j in range(partition_num):
            if not i == j:
                data.extend(parts[j])
        tests = parts[i]
        no_means, yes_means, no_stds, yes_stds, P_yes, P_no = calc_mean_std(data)

        correct = 0
        for t in tests:
            result = "yes"
            yes_prob = nb_test_one_outcome(yes_means, yes_stds, t[:-1])*P_yes
            no_prob = nb_test_one_outcome(no_means, no_stds, t[:-1])*P_no
            if yes_prob >= no_prob:
                result = "yes"
            else:
                result = "no"
            
            if result == t[-1]:
                correct += 1
        average += correct / float(len(tests))

    return average / partition_num


if __name__ == "__main__":
    print(f"pima bayes: {validate_bayes('data/stratified/pima.csv')}")
    print(f"pima nn, k=10: {validate_nn('data/stratified/pima.csv', 10)}")
    print(f"pima nn, k=5: {validate_nn('data/stratified/pima.csv', 5)}")
    print(f"pima nn, k=2: {validate_nn('data/stratified/pima.csv', 2)}")
    print(f"pima nn, k=1: {validate_nn('data/stratified/pima.csv', 1)}")
    print(f"occ bayes: {validate_bayes('data/stratified/occupancy.csv')}")
    print(f"occ nn, k=10: {validate_nn('data/stratified/occupancy.csv', 10)}")
