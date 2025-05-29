import os
import tensorflow as tf
import numpy as np
import json


class Chatbot:
    def __init__(self):
        # Directorio base
        base_dir = os.path.dirname(os.path.abspath(__file__))

        # Cargar modelo y recursos
        self.ruta_modelo = os.path.join(base_dir, "../saved_model/modelo.keras")
        self.ruta_vocabulario = os.path.join(base_dir, "../saved_model/vocabulary.txt")
        self.ruta_etiquetas = os.path.join(base_dir, "../saved_model/etiquetas.json")

        # Cargar el modelo
        self.model = tf.keras.models.load_model(self.ruta_modelo)

        # Cargar el vocabulario
        with open(self.ruta_vocabulario, "r", encoding="utf-8") as f:
            vocabulario = [line.strip() for line in f]
        self.tokenizer = tf.keras.layers.TextVectorization()
        self.tokenizer.set_vocabulary(vocabulario)

        # Cargar las etiquetas
        with open(self.ruta_etiquetas, "r", encoding="utf-8") as f:
            etiquetas = json.load(f)
        self.index_to_label = {v: k for k, v in etiquetas.items()}

    def predecir(self, texto: str) -> str:
        texto_vectorizado = self.tokenizer([texto])
        prediccion = self.model.predict(texto_vectorizado)
        indice = int(np.argmax(prediccion[0]))
        return self.index_to_label.get(indice, "NO ENTIENDO")
    
chatbot = Chatbot()

def realizar_prediccion(texto: str) -> str:
    return chatbot.predecir(texto)
