import numpy as np
import os
import cv2
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Conv2D, MaxPooling2D, Flatten, Dense, Dropout
from sklearn.model_selection import train_test_split

# Ruta base de las carpetas de inspección
base_path = "C:\\ELVIS\\TmP"
# Ruta donde se guardarán los modelos
models_path = os.path.join(base_path, "002_Model")

# Crear la carpeta de modelos si no existe
if not os.path.exists(models_path):
    os.makedirs(models_path)

# Función para cargar imágenes desde las carpetas NG y OK
def load_images_from_folder(folder, label):
    images = []
    labels = []
    for filename in os.listdir(folder):
        img_path = os.path.join(folder, filename)
        if os.path.isfile(img_path):
            img = cv2.imread(img_path, cv2.IMREAD_GRAYSCALE)
            if img is not None:
                img = cv2.resize(img, (128, 128))  # Redimensionar las imágenes
                images.append(img)
                labels.append(label)
    return images, labels

# Función para preprocesar una imagen individual
def preprocess_image(image_path):
    img = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
    img = cv2.resize(img, (128, 128))  # Redimensionar a 128x128 píxeles
    img = img.reshape(1, 128, 128, 1)  # Añadir dimensiones para batch size y canal
    img = img / 255.0  # Normalizar
    return img

# Función para entrenar el modelo con las imágenes de una carpeta de inspección
def train_model_on_inspection_folder(inspection_folder):
    ok_folder = os.path.join(inspection_folder, 'OK')
    ng_folder = os.path.join(inspection_folder, 'NG')

    if not os.path.exists(ok_folder) or not os.path.exists(ng_folder):
        print(f"Skipping {inspection_folder}: OK or NG folder not found.")
        return

    good_images, good_labels = load_images_from_folder(ok_folder, 1)
    bad_images, bad_labels = load_images_from_folder(ng_folder, 0)

    images = np.array(good_images + bad_images)
    labels = np.array(good_labels + bad_labels)
    images = images.reshape(images.shape[0], 128, 128, 1)  # Añadir canal de color

    images = images / 255.0

    X_train, X_test, y_train, y_test = train_test_split(images, labels, test_size=0.2, random_state=42)

    model = Sequential([
        Conv2D(32, (3, 3), activation='relu', input_shape=(128, 128, 1)),
        MaxPooling2D((2, 2)),
        Conv2D(64, (3, 3), activation='relu'),
        MaxPooling2D((2, 2)),
        Flatten(),
        Dense(64, activation='relu'),
        Dropout(0.5),
        Dense(1, activation='sigmoid')
    ])

    model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])

    model.fit(X_train, y_train, epochs=10, validation_data=(X_test, y_test))

    loss, accuracy = model.evaluate(X_test, y_test)
    print(f'Inspection Folder: {inspection_folder} - Accuracy: {accuracy*100:.2f}%')

    # Guardar el modelo entrenado en formato nativo de Keras
    model_name = os.path.basename(inspection_folder)
    model.save(os.path.join(models_path, f'model_{model_name}.keras'))
    print(f'Model saved for {inspection_folder} as model_{model_name}.keras')

# Función para clasificar una imagen
def classify_image(image_path):
    img = preprocess_image(image_path)
    start_time = time.time()
    prediction = model.predict(img)
    end_time = time.time()
    prediction_label = 'Buena' if prediction[0][0] >= 0.5 else 'Mala'
    print(f'Predicción: {prediction_label}, Tiempo de Inferencia: {end_time - start_time:.4f} segundos')

# Iterar a través de cada carpeta de inspección
for inspection_folder in os.listdir(base_path):
    inspection_path = os.path.join(base_path, inspection_folder)
    if os.path.isdir(inspection_path):
        train_model_on_inspection_folder(inspection_path)

# Ejemplo de uso de clasificación
image_path = 'ruta_a_una_nueva_imagen.jpg'
classify_image(image_path)