library(readr)
set.seed(98121)

template <- read_csv("../io/template.csv")

##example set of predictions
prediction <- rnorm(nrow(template), sd=1.5)+7

##make sure nothing is below 0 otherwise it will fail validation
prediction[prediction<0] <- 0

##add prediction row to template
template$`pKd_[M]_pred` <- prediction

write_csv(template, "../io/prediction.csv")
