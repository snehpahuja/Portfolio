# ARIMA Analysis using BASE R ONLY 

print("=== ARIMA ANALYSIS USING BASE R ONLY ===")

# Create the data
months <- c("Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug")
visits <- c(35, 38, 40, 42, 45, 48, 50, 53)

# Create time series object (base R function)
ts_data <- ts(visits, start = c(2024, 1), frequency = 12)

print("Data loaded successfully:")
print(data.frame(Month = months, Visits = visits))

# Step 1: Plot the original time series and check for trend
print("=== STEP 1: PLOT ORIGINAL SERIES ===")
plot(ts_data, main = "Original Time Series - Monthly Visits", 
     xlab = "Time", ylab = "Visits", type = "o", col = "blue", lwd = 2, pch = 16)
grid()

# Visual trend analysis
trend_slope <- lm(visits ~ seq_along(visits))
print("Trend Analysis:")
print(paste("Linear trend slope:", round(coef(trend_slope)[2], 3)))
print("Visual inspection shows a clear upward trend")

# Step 2: Make the series stationary
print("=== STEP 2: MAKE SERIES STATIONARY ===")
print("Original series statistics:")
print(summary(visits))

# Apply first differencing
ts_diff1 <- diff(ts_data, differences = 1)
diff_values <- as.numeric(ts_diff1)

print("After first differencing:")
print(diff_values)
print("Differenced series statistics:")
print(summary(diff_values))

# Plot differenced series
plot(ts_diff1, main = "First Differenced Series", 
     xlab = "Time", ylab = "Differenced Visits", type = "o", col = "red", lwd = 2, pch = 16)
grid()
abline(h = mean(diff_values, na.rm = TRUE), col = "blue", lty = 2, lwd = 2)
abline(h = 0, col = "gray", lty = 1)

# Step 3: ACF and PACF plots (base R)
print("=== STEP 3: ACF AND PACF ANALYSIS ===")

# Set up 2x2 plot layout
par(mfrow = c(2, 2))

# ACF and PACF for original series
acf(ts_data, main = "ACF - Original Series", lag.max = 6, col = "blue")
pacf(ts_data, main = "PACF - Original Series", lag.max = 6, col = "blue")

# ACF and PACF for differenced series
acf(ts_diff1, main = "ACF - Differenced Series", lag.max = 5, col = "red")
pacf(ts_diff1, main = "PACF - Differenced Series", lag.max = 5, col = "red")

# Reset to single plot
par(mfrow = c(1, 1))

# Step 4: Identify ARIMA parameters (PROPER METHOD)
print("=== STEP 4: ARIMA PARAMETER IDENTIFICATION ===")

# d parameter - already determined
d <- 1  
print(paste("d =", d, "(differencing order - determined from stationarity analysis)"))

# PROPER p and q identification from ACF/PACF patterns
print("\n=== ANALYZING ACF/PACF PATTERNS FOR p AND q ===")

# Get ACF and PACF values for analysis
acf_diff <- acf(ts_diff1, lag.max = 5, plot = FALSE)
pacf_diff <- pacf(ts_diff1, lag.max = 5, plot = FALSE)

print("ACF values for differenced series (lags 1-5):")
acf_values <- round(acf_diff$acf[-1], 3)  # exclude lag 0
print(acf_values)

print("PACF values for differenced series (lags 1-5):")
pacf_values <- round(pacf_diff$acf, 3)
print(pacf_values)

# Significance threshold (approximate)
n <- length(diff_values)
threshold <- round(1.96/sqrt(n), 3)
print(paste("Approximate significance threshold (95% level):", threshold))

# Analyze patterns
print("\n=== PARAMETER IDENTIFICATION RULES ===")
print("ACF pattern analysis:")
significant_acf <- abs(acf_values) > threshold
print(paste("Significant ACF lags:", paste(which(significant_acf), collapse = ", ")))

print("PACF pattern analysis:")  
significant_pacf <- abs(pacf_values) > threshold
print(paste("Significant PACF lags:", paste(which(significant_pacf), collapse = ", ")))

# Parameter selection logic
print("\n=== PARAMETER SELECTION LOGIC ===")
print("ARIMA parameter identification rules:")
print("- If PACF cuts off after lag p and ACF tails off: AR(p) model")
print("- If ACF cuts off after lag q and PACF tails off: MA(q) model") 
print("- If both ACF and PACF tail off: ARMA(p,q) model")

# Determine p and q based on patterns
if(length(which(significant_pacf)) == 0) {
  p_suggested <- 0
  print("PACF shows no significant lags -> p = 0")
} else {
  p_suggested <- max(which(significant_pacf))
  print(paste("PACF significant up to lag", p_suggested, "-> p =", p_suggested))
}

if(length(which(significant_acf)) == 0) {
  q_suggested <- 0
  print("ACF shows no significant lags -> q = 0")
} else {
  q_suggested <- max(which(significant_acf))
  print(paste("ACF significant up to lag", q_suggested, "-> q =", q_suggested))
}

