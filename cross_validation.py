from knn import nn
import pprint

pp = pprint

def validate(training_file, k):
    data_f = open(training_file, "r")
    data = []
    fold = []

    # partition the dataset into folds
    for line in data_f:
        if "fold" in line:
            if len(fold) > 0:
                data.append(fold)
            fold = []
        elif line.strip() == "":
            pass
        else:
            fold.append(line.strip().split(","))
    if len(fold) > 0:
        data.append(fold)

    data_f.close()

    if len(data) == 0:
        return []
    
    # tests_f = open(testing_file, "r")
    # tests = [t.strip().split(",") for t in tests_f.readlines()]
    # tests_f.close()

    # if len(tests) == 0:
    #     return []
    
    # col_num = len(tests[0])
    # classified = []
    # for t in tests:
    #     classified.append(nn(t, data, col_num, k))

    # return classified

if __name__ == "__main__":
    validate("data/partitioned-occupancy.csv", 3)