import numpy as np


def sigmoid(x: np.ndarray) -> np.ndarray:
    return 1.0 / (1.0 + np.exp(-x))

def soft_label_to_target(label: int, output_nodes: int) -> np.ndarray:
    targets = np.ones(output_nodes, dtype=np.float64) * 0.01
    targets[label] = 0.99
    return targets

def scale_inputs(pixels_0_255: np.ndarray) -> np.ndarray:
    return (pixels_0_255 / 255.0 * 0.99) + 0.01

class NeuralNetwork:
    """
    3-layer fully-connected NN:
    input -> hidden -> output
    Activation: sigmoid
    Learning: gradient descent with backprop
    """
    def __init__(self, input_nodes: int, hidden_nodes: int, output_nodes: int, learning_rate: float, seed: int = 0):
        self.inodes = input_nodes
        self.hnodes = hidden_nodes
        self.onodes = output_nodes
        self.lr = learning_rate

        rng = np.random.default_rng(seed)

        self.wih = rng.normal(0.0, pow(self.inodes, -0.5), size=(self.hnodes, self.inodes))
        self.who = rng.normal(0.0, pow(self.hnodes, -0.5), size=(self.onodes, self.hnodes))

    def train(self, inputs: np.ndarray, targets: np.ndarray) -> None:
        inputs = inputs.reshape(-1, 1)
        targets = targets.reshape(-1, 1)

        hidden_inputs = self.wih @ inputs
        hidden_outputs = sigmoid(hidden_inputs)

        final_inputs = self.who @ hidden_outputs
        final_outputs = sigmoid(final_inputs)

        output_errors = targets - final_outputs
        hidden_errors = self.who.T @ output_errors

        self.who += self.lr * ((output_errors * final_outputs * (1.0 - final_outputs)) @ hidden_outputs.T)

        self.wih += self.lr * ((hidden_errors * hidden_outputs * (1.0 - hidden_outputs)) @ inputs.T)

    def query(self, inputs: np.ndarray) -> np.ndarray:
        inputs = inputs.reshape(-1, 1)

        hidden_inputs = self.wih @ inputs
        hidden_outputs = sigmoid(hidden_inputs)

        final_inputs = self.who @ hidden_outputs
        final_outputs = sigmoid(final_inputs)

        return final_outputs

    def save(self, path: str) -> None:
        np.savez(path, wih=self.wih, who=self.who, inodes=self.inodes, hnodes=self.hnodes, onodes=self.onodes, lr=self.lr)

    @staticmethod
    def load(path: str) -> "NeuralNetwork":
        data = np.load(path, allow_pickle=True)
        nn = NeuralNetwork(int(data["inodes"]), int(data["hnodes"]), int(data["onodes"]), float(data["lr"]))
        nn.wih = data["wih"]
        nn.who = data["who"]
        return nn


def load_mnist_csv_lines(csv_path: str):
    with open(csv_path, "r", encoding="utf-8") as f:
        return f.readlines()

def parse_mnist_csv_line(line: str, input_nodes: int, output_nodes: int):
    parts = line.strip().split(",")
    label = int(parts[0])
    pixels = np.array(parts[1:], dtype=np.float64)
    if pixels.size != input_nodes:
        raise ValueError(f"Expected {input_nodes} pixels, got {pixels.size}. Check your CSV format.")
    inputs = scale_inputs(pixels)
    targets = soft_label_to_target(label, output_nodes)
    return label, inputs, targets

def evaluate(nn: NeuralNetwork, test_lines, input_nodes: int, output_nodes: int, max_items: int | None = None) -> float:
    correct = 0
    total = 0

    for i, line in enumerate(test_lines):
        if max_items is not None and i >= max_items:
            break
        label, inputs, _targets = parse_mnist_csv_line(line, input_nodes, output_nodes)
        outputs = nn.query(inputs)
        predicted = int(np.argmax(outputs))
        total += 1
        if predicted == label:
            correct += 1

    return correct / total if total > 0 else 0.0

def main():

    input_nodes = 784
    hidden_nodes = 200
    output_nodes = 10
    learning_rate = 0.1
    epochs = 5

    train_path = "mnist_train.csv"
    test_path = "mnist_test.csv"

    print("Loading data...")
    train_lines = load_mnist_csv_lines(train_path)
    test_lines = load_mnist_csv_lines(test_path)

    nn = NeuralNetwork(input_nodes, hidden_nodes, output_nodes, learning_rate, seed=1)

    print(f"Training for {epochs} epochs...")
    for e in range(epochs):
        for line in train_lines:
            label, inputs, targets = parse_mnist_csv_line(line, input_nodes, output_nodes)
            nn.train(inputs, targets)

        acc = evaluate(nn, test_lines, input_nodes, output_nodes)
        print(f"Epoch {e+1}/{epochs} - Test Accuracy: {acc:.4f}")


    nn.save("mnist_nn_book_style_weights.npz")
    print("Saved weights to mnist_nn_book_style_weights.npz")


    sample_acc = evaluate(nn, test_lines, input_nodes, output_nodes, max_items=200)
    print(f"Quick check on first 200 test images: {sample_acc:.4f}")

if __name__ == "__main__":
    main()
