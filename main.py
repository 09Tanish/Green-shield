from fastapi import FastAPI, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
import numpy as np
from io import BytesIO
from PIL import Image
import tensorflow as tf

# Initialize FastAPI App
app = FastAPI()

# Allow CORS for Frontend Access
origins = [
    "http://localhost",
    "http://localhost:5000",
    "http://127.0.0.1:5500"  # Ensure frontend can access the API
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Updated Model Path
MODEL_PATH = r"D:\11\code\plant project -1\saved_models\4"

# Load Model using TensorFlow SavedModel
MODEL = tf.saved_model.load(MODEL_PATH)

# Class Names
CLASS_NAMES = ["Early Blight", "Late Blight", "Healthy"]

@app.get("/ping")
async def ping():
    return {"message": "Hello, I am alive!"}

# Function to Process Image
def read_file_as_image(data) -> np.ndarray:
    image = Image.open(BytesIO(data))
    image = image.resize((256, 256))  # Ensure the image is 256x256
    image = np.array(image) / 255.0   # Normalize pixel values
    return image

@app.post("/predict")
async def predict(file: UploadFile = File(...)):
    try:
        image = read_file_as_image(await file.read())
        img_batch = np.expand_dims(image, axis=0)  # Add batch dimension
        img_batch = img_batch.astype(np.float32)   # Ensure float32

        # Use the model for prediction
        predictions = MODEL.signatures["serving_default"](tf.constant(img_batch))
        predictions = predictions['output_0'].numpy()  # Adjust based on model output
        
        predicted_class = CLASS_NAMES[np.argmax(predictions[0])]
        confidence = float(np.max(predictions[0]))

        return {
            "class": predicted_class,
            "confidence": confidence
        }
    except Exception as e:
        return {"error": str(e)}

if __name__ == "__main__":
    uvicorn.run(app, host="localhost", port=5000)