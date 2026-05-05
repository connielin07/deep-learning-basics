import numpy as np


class Perceptron:
    """
    Single-layer perceptron for learning a 2-input logic gate.

    This model uses:
    1. weights to represent the contribution of each input
    2. bias to adjust the decision threshold
    3. a step activation function to produce binary output
    """

    def __init__(self, input_length, weights=None, bias=None):
        """
        Initialize the perceptron.

        Parameters:
        - input_length: number of features in each input sample
        - weights: optional initial weights
        - bias: optional initial bias

        If no weights or bias are provided, they start from 0.
        """
        self.weights = np.zeros(input_length) if weights is None else weights
        self.bias = 0 if bias is None else bias

    @staticmethod
    def activation_function(x):
        """
        Step activation function.

        If the weighted sum is greater than or equal to 0,
        return 1; otherwise, return 0.

        This makes the perceptron suitable for binary classification,
        such as logic gate problems.
        """
        return 1 if x >= 0 else 0

    def __call__(self, input_data):
        """
        Compute the perceptron output for a given input.

        Steps:
        1. Calculate weighted sum = weights · inputs + bias
        2. Pass the result through the activation function
        3. Return the predicted class (0 or 1)
        """
        weighted_sum = np.dot(self.weights, input_data) + self.bias
        return Perceptron.activation_function(weighted_sum)

    def train(self, training_data, targets, learning_rate=0.1, epochs=100):
        """
        Train the perceptron using training samples and target outputs.

        Parameters:
        - training_data: all input combinations
        - targets: correct outputs for each input
        - learning_rate: step size for parameter updates
        - epochs: maximum number of passes through the dataset

        Perceptron update rule:
        error = target - prediction

        If prediction is incorrect:
        - update weights by: weights += learning_rate * error * x
        - update bias by: bias += learning_rate * error

        The training stops early if all samples are classified correctly.
        """
        for epoch in range(epochs):
            errors = 0  # Count how many samples are misclassified in this epoch

            for x, target in zip(training_data, targets):
                prediction = self(x)
                error = target - prediction

                # Only update parameters when the prediction is wrong
                if error != 0:
                    self.weights += learning_rate * error * x
                    self.bias += learning_rate * error
                    errors += 1

            # If no errors occur, the model has learned all training samples
            if errors == 0:
                print(f"Training converged at epoch {epoch + 1}")
                break
        else:
            # This runs only if the loop finishes without convergence
            print("Training did not converge")


# ---------------------------------------------------
# Prepare training data for the NOR logic gate
# ---------------------------------------------------
# Four possible input combinations for two binary inputs
training_inputs = np.array([
    [0, 0],
    [0, 1],
    [1, 0],
    [1, 1]
])

# NOR truth table:
# 0 NOR 0 = 1
# 0 NOR 1 = 0
# 1 NOR 0 = 0
# 1 NOR 1 = 0
targets = np.array([1, 0, 0, 0])

# Create a perceptron with 2 input features
NOR_Gate = Perceptron(2)

# Train the perceptron on NOR gate data
NOR_Gate.train(training_inputs, targets)

# Show the final weights and bias after learning
print("Final weights:", NOR_Gate.weights)
print("Final bias:", NOR_Gate.bias)

# ---------------------------------------------------
# Test the trained model on all input combinations
# ---------------------------------------------------
print("Prediction results:")
for x, expected in zip(training_inputs, targets):
    predicted = NOR_Gate(x)
    print(f"{x} -> Predicted: {predicted}, Expected: {expected}")