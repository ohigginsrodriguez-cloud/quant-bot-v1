class TradingEngine:

    def __init__(self, strategy, executor):
        self.strategy = strategy
        self.executor = executor

    def run(self, data):
        signal = self.strategy.generate_signal(data)

        if signal is None:
            return None

        self.executor.execute(signal)
        return signal