from sklearn.svm import OneClassSVM

X = [[0], [0.44], [1.65], [0.46], [1]]
data_train = [[0.2], [0.14], [0.85], [0.45], [0.76]]

classifier = OneClassSVM(gamma='auto').fit(data_train)

#classifier.fit(data_train)

print(classifier.predict(X))
print(classifier.score_samples(X))
