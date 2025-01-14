import PyPDF2
import nltk
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
import os


def extraer_texto(pdf_path):
    with open(pdf_path, 'rb') as file:
        reader = PyPDF2.PdfReader(file) 
        text = ""
        for page in reader.pages:
            text += page.extract_text()
    return text


def preprocesar_texto(texto):
    # Tokenización en oraciones y palabras
    oraciones = sent_tokenize(texto)
    palabras = word_tokenize(texto)

    # Eliminar stopwords y puntuación
    stopwords_esp = set(stopwords.words('spanish'))
    palabras = [palabra.lower() for palabra in palabras if palabra.isalpha()]
    palabras = [palabra for palabra in palabras if palabra not in stopwords_esp]

    # Lematización
    lematizador = WordNetLemmatizer()
    palabras = [lematizador.lemmatize(palabra) for palabra in palabras]

    return palabras


def buscar_respuesta(pregunta, texto):
    # Preprocesar la pregunta
    palabras_pregunta = preprocesar_texto(pregunta)

    # Preprocesar el texto y obtener las oraciones
    palabras_texto = preprocesar_texto(texto)
    oraciones = sent_tokenize(texto)

    # Buscar las palabras clave en el texto
    palabras_clave = [
        palabra for palabra in palabras_pregunta if palabra in palabras_texto]

    # Construir la respuesta
    respuesta = "No se encontró respuesta."
    if palabras_clave:
        respuesta = "La respuesta es: "
        for palabra in palabras_clave:
            for i, oracion in enumerate(oraciones):
                if palabra in oracion:
                    respuesta += oracion
                    break

    return respuesta


# Ruta del archivo PDF
# pdf_path = "./redes_lan.pdf"

# Leer el PDF


def generar_pregunta(pregunta,path):
    texto = extraer_texto(path)
    respuesta = buscar_respuesta(pregunta, texto)
    return respuesta