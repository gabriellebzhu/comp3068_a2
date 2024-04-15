import math


def insert_best_neighbour(sorted_k_best_data: list, new_neighbour, k):
    for i in range(len(sorted_k_best_data)):
        if new_neighbour[0] < sorted_k_best_data[i][0]:
            sorted_k_best_data.insert(i, new_neighbour)
            break
    
    if len(sorted_k_best_data) > k:
        sorted_k_best_data.pop()
    elif len(sorted_k_best_data) < k:
        sorted_k_best_data.append(new_neighbour)

    return sorted_k_best_data


def averaged_nn(sorted_k_best_data):
    class_dict = {}
    for item in sorted_k_best_data:
        if item[1] not in class_dict:
            class_dict[item[1]] = 1
        else:
            class_dict[item[1]] += 1

    sorted_classes = sorted(class_dict.items(), key=lambda x: x[1], reverse=True)
    if len(sorted_classes) > 1 and sorted_classes[0][1] == sorted_classes[1][1]:
        # TODO(gabbie): check that this indeed solves ties correctly
        return "yes"
    return sorted_classes[0][0]


def nn(test, data, cols, k):
    # each item is a tuple pair of (`distance`, `class`)
    sorted_k_best_data = []

    for row in data:
        distance = 0
        for i in range(cols):
            # TODO(gabbie): use numpy to calculate instead for better performance
            distance += (float(row[i])-float(test[i])) ** 2
        distance = math.sqrt(distance)
        insert_best_neighbour(sorted_k_best_data, (distance,row[-1]), k)

    return averaged_nn(sorted_k_best_data)

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
    classified = []
    for t in tests:
        classified.append(nn(t, data, col_num, k))

    return classified


if __name__ == "__main__":
    print(classify_nn("data/norm-occupancy-estimation.csv", "data/testing/temp-test.csv", 5))