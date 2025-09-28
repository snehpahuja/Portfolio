library(readxl)
library(caTools)
library(e1071)
library(FSelector)
library(caret)


#import the dataset
airline <- read_xlsx("C:/Users/Sneh Pahuja/Desktop/flame/data mining/Airlinecustomersatisfactioncleaned.xlsx")

#Remove null values
airline <- na.omit(airline)

# subsetting 40% of dataset
airline <- airline[sample(nrow(airline), nrow(airline) / 2.5),]

#Change datatypes to factors
airline$Gender<-as.factor(airline$Gender)
airline$customer_type<-as.factor(airline$customer_type)
airline$travel_type<-as.factor(airline$travel_type)
airline$Class<-as.factor(airline$Class)
airline$satisfaction<-as.factor(airline$satisfaction)
levels(airline$satisfaction)<-c(0,1)
levels(airline$satisfaction)

#splitting the dataset into the Training Set and Test Set
set.seed(123)
split = sample.split(airline$satisfaction, SplitRatio = .7)

train = subset(airline, split == TRUE)
test = subset(airline, split == FALSE)

#Compute information gain for each feature
info_gain <- information.gain(formula(airline), airline)

#Convert information gain values to a data frame
info_gain_df <- data.frame(Feature = names(info_gain), Information_Gain = unname(info_gain))

#Sort the information gain values in descending order
sorted_info_gain <- info_gain_df[order(-info_gain_df$Information_Gain), ]

#Print the sorted information gain values
print(sorted_info_gain)

#Scaling only the relevant columns with high info gain
columns_to_scale <- c("flight_distance", "Class", "Departure_Delay_Mins", "Inflight_service2", "Bag_handling", "web_check_in", "onboard_service", "Arrival_Delay_mins", "Seat_comfort", "legroom")

# Apply feature scaling for standardisation to the selected columns in the training set
train[, columns_to_scale] <- lapply(train[, columns_to_scale], as.numeric)

# Apply feature scaling for standardisation to the selected columns in the test set
test[, columns_to_scale] <- lapply(test[, columns_to_scale], as.numeric)

classifier <- svm(formula = satisfaction ~ flight_distance + Class + Departure_Delay_Mins + Inflight_service2 + Bag_handling + web_check_in + onboard_service + Arrival_Delay_mins + Seat_comfort + legroom,
                    data = train,
                    type = "C-classification",
                    kernel = 'radial',
                    gamma = 0.01
                  )

print(classifier)

# Predict outcomes for the test set
y_pred <- predict(classifier, newdata = test)

# Evaluate the predictions
conf_matrix <- table(test$satisfaction, y_pred)
accuracy <- sum(diag(conf_matrix)) / sum(conf_matrix)

# Calculate sensitivity (recall)
sensitivity <- sensitivity(y_pred, test$satisfaction)

# Calculate specificity
specificity <- specificity(y_pred, test$satisfaction)

# Calculate precision
precision <- posPredValue(y_pred, test$satisfaction)

print(sensitivity)
print(specificity)
print(precision)
print(conf_matrix)
print(accuracy)



