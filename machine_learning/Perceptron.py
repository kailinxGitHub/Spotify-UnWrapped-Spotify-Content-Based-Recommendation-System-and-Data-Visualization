import numpy as np

# the Perceptron class as a simple perceptron model
class Perceptron:
    def __init__(self, features, learning_rate=0.01, epochs=20):
        self.features = features
        self.learning_rate = learning_rate
        self.epochs = epochs
        self.weights = None
        self.bias = None

    # the fit method trains the model epoch times
    def fit(self, X, y):
        n_samples, n_features = X.shape
        self.weights = np.zeros(n_features)
        self.bias = 0

        for _ in range(self.epochs):
            for idx, x_i in enumerate(X):
                linear_output = np.dot(x_i, self.weights) + self.bias
                y_predicted = self._activation_function(linear_output)

                update = self.learning_rate * (y[idx] - y_predicted)
                self.weights += update * x_i
                self.bias += update

    # predicts the output based on the weights and bias
    def predict(self, X):
        linear_output = np.dot(X, self.weights) + self.bias
        y_predicted = self._activation_function(linear_output)
        return y_predicted

    # the activation function for the perceptron
    def _activation_function(self, x):
        return np.where(x >= 0, 1, 0)
    
    