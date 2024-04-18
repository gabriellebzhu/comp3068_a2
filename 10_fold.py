
data_f = open("pima.csv", "r")
data = [r.strip().split(",") for r in data_f.readlines()]
data_f.close()

num_rows = len(data)
num_attributes = len(data[0])

num_yes, num_no = 0, 0
yes_rows, no_rows = [], []

for row in data:
    if row[-1] == "yes":
        num_yes += 1
        yes_rows.append(row)
    elif row[-1] == "no":
        num_no += 1
        no_rows.append(row)

yes_base = num_yes//10
no_base = num_no//10

yes_folds = [[] for _ in range(10)]
no_folds = [[] for _ in range(10)]
total_folds = [[] for _ in range(10)]

def partition(type_rows, fold_array, base):
    fold_num = 0
    fill_in_remainders = False #only triggered true if we get to the end of the folds and there is remainder
    row_num=0
    for row in type_rows:
        current_fold = fold_array[fold_num]
        if fill_in_remainders:
            current_fold.append(row)
            fold_num += 1
        if len(current_fold) < base:
            current_fold.append(row)
        if len(current_fold) == base:
            fold_num += 1
            if fold_num == 10:
                fold_num = 0
                fill_in_remainders = True
    return fold_array

yes_folds = (partition(yes_rows, yes_folds, yes_base))
no_folds = (partition(no_rows, no_folds, no_base))


for i in range (0,9):
    total_folds[i].extend(yes_folds[i])
    total_folds[i].extend(no_folds[i])

print(total_folds)

f = open("answer.txt", "w")
for k in range(1, 10):
    f.write("fold" + str(k) + "\n")
    for row in total_folds[k-1]:
        my_string = ",".join(str(element) for element in row)
        f.write(my_string + "\n")
    f.write('\n')
