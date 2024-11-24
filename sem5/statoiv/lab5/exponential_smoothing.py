import numpy as np

class ExponentialSmoothing:
    def __init__(self, alpha=0.2, beta=0.1, gamma=0.1, season_length=12):
        self.alpha = alpha
        self.beta = beta
        self.gamma = gamma
        self.season_length = season_length
    
    def fit(self, train):
        self.train = np.array(train)
        self.n = len(self.train)
        
        self.level = np.zeros(self.n)
        self.trend = np.zeros(self.n)
        self.seasonal = np.zeros(self.n)

        self.level[0] = self.train[0]
        self.trend[0] = self.train[1] - self.train[0]
        self.seasonal[:self.season_length] = self.train[:self.season_length] - np.mean(self.train[:self.season_length])

        for t in range(1, self.n):
            if t < self.season_length:
                self.seasonal[t] = self.train[t] - self.level[t-1]
            else:
                self.seasonal[t] = self.gamma * (self.train[t] - self.level[t-1]) + (1 - self.gamma) * self.seasonal[t-self.season_length]
            
            self.level[t] = self.alpha * (self.train[t] - self.seasonal[t]) + (1 - self.alpha) * (self.level[t-1] + self.trend[t-1])
            self.trend[t] = self.beta * (self.level[t] - self.level[t-1]) + (1 - self.beta) * self.trend[t-1]

    def forecast(self, forecast_length):
        forecasts = []
        for h in range(1, forecast_length + 1):
            forecast = self.level[-1] + h * self.trend[-1] + self.seasonal[(self.n + h - self.season_length) % self.n]
            forecasts.append(forecast)
        return np.array(forecasts)


