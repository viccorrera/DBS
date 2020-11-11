# stochastic prediction
# Bernoulli with 1000 values
data = mtcars
head(data)
x = mtcars$carb
table(x)  # frequency table

# model x using Bin(n, p)  -> variable should be discrete. No continuous values
# how to estimate p

n = max(x)  # n is max value for X

phat = sum(x)/(n * nrow(data))  # generic formula for binomial model. More than 2 outcomes

sim = rbinom(1000, n, phat)
sim
pred = mean(sim)
pred = round(pred)

################################

y = mtcars$cyl
# model y using multinomial model
# (n, p1, pk) pi is the ratio of i'th class
# this example, class 4, 6 and 8
tab = table(y)
phat = tab / sum(tab)  # parameter estimation based on data for multinomial model

# prediction
sim = rmultinom(100, size = 1, prob = phat)
sim
F = c()
for(i in 1:3){  # number of classes
  f_i = sum(sim[i,])
  F = c(F, f_i)
}
F


#############################
# Example 1 - Slides
x = c(8, 1, 1, 0)
p = c(0.4, 0.2, 0.2, 0.2)
n = 10
prob = dmultinom(x, n, p)  # used for probability computation
prob


# Example 2 - Slides
x = c(1, 2, 3)
p = c(0.2, 0.3, 0.5)
probability = dmultinom(x, 6, p)
probability

##########
# Other Example 1
p = 0.5
n = 4

dbinom(0, size = n, p)
dbinom(1, size = n, p)
dbinom(2, size = n, p)
dbinom(3, size = n, p)
dbinom(4, size = n, p)












# From the Book
# 10% of egg being brown.
# Probability of 2 eggs being brown
# to calculate this, we use dbinom
dbinom(2, size = 6, prob = 0.1)


# to predict next value, we do the following:
# Declare website link variable
link = 'http://users.stat.ufl.edu/~winner/data/remorse_death.csv'

# Read csv from website
data = read.csv(link)

# declare n, which is max value of X. In thi case, will be remorse
x = data$remorse
n = max(x)

# calculate phat
phat = sum(x)/(n * nrow(data))

# Simulate n=1000 cases
sim = rbinom(n = 100, size = n, prob = phat)
sim

mean(sim)