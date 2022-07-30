import numpy as np
import matplotlib.pyplot as plt
import yfinance as yf

class SMABacktester():
    def __init__(self, symbol, SMA_S, SMA_L, start, end):
        self.symbol = symbol
        self.SMA_S = SMA_S
        self.SMA_L = SMA_L
        self.start = start
        self.end = end
        self.results = None
        self.get_data()
    def get_data(self):
        df = yf.download(self.symbol, start = self.start, end = self.end)
        data = df.Close.to_frame()
        data["returns"] = np.log(data.Close / data.Close.shift(1))
        data["SMA_S"] = data.Close.rolling(self.SMA_S).mean()
        data["SMA_L"] = data.Close.rolling(self.SMA_L).mean()
        data.dropna(inplace = True)
        self.data2 = data
        
    def test_results(self):
        data = self.data2
        data["position"] = np.where(data["SMA_S"] > data["SMA_L"], 1, -1)
        data["strategy"] = data["position"].shift(1) * data["returns"]
        data.dropna(inplace=True)
        data["returnsbh"] = data.returns.cumsum().apply(np.exp)
        data["returnsstrategy"] = data.strategy.cumsum().apply(np.exp)
        perf = data.returnsstrategy[-1]
        outperf = perf - data["returnsbh"][-1]
        self.results = data
        ret = np.exp(data["strategy"].sum())
        std = (np.exp(data["strategy"]) - 1).std() * np.sqrt(252)
        print(round(perf,6), round(outperf,6)) 
        return (round(perf,6), round(outperf,6))
        
    def plot_results(self):
        if self.results is None:
            print("Run the test first")
        else:
            title = f"{self.symbol} | SMA_S = {self.SMA_S} | SMA_L={self.SMA_L}"
            self.results[["returnsbh","returnsstrategy"]].plot(title = title, figsize = (12,8))
