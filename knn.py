def nn(test, data, cols, k):

    return "no"

def classify_nn(training_file, testing_file, k):
    data_f = open(training_file, "r")
    data = [r.strip().split(",") for r in data_f.readlines()]
    data_f.close()

    if len(data) == 0:
        return []
    
    tests_f = open(testing_file, "r")
    tests = [t.strip().split(",") for t in tests_f.readlines()]
    tests_f.close()

    if len(tests) == 0:
        return []
    
    col_num = len(tests[0])
    for t in tests:
        nn(t, data, col_num, k)

    return []


if __name__ == "__main__":
    classify_nn("data/norm-occupancy-estimation.csv", "data/testing/temp-test.csv", 1)