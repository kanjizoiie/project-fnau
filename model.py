import tensorflow as tf

train_datagen = tf.keras.preprocessing.image.ImageDataGenerator(
    rescale = 1./255,
    shear_range = 0.5,
    zoom_range = 0.4,
    horizontal_flip = True,
    rotation_range= 170)

test_datagen = tf.keras.preprocessing.image.ImageDataGenerator(
    rescale = 1./255)


training_set = train_datagen.flow_from_directory('training_set',
    target_size = (64, 64),
    batch_size = 32,
    class_mode = 'binary')

test_set = test_datagen.flow_from_directory('test_set',
    target_size = (64, 64),
    batch_size = 32,
    class_mode = 'binary')


class food_model:
    model = 0

    def __init__(self):
        self.model = tf.keras.models.Sequential();
    def create(self):
        self.model.add(tf.keras.layers.Conv2D(32, (3, 3), input_shape=(64, 64, 3))) # add a convolutional 2d layer to the self.model.
        self.model.add(tf.keras.layers.Activation('relu')) # set the activation to relu
        self.model.add(tf.keras.layers.MaxPooling2D(pool_size=(2, 2))) # create a pooling layer.

        self.model.add(tf.keras.layers.Conv2D(64, (3, 3)))
        self.model.add(tf.keras.layers.Activation('relu'))
        self.model.add(tf.keras.layers.MaxPooling2D(pool_size=(2, 2)))

        self.model.add(tf.keras.layers.Conv2D(64, (3, 3)))
        self.model.add(tf.keras.layers.Activation('relu'))
        self.model.add(tf.keras.layers.MaxPooling2D(pool_size=(2, 2)))

        # the self.model so far outputs 3D feature maps (height, width, features)

        self.model.add(tf.keras.layers.Flatten())  # this converts our 3D feature maps to 1D feature vectors
        self.model.add(tf.keras.layers.Dense(128))  #
        self.model.add(tf.keras.layers.Activation('relu'))
        self.model.add(tf.keras.layers.Dropout(0.5))
        self.model.add(tf.keras.layers.Dense(1))
        self.model.add(tf.keras.layers.Activation('sigmoid'))
    def compile(self):
        # COMPILE
        self.model.compile(loss='binary_crossentropy', optimizer='adam', metrics=['accuracy'])
    def get(self):
        return self.model

    def train(self):
        # TRAINING
        self.model.fit_generator(
            training_set,
            steps_per_epoch=100,
            epochs=40,
            validation_data=test_set,
            validation_steps=100)
    def save(self, name):
        self.model.save_weights(name)
    def load(self, name):
        self.model.load_weights(name)
    def predict(self, x):
        return self.model.predict(x)
    def classes(self):
        return training_set.class_indices;