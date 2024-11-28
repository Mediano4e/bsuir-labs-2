import numpy as np


class ExponentialSmoothing:
    def __init__(self, data, seasonal_periods, alpha=0.2, beta=0.1, gamma=0.1):
        self.data = np.array(data)
        self.seasonal_periods = seasonal_periods
        self.alpha = alpha
        self.beta = beta
        self.gamma = gamma
        self.level = None
        self.trend = None
        self.seasonality = None
        self.fitted_values = []
        self.forecast_values = []
    
    def initialize_components(self):
        self.level = np.mean(self.data[:self.seasonal_periods])
        
        self.trend = (np.mean(self.data[self.seasonal_periods:2*self.seasonal_periods]) - 
                      np.mean(self.data[:self.seasonal_periods])) / self.seasonal_periods
        
        self.seasonality = np.zeros(self.seasonal_periods)
        for i in range(self.seasonal_periods):
            self.seasonality[i] = np.mean(self.data[i::self.seasonal_periods]) - self.level
    
    def fit(self):
        self.initialize_components()
        n = len(self.data)
        level = self.level
        trend = self.trend
        seasonality = self.seasonality
        fitted_values = []
        
        for t in range(n):
            if t >= self.seasonal_periods:
                seasonal_component = seasonality[t % self.seasonal_periods]
            else:
                seasonal_component = 0
            
            fitted = level + trend + seasonal_component
            fitted_values.append(fitted)
            
            if t >= self.seasonal_periods:
                error = self.data[t] - fitted
                new_level = self.alpha * (self.data[t] - seasonal_component) + (1 - self.alpha) * (level + trend)
                new_trend = self.beta * (new_level - level) + (1 - self.beta) * trend
                new_seasonality = self.gamma * error + (1 - self.gamma) * seasonal_component
                
                level, trend = new_level, new_trend
                seasonality[t % self.seasonal_periods] = new_seasonality
        
        self.level = level
        self.trend = trend
        self.seasonality = seasonality
        self.fitted_values = np.array(fitted_values)
    
    def forecast(self, steps):
        forecasts = []
        for h in range(steps):
            seasonal_component = self.seasonality[(len(self.data) + h) % self.seasonal_periods]
            forecast = self.level + h * self.trend + seasonal_component
            forecasts.append(forecast)
        self.forecast_values = np.array(forecasts)
        return self.forecast_values
