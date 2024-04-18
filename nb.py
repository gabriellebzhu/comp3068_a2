import math
import statistics as stat

def calc_mean_std(data):
    no_means, yes_means, no_stds, yes_stds = [], [], [], []
    count_yes = 0
    P_yes, P_no = 0, 0
    i = 0
    yes_attributes, no_attributes = [], []
    
    while i < (len(data[0]) -1):
        yes_row, no_row = [], []
        for row in data:
            if row[-1] == "yes":
                yes_row.append(float(row[i]))
                if (i==0):
                    count_yes += 1
            else:
                no_row.append(float(row[i]))
        yes_attributes.append(yes_row)
        no_attributes.append(no_row)
        i+= 1
    
    for attribute in yes_attributes:
        yes_means.append(stat.mean(attribute))
        yes_stds.append(stat.stdev(attribute))
    
    for attribute in no_attributes:
        no_means.append(stat.mean(attribute))
        no_stds.append(stat.stdev(attribute))
        # maybe add error handling for how variane requires > 1 data points
    P_yes = count_yes / len(data)
    P_no = 1 - P_yes

    return no_means, yes_means, no_stds, yes_stds, P_yes, P_no

def probability_distribution(x, mean, std):
    if std == 0:
        return 1e-20
    else:
        power = -((float(x) - mean)**2)/(2*(std**2))
        denominator = std * math.sqrt(2*math.pi)
        result = (1/denominator)*(math.e ** power)
        return result

def nb_test_one_outcome(mean, std, test) -> str:
    # dont need to refer to the native training data, just use mean and std
    # just test numerator
    probability_product = 1
    num_attributes = len(test) #we choose to go up to the num of attributes in the TEST as this may be fewer than the training
    i = 0
    while i < num_attributes:
        attribute_prob = probability_distribution(test[i], mean[i], std[i])
        probability_product *= attribute_prob
        i += 1
    return probability_product

def classify_nb(training_file, testing_file):
    data_f = open(training_file, "r")
    data = [r.strip().split(",") for r in data_f.readlines()]
    data_f.close()

    if len(data) == 0:
        return []
    
    tests_f = open(testing_file, "r")
    tests = [t.strip().split(",") for t in tests_f.readlines()]
    tests_f.close()

    # 2D array: now each row is stored in a separate array

    if len(tests) == 0:
        return []
    
    col_num = len(tests[0]) # get no. attributes in the test data
    classified = []

    no_means, yes_means, no_stds, yes_stds, P_yes, P_no = calc_mean_std(data)

    for t in tests:
        yes_prob = nb_test_one_outcome(yes_means, yes_stds, t)*P_yes
        no_prob = nb_test_one_outcome(no_means, no_stds, t)*P_no
        if yes_prob >= no_prob:
            classified.append("yes")
        else:
            classified.append("no")

    return classified

