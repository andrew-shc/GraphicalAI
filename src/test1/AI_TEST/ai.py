from sklearn import svm

# data to be inputted for machine learning
input_data = [
    # column = components
    # row each obj
    [5, 0, 14, 1, 5],
    [1, 0, 35, 10, 6],
    [1, 1, 15, 3, 9],
    [4, 1, 19, 7, 2],
]

output_data = [
    "MC",
    "CS",
    "Overwatch",
    "Mario",
]

# model, classify data into labels
model = svm.SVC()
print(model)
# learning algorithm
model.fit(input_data, output_data)
print(model.decision_function_shape)
# predicts
r = model.predict([[1, 1, 14, 3, 5]])
print(r)
