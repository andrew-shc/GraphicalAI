from sklearn import linear_model

x = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]  # time
y = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]  # amount of cars
print(j for j in [i for i in zip(x, y)])
model = linear_model.LinearRegression().fit([i for i in zip(x, y)], y)

r = model.predict([[4, 3]])
print(r)
