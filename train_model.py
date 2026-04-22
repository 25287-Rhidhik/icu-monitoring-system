import numpy as np
import tensorflow as tf
from tensorflow import keras

# Generate better dataset
temps = np.random.uniform(25, 40, 2000)
hums = np.random.uniform(30, 90, 2000)

# Improved labels (more balanced)
y = np.where(
    (temps > 35) | (hums > 65),
    1,  # WARNING
    0   # SAFE
)

# Normalize
temp_norm = (temps - 25) / (40 - 25)
hum_norm = (hums - 30) / (90 - 30)

X = np.column_stack((temp_norm, hum_norm))

# Better model
model = keras.Sequential([
    keras.layers.Dense(16, activation='relu', input_shape=(2,)),
    keras.layers.Dense(8, activation='relu'),
    keras.layers.Dense(1, activation='sigmoid')
])

model.compile(
    optimizer='adam',
    loss='binary_crossentropy',
    metrics=['accuracy']
)

model.fit(X, y, epochs=50)

model.save("model.h5")

print("Model trained successfully")