# For small sample, be conservative
print("\n=== FINAL PARAMETER SELECTION ===")
print("Given the small sample size (n=8), we'll be conservative:")

# Choose parameters
p <- min(p_suggested, 2)  # Cap at 2 for small sample
q <- min(q_suggested, 2)  # Cap at 2 for small sample

# If both are 0, use (1,1) as minimum
if(p == 0 && q == 0) {
  p <- 1
  q <- 1
  print("Both p and q would be 0, using minimum ARMA(1,1) for small sample")
}

print(paste("Selected parameters: ARIMA(", p, ",", d, ",", q, ")", sep = ""))
print("Reasoning:")
print(paste("- p =", p, "(from PACF analysis, capped for small sample)"))
print(paste("- d =", d, "(from differencing requirement)"))  
print(paste("- q =", q, "(from ACF analysis, capped for small sample)"))

# Try multiple models for comparison
print("\n=== TRYING MULTIPLE ARIMA MODELS ===")
models_to_try <- list(
  c(0,1,1), c(1,1,0), c(1,1,1), c(0,1,2), c(2,1,0)
)

model_results <- data.frame(
  Model = character(0),
  AIC = numeric(0),
  LogLik = numeric(0)
)

for(i in 1:length(models_to_try)) {
  order <- models_to_try[[i]]
  tryCatch({
    temp_model <- arima(ts_data, order = order)
    model_name <- paste0("ARIMA(", paste(order, collapse = ","), ")")
    model_results <- rbind(model_results, 
                           data.frame(Model = model_name, 
                                      AIC = round(AIC(temp_model), 2),
                                      LogLik = round(temp_model$loglik, 2)))
  }, error = function(e) {
    print(paste("Model", paste(order, collapse = ","), "failed to fit"))
  })
}

print("Model comparison (lower AIC is better):")
model_results <- model_results[order(model_results$AIC), ]
print(model_results)

# Select best model based on AIC
if(nrow(model_results) > 0) {
  best_model_name <- model_results$Model[1]
  best_params <- as.numeric(strsplit(gsub("[ARIMA()]", "", best_model_name), ",")[[1]])
  p <- best_params[1]
  d <- best_params[2] 
  q <- best_params[3]
  
  print(paste("BEST MODEL based on AIC:", best_model_name))
} else {
  print("Using default ARIMA(1,1,1)")
}

print(paste("FINAL SELECTED PARAMETERS: ARIMA(", p, ",", d, ",", q, ")", sep = ""))

# Step 5: Fit ARIMA model (base R function)
print("=== STEP 5: FIT ARIMA MODEL ===")

arima_model <- arima(ts_data, order = c(p, d, q))
print("ARIMA Model Summary:")
print(arima_model)

print("Model coefficients:")
print(arima_model$coef)
print(paste("AIC:", round(AIC(arima_model), 2)))
print(paste("Log-likelihood:", round(arima_model$loglik, 2)))

# Step 6: Forecast using base R
print("=== STEP 6: FORECASTING NEXT 2 MONTHS ===")

# Use predict function (base R)
arima_pred <- predict(arima_model, n.ahead = 2)

# Calculate confidence intervals (95%)
forecast_values <- as.numeric(arima_pred$pred)
forecast_se <- as.numeric(arima_pred$se)
lower_ci <- forecast_values - 1.96 * forecast_se
upper_ci <- forecast_values + 1.96 * forecast_se

print("ARIMA Forecasts:")
forecast_df <- data.frame(
  Month = c("Sep", "Oct"),
  Forecast = round(forecast_values, 1),
  Lower_95 = round(lower_ci, 1),
  Upper_95 = round(upper_ci, 1),
  Std_Error = round(forecast_se, 2)
)
print(forecast_df)

# Plot forecast
plot(ts_data, xlim = c(2024, 2024.9), ylim = c(30, 70),
     main = "ARIMA Forecast for Next 2 Months", 
     xlab = "Time", ylab = "Visits", type = "o", col = "blue", lwd = 2, pch = 16)
grid()

# Add forecast points
future_time <- c(2024 + 8/12, 2024 + 9/12)  # Sep, Oct
points(future_time, forecast_values, col = "red", pch = 17, cex = 1.5)
lines(future_time, forecast_values, col = "red", lwd = 2, lty = 2)

# Add confidence intervals
arrows(future_time, lower_ci, future_time, upper_ci, 
       length = 0.05, angle = 90, code = 3, col = "red", lwd = 2)

# Add labels
text(future_time[1], forecast_values[1] + 3, "Sep", col = "red", font = 2)
text(future_time[2], forecast_values[2] + 3, "Oct", col = "red", font = 2)

legend("topleft", legend = c("Historical Data", "Forecast", "95% CI"), 
       col = c("blue", "red", "red"), lty = c(1, 2, 1), lwd = c(2, 2, 2),
       pch = c(16, 17, NA))

# Step 7: Simple Exponential Smoothing (manual implementation)
print("=== STEP 7: EXPONENTIAL SMOOTHING COMPARISON ===")

