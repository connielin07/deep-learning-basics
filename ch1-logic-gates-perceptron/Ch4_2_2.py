import numpy as np

class Perceptron:    
    def __init__(self, input_length, weights=None, bias=None):
        if weights is None:
            self.weights = np.ones(input_length) * 1
        else:
            self.weights = weights
        if bias is None:
            self.bias = -1
        else:
            self.bias = bias    
    
    @staticmethod    
    def activation_function(x):
        if x > 0:
            return 1
        return 0
        
    def __call__(self, input_data):
        w_input = self.weights * input_data
        w_sum = w_input.sum() + self.bias
        return Perceptron.activation_function(w_sum), w_sum

weights = np.array([1, 1])
bias = -1    
AND_Gate = Perceptron(2, weights, bias)

weights = np.array([-1, -1])
bias = 1.5 
NAND_Gate = Perceptron(2, weights, bias)

weights = np.array([1, 1])
bias = -0.5   
OR_Gate = Perceptron(2, weights, bias)

input_data = [np.array([0, 0]), np.array([0, 1]), 
              np.array([1, 0]), np.array([1, 1])]
for x in input_data:
    out1, w1 = OR_Gate(np.array(x))
    out2, w2 = NAND_Gate(np.array(x))
    new_point = np.array([w1, w2])
    new_input = np.array([out1, out2])
    out, w = AND_Gate(new_input)
    print(x, new_point, new_input, out)