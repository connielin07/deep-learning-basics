import numpy as np


class Perceptron:
    """
    Single-layer perceptron for learning a 2-input logic gate.

    This model uses:
    1. weights to represent the importance of each input
    2. bias to shift the decision boundary
    3. a step activation function to output either 0 or 1
    """

    def __init__(self, input_length, weights=None, bias=None):
        """
        Initialize the perceptron.

        Parameters:
        - input_length: number of input features
        - weights: optional initial weights
        - bias: optional initial bias

        If weights and bias are not given, they are initialized to 0.
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
        Train the perceptron using the perceptron learning rule.

        Parameters:
        - training_data: input samples
        - targets: expected output values
        - learning_rate: controls update size
        - epochs: maximum number of training rounds

        Training rule:
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
# Prepare training data for the NAND logic gate
# ---------------------------------------------------
# Each row represents one input combination: [x1, x2]
training_inputs = np.array([
    [0, 0],
    [0, 1],
    [1, 0],
    [1, 1]
])

# NAND truth table:
# 0 NAND 0 = 1
# 0 NAND 1 = 1
# 1 NAND 0 = 1
# 1 NAND 1 = 0
targets = np.array([1, 1, 1, 0])

# Create a perceptron with 2 input nodes
NAND_Gate = Perceptron(2)

# Train the perceptron using the NAND training data
NAND_Gate.train(training_inputs, targets)

# Display the final learned parameters after training
print("Final weights:", NAND_Gate.weights)
print("Final bias:", NAND_Gate.bias)

# ---------------------------------------------------
# Verify whether the trained model predicts all
# input combinations correctly
# ---------------------------------------------------
print("Prediction results:")
for x, expected in zip(training_inputs, targets):
    predicted = NAND_Gate(x)
    print(f"{x} -> Predicted: {predicted}, Expected: {expected}")