# Simple exponential smoothing function
simple_exp_smooth <- function(data, alpha = 0.3) {
  n <- length(data)
  s <- numeric(n + 2)  # extra space for forecasts
  s[1] <- data[1]
  
  # Calculate smoothed values
  for(i in 2:n) {
    s[i] <- alpha * data[i] + (1 - alpha) * s[i-1]
  }
  
  # Forecast next 2 periods
  s[n+1] <- s[n]  # Simple forecast
  s[n+2] <- s[n]  # Same for period 2
  
  return(list(fitted = s[1:n], forecasts = s[(n+1):(n+2)]))
}

# Apply exponential smoothing
alpha <- 0.3  # smoothing parameter
es_result <- simple_exp_smooth(visits, alpha)

print("Exponential Smoothing Results:")
es_forecasts <- es_result$forecasts
print(data.frame(
  Month = c("Sep", "Oct"),
  ES_Forecast = round(es_forecasts, 1)
))

# Step 8: Compare forecasts
print("=== STEP 8: FORECAST COMPARISON ===")
comparison_df <- data.frame(
  Month = c("Sep", "Oct"),
  ARIMA_Forecast = round(forecast_values, 1),
  ES_Forecast = round(es_forecasts, 1),
  Difference = round(forecast_values - es_forecasts, 1)
)
print("Forecast Comparison:")
print(comparison_df)

# Combined forecast plot
plot(ts_data, xlim = c(2024, 2024.9), ylim = c(30, 65),
     main = "Forecast Comparison: ARIMA vs Exponential Smoothing",
     xlab = "Time", ylab = "Visits", type = "o", col = "black", lwd = 2, pch = 16)
grid()

# Add ARIMA forecast
points(future_time, forecast_values, col = "blue", pch = 17, cex = 1.5)
lines(future_time, forecast_values, col = "blue", lwd = 2, lty = 2)

# Add ES forecast
points(future_time, es_forecasts, col = "green", pch = 18, cex = 1.5)
lines(future_time, es_forecasts, col = "green", lwd = 2, lty = 3)

legend("topleft", 
       legend = c("Historical", "ARIMA Forecast", "ES Forecast"),
       col = c("black", "blue", "green"), 
       lty = c(1, 2, 3), lwd = 2,
       pch = c(16, 17, 18))

# Step 9: Residual Analysis
print("=== STEP 9: RESIDUAL ANALYSIS ===")

# ARIMA residuals
arima_residuals <- residuals(arima_model)
arima_residuals <- arima_residuals[!is.na(arima_residuals)]

# ES residuals  
es_fitted <- es_result$fitted[-1]  # remove first value
es_residuals <- visits[-1] - es_fitted  # exclude first observation

# Set up 2x2 plot for residuals
par(mfrow = c(2, 2))

# ARIMA residual plots
plot(arima_residuals, main = "ARIMA Model Residuals", 
     xlab = "Time", ylab = "Residuals", type = "o", col = "blue", pch = 16)
abline(h = 0, col = "red", lty = 2, lwd = 2)
grid()

hist(arima_residuals, main = "ARIMA Residuals Distribution", 
     xlab = "Residuals", col = "lightblue", border = "blue", breaks = 4)
abline(v = 0, col = "red", lty = 2, lwd = 2)

# ES residual plots
plot(es_residuals, main = "ES Model Residuals", 
     xlab = "Time", ylab = "Residuals", type = "o", col = "green", pch = 16)
abline(h = 0, col = "red", lty = 2, lwd = 2)
grid()

hist(es_residuals, main = "ES Residuals Distribution", 
     xlab = "Residuals", col = "lightgreen", border = "green", breaks = 4)
abline(v = 0, col = "red", lty = 2, lwd = 2)

# Reset plot layout
par(mfrow = c(1, 1))

# Residual statistics
print("ARIMA Residual Statistics:")
print(summary(arima_residuals))
arima_rmse <- sqrt(mean(arima_residuals^2, na.rm = TRUE))
print(paste("ARIMA RMSE:", round(arima_rmse, 3)))

print("Exponential Smoothing Residual Statistics:")
print(summary(es_residuals))
es_rmse <- sqrt(mean(es_residuals^2, na.rm = TRUE))
print(paste("ES RMSE:", round(es_rmse, 3)))

# Model comparison summary
print("=== FINAL MODEL COMPARISON ===")
print("Model Performance (Lower is Better):")
performance_df <- data.frame(
  Model = c("ARIMA(1,1,1)", "Exponential Smoothing"),
  RMSE = round(c(arima_rmse, es_rmse), 3),
  AIC = c(round(AIC(arima_model), 1), "N/A")
)
print(performance_df)

if(arima_rmse < es_rmse) {
  print("RECOMMENDATION: ARIMA model performs better (lower RMSE)")
} else {
  print("RECOMMENDATION: Exponential Smoothing performs better (lower RMSE)")
}

print("=== ANALYSIS COMPLETE ===")