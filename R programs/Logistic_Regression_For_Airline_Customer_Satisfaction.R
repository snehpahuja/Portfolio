library(readxl)
library(ggplot2)
library(caTools)
library(FSelector)
library(caret)

#Load data
airline<-read_xlsx("C:/Users/Sneh Pahuja/Desktop/flame/data mining/Airlinecustomersatisfactioncleaned.xlsx")

#Preprocess/Clean data:

#Check for missing values and data types
num_na_values <- sum(is.na(airline))
data_types <- sapply(airline, class)
duplicate_rows <- sum(duplicated(airline))
inconsistent_age <- sum(airline$Age < 0 | airline$Age > 120)

print(num_na_values)
print(data_types)
print(duplicate_rows)
print(inconsistent_age)

#Remove null values
airline <- na.omit(airline)

#Exploratory analysis:
summary(airline)
head(airline)
mean(airline$flight_distance)
mean(airline$Departure_Delay_Mins)
mean(airline$Arrival_Delay_mins)
quantile(airline$flight_distance,0.25)

#Change datatypes to factors
airline$Gender<-as.factor(airline$Gender)
airline$customer_type<-as.factor(airline$customer_type)
airline$travel_type<-as.factor(airline$travel_type)
airline$Class<-as.factor(airline$Class)
airline$satisfaction<-as.factor(airline$satisfaction)
levels(airline$satisfaction)<-c(0,1)
levels(airline$satisfaction)

#Train the logistic model
#Compute information gain for each feature
info_gain <- information.gain(formula(airline), airline)

#Convert information gain values to a data frame
info_gain_df <- data.frame(Feature = names(info_gain), Information_Gain = unname(info_gain))

#Sort the information gain values in descending order
sorted_info_gain <- info_gain_df[order(-info_gain_df$Information_Gain), ]

#Print the sorted information gain values
print(sorted_info_gain)


#Split data for training and testing
split <- sample.split(airline$satisfaction, SplitRatio = 0.7) 

train <- airline[split, ]
test <- airline[!split, ]
logistic_model <- glm(satisfaction ~ flight_distance + Class + Checkin_service + Inflight_service2 + Bag_handling + web_check_in + onboard_service + Seat_comfort + legroom + Arrival_Delay_mins + Departure_Delay_Mins, data= train, family = "binomial") 
summary(logistic_model) 

#Test model 
predictions <- predict(logistic_model, newdata = test, type = "response") 
summary(predictions) 
binary_predi <- ifelse(predictions > 0.5, 1, 0) 

#Convert binary predictions data to factor data type
is.factor(binary_predi) 
levels(binary_predi) 
binary_predi<-as.factor(binary_predi) 
levels(binary_predi)<-c("0","1") 



# Create confusion matrix
conf_matrix <- table(test$satisfaction, binary_predi)

#Print confusion matrix
print(conf_matrix)

# Calculate accuracy
accuracy <- sum(diag(conf_matrix)) / sum(conf_matrix)

# Print accuracy
print(accuracy)

#Check sensitivity
sensitivity(factor(test$satisfaction),binary_predi) 

#Check sensitivity
specificity(factor(test$satisfaction),binary_predi) 




