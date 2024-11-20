import tensorflow as tf
import os

def load_tflite_interpreter():
    # Get the current directory where this script is located
    current_directory = os.path.dirname(__file__)
    # Build the full path to the .tflite model file
    model_path = os.path.join(current_directory, 'ml_models', 'modelo1.tflite')
    # Create a TensorFlow Lite Interpreter object
    interpreter = tf.lite.Interpreter(model_path=model_path)
    # Allocate memory for the model
    interpreter.allocate_tensors()
    return interpreter

# Create a global interpreter object
interpreter = load_tflite_interpreter()
