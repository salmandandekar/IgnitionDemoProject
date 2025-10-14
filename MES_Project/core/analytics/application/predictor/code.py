
class Predictor(object):
    def anomaly_score(self, value): return min(1.0, abs(value-1.0))
