import os
import numpy as np
from PIL import Image
import tensorflow as tf
import logging

# Configura el nivel de logging
logging.basicConfig(level=logging.INFO)

# Configura el intérprete de TensorFlow Lite
model_path = os.path.join(os.path.dirname(__file__), 'ml_models', 'modelo1.tflite')
logging.info(f"Model path: {model_path}")

interpreter = tf.lite.Interpreter(model_path=model_path)
interpreter.allocate_tensors()
input_details = interpreter.get_input_details()
output_details = interpreter.get_output_details()

logging.info(f"Input details: {input_details}")
logging.info(f"Output details: {output_details}")

# Función para preprocesar la imagen
def preprocess_image(image_path, input_shape):
    logging.info(f"Preprocessing image: {image_path}")
    image = Image.open(image_path).convert('RGB')  # Convertir a RGB si el modelo lo requiere
    image = image.resize((input_shape[1], input_shape[2]))  # Redimensionar al tamaño esperado
    image_array = np.array(image).astype('float32') / 255.0  # Normalizar a [0, 1]
    image_array = np.expand_dims(image_array, axis=0)  # Añadir una dimensión extra para el batch
    logging.info(f"Image shape after preprocessing: {image_array.shape}")
    return image_array

# Función para ejecutar la inferencia
def run_inference(image_path):
    logging.info(f"Running inference on image: {image_path}")
    input_shape = input_details[0]['shape']
    image_data = preprocess_image(image_path, input_shape)
    interpreter.set_tensor(input_details[0]['index'], image_data)
    interpreter.invoke()
    output_data = interpreter.get_tensor(output_details[0]['index'])
    logging.info(f"Inference output: {output_data}")
    return output_data

# Función para predecir la imagen
def predict_image(image_path):
    logging.info(f"Predicting image: {image_path}")
    output_data = run_inference(image_path)
    predicted_class = np.argmax(output_data[0])
    logging.info(f"Predicted class: {predicted_class}")
    return predicted_class, output_data
