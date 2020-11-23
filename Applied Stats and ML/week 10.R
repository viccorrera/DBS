library(e1071)  #skitlearn in R
dataset = iris
acc = 0
head(dataset)
n = nrow(dataset)
for(i in 1:200){
  index = sample(n, n * (80/100))
  trainset = dataset[index,]
  testset = dataset[-index,]
  m = naiveBayes(Species ~., data = trainset)
  pred = predict(m, testset[, -5])  # exclude target column
  accuracy = mean(pred == testset$Species)
  accuracy
  cm = table(pred, testset$Species)
  cm
  acc = acc + (1/200) * accuracy
}
acc

# how to predict a value
x = tail(dataset, 1)
predict(m, x[, -5])
