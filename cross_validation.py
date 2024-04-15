from knn import nn
import pprint

pp = pprint

def validate(training_file, k):
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



if __name__ == "__main__":
    print(validate("data/partitioned-occupancy.csv", 10))