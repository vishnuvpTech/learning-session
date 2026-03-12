# Python Backend Developer to AI/ML Engineer
## Complete Roadmap for Learning Artificial Intelligence and Machine Learning

**Version:** 1.0  
**Last Updated:** March 2026  
**Target Audience:** Python backend developers transitioning to AI/ML  
**Prerequisites:** Strong Python programming skills, backend development experience  

---

## Table of Contents

1. [Your Advantages as a Backend Developer](#advantages)
2. [AI/ML Learning Path Overview](#overview)
3. [Phase 1: Mathematics & Statistics Foundations](#phase-1)
4. [Phase 2: Machine Learning Basics](#phase-2)
5. [Phase 3: Deep Learning Fundamentals](#phase-3)
6. [Phase 4: Natural Language Processing](#phase-4)
7. [Phase 5: Computer Vision](#phase-5)
8. [Phase 6: MLOps & Production Deployment](#phase-6)
9. [Phase 7: Advanced Topics & LLMs](#phase-7)
10. [Practical Projects Portfolio](#projects)

---

<a name="phase-6"></a>
## 8. Phase 6: MLOps & Production Deployment

### 8.1 Model Serving with FastAPI

```python
# Deploy ML model as REST API using FastAPI
from fastapi import FastAPI, File, UploadFile, HTTPException
from pydantic import BaseModel
import tensorflow as tf
import numpy as np
from PIL import Image
import io
import joblib
from typing import List

app = FastAPI(title="ML Model API", version="1.0.0")

# Load models at startup
class ModelManager:
    def __init__(self):
        self.models = {}
    
    def load_models(self):
        """Load all models at application startup."""
        try:
            # Load image classification model
            self.models['image_classifier'] = tf.keras.models.load_model('models/image_classifier.h5')
            
            # Load text classification model
            self.models['text_classifier'] = joblib.load('models/text_classifier.pkl')
            self.models['vectorizer'] = joblib.load('models/vectorizer.pkl')
            
            print("Models loaded successfully")
        except Exception as e:
            print(f"Error loading models: {e}")
    
    def get_model(self, model_name):
        return self.models.get(model_name)

model_manager = ModelManager()

@app.on_event("startup")
async def startup_event():
    """Load models when app starts."""
    model_manager.load_models()

# Request/Response models
class TextRequest(BaseModel):
    text: str

class PredictionResponse(BaseModel):
    prediction: str
    confidence: float
    probabilities: dict

class ImagePredictionResponse(BaseModel):
    predictions: List[dict]
    processing_time: float

# Health check endpoint
@app.get("/health")
async def health_check():
    """Check if API is running."""
    return {"status": "healthy", "models_loaded": len(model_manager.models)}

# Text classification endpoint
@app.post("/predict/text", response_model=PredictionResponse)
async def predict_text(request: TextRequest):
    """
    Predict sentiment of text.
    """
    try:
        # Get model and vectorizer
        model = model_manager.get_model('text_classifier')
        vectorizer = model_manager.get_model('vectorizer')
        
        if not model or not vectorizer:
            raise HTTPException(status_code=500, detail="Model not loaded")
        
        # Preprocess
        text_vectorized = vectorizer.transform([request.text])
        
        # Predict
        prediction = model.predict(text_vectorized)[0]
        probabilities = model.predict_proba(text_vectorized)[0]
        
        # Format response
        classes = ['negative', 'positive']
        return PredictionResponse(
            prediction=classes[prediction],
            confidence=float(max(probabilities)),
            probabilities={
                classes[i]: float(prob) 
                for i, prob in enumerate(probabilities)
            }
        )
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Image classification endpoint
@app.post("/predict/image", response_model=ImagePredictionResponse)
async def predict_image(file: UploadFile = File(...)):
    """
    Classify uploaded image.
    """
    import time
    start_time = time.time()
    
    try:
        # Read and preprocess image
        image_data = await file.read()
        image = Image.open(io.BytesIO(image_data))
        image = image.resize((224, 224))
        image_array = np.array(image) / 255.0
        image_array = np.expand_dims(image_array, axis=0)
        
        # Get model
        model = model_manager.get_model('image_classifier')
        if not model:
            raise HTTPException(status_code=500, detail="Model not loaded")
        
        # Predict
        predictions = model.predict(image_array)[0]
        
        # Get top 5 predictions
        top_indices = np.argsort(predictions)[-5:][::-1]
        
        class_names = ['class_0', 'class_1', 'class_2', 'class_3', 'class_4',
                       'class_5', 'class_6', 'class_7', 'class_8', 'class_9']
        
        results = [
            {
                'class': class_names[idx],
                'confidence': float(predictions[idx])
            }
            for idx in top_indices
        ]
        
        processing_time = time.time() - start_time
        
        return ImagePredictionResponse(
            predictions=results,
            processing_time=processing_time
        )
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Batch prediction endpoint
class BatchTextRequest(BaseModel):
    texts: List[str]

@app.post("/predict/batch")
async def predict_batch(request: BatchTextRequest):
    """
    Batch prediction for multiple texts.
    """
    try:
        model = model_manager.get_model('text_classifier')
        vectorizer = model_manager.get_model('vectorizer')
        
        # Vectorize all texts
        texts_vectorized = vectorizer.transform(request.texts)
        
        # Predict
        predictions = model.predict(texts_vectorized)
        probabilities = model.predict_proba(texts_vectorized)
        
        # Format results
        classes = ['negative', 'positive']
        results = [
            {
                'text': text,
                'prediction': classes[pred],
                'confidence': float(max(prob))
            }
            for text, pred, prob in zip(request.texts, predictions, probabilities)
        ]
        
        return {'results': results, 'count': len(results)}
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Model metadata endpoint
@app.get("/models")
async def get_models():
    """
    Get information about loaded models.
    """
    return {
        'models': list(model_manager.models.keys()),
        'count': len(model_manager.models)
    }

# Run with: uvicorn app:app --reload
```

---

### 8.2 Docker Containerization

```dockerfile
# Dockerfile for ML API
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    libgomp1 \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Create directory for models
RUN mkdir -p models

# Expose port
EXPOSE 8000

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8000/health || exit 1

# Run application
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]
```

```yaml
# docker-compose.yml
version: '3.8'

services:
  ml-api:
    build: .
    ports:
      - "8000:8000"
    volumes:
      - ./models:/app/models
      - ./logs:/app/logs
    environment:
      - MODEL_PATH=/app/models
      - LOG_LEVEL=INFO
    restart: unless-stopped
    deploy:
      resources:
        limits:
          cpus: '2'
          memory: 4G
        reservations:
          cpus: '1'
          memory: 2G

  redis:
    image: redis:7-alpine
    ports:
      - "6379:6379"
    volumes:
      - redis-data:/data

  prometheus:
    image: prom/prometheus
    ports:
      - "9090:9090"
    volumes:
      - ./prometheus.yml:/etc/prometheus/prometheus.yml
      - prometheus-data:/prometheus

  grafana:
    image: grafana/grafana
    ports:
      - "3000:3000"
    volumes:
      - grafana-data:/var/lib/grafana
    environment:
      - GF_SECURITY_ADMIN_PASSWORD=admin

volumes:
  redis-data:
  prometheus-data:
  grafana-data:
```

```text
# requirements.txt
fastapi==0.109.0
uvicorn[standard]==0.27.0
pydantic==2.5.0
tensorflow==2.15.0
scikit-learn==1.4.0
numpy==1.26.0
pandas==2.1.0
pillow==10.2.0
python-multipart==0.0.6
joblib==1.3.2
redis==5.0.1
prometheus-client==0.19.0
```

---

### 8.3 Model Monitoring and Logging

```python
# monitoring.py - Add monitoring to ML API
from prometheus_client import Counter, Histogram, Gauge, make_asgi_app
from fastapi import FastAPI, Request
import time
import logging
from datetime import datetime

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('logs/ml_api.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# Prometheus metrics
prediction_counter = Counter(
    'ml_predictions_total',
    'Total number of predictions',
    ['model', 'endpoint']
)

prediction_latency = Histogram(
    'ml_prediction_latency_seconds',
    'Prediction latency in seconds',
    ['model', 'endpoint']
)

model_accuracy = Gauge(
    'ml_model_accuracy',
    'Current model accuracy',
    ['model']
)

error_counter = Counter(
    'ml_errors_total',
    'Total number of errors',
    ['model', 'error_type']
)

class MonitoringMiddleware:
    """Middleware to track API metrics."""
    
    def __init__(self, app):
        self.app = app
    
    async def __call__(self, scope, receive, send):
        if scope['type'] != 'http':
            return await self.app(scope, receive, send)
        
        start_time = time.time()
        
        # Log request
        logger.info(f"Request: {scope['method']} {scope['path']}")
        
        async def send_wrapper(message):
            if message['type'] == 'http.response.start':
                duration = time.time() - start_time
                
                # Record metrics
                endpoint = scope['path']
                if 'predict' in endpoint:
                    prediction_latency.labels(
                        model='default',
                        endpoint=endpoint
                    ).observe(duration)
                    
                    prediction_counter.labels(
                        model='default',
                        endpoint=endpoint
                    ).inc()
                
                # Log response
                logger.info(
                    f"Response: {message.get('status', 0)} "
                    f"in {duration:.3f}s"
                )
            
            await send(message)
        
        await self.app(scope, receive, send_wrapper)

# Add to FastAPI app
from fastapi import FastAPI

app = FastAPI()
app.add_middleware(MonitoringMiddleware)

# Mount Prometheus metrics endpoint
metrics_app = make_asgi_app()
app.mount("/metrics", metrics_app)

# Data drift detection
import numpy as np
from scipy import stats

class DataDriftDetector:
    """Detect distribution shifts in input data."""
    
    def __init__(self, reference_data):
        self.reference_data = reference_data
        self.reference_mean = np.mean(reference_data, axis=0)
        self.reference_std = np.std(reference_data, axis=0)
    
    def detect_drift(self, new_data, threshold=0.05):
        """
        Detect if new data has drifted from reference distribution.
        Uses Kolmogorov-Smirnov test.
        """
        drifted_features = []
        
        for i in range(new_data.shape[1]):
            # Perform KS test
            statistic, p_value = stats.ks_2samp(
                self.reference_data[:, i],
                new_data[:, i]
            )
            
            if p_value < threshold:
                drifted_features.append({
                    'feature_index': i,
                    'p_value': p_value,
                    'drift_detected': True
                })
        
        return drifted_features
    
    def get_statistics(self, new_data):
        """Get distribution statistics."""
        new_mean = np.mean(new_data, axis=0)
        new_std = np.std(new_data, axis=0)
        
        mean_shift = np.abs(new_mean - self.reference_mean)
        std_shift = np.abs(new_std - self.reference_std)
        
        return {
            'mean_shift': mean_shift.tolist(),
            'std_shift': std_shift.tolist()
        }

# Model performance tracking
class PerformanceTracker:
    """Track model performance over time."""
    
    def __init__(self):
        self.predictions = []
        self.ground_truth = []
        self.timestamps = []
    
    def add_prediction(self, prediction, ground_truth=None):
        """Add prediction to tracking."""
        self.predictions.append(prediction)
        if ground_truth is not None:
            self.ground_truth.append(ground_truth)
        self.timestamps.append(datetime.now())
    
    def calculate_accuracy(self, window_size=100):
        """Calculate accuracy over recent predictions."""
        if len(self.ground_truth) < window_size:
            return None
        
        recent_preds = self.predictions[-window_size:]
        recent_truth = self.ground_truth[-window_size:]
        
        accuracy = np.mean(np.array(recent_preds) == np.array(recent_truth))
        
        # Update Prometheus metric
        model_accuracy.labels(model='default').set(accuracy)
        
        return accuracy
    
    def get_metrics(self):
        """Get comprehensive metrics."""
        from sklearn.metrics import precision_score, recall_score, f1_score
        
        if not self.ground_truth:
            return None
        
        return {
            'accuracy': np.mean(
                np.array(self.predictions) == np.array(self.ground_truth)
            ),
            'precision': precision_score(
                self.ground_truth, 
                self.predictions, 
                average='weighted'
            ),
            'recall': recall_score(
                self.ground_truth, 
                self.predictions, 
                average='weighted'
            ),
            'f1': f1_score(
                self.ground_truth, 
                self.predictions, 
                average='weighted'
            ),
            'total_predictions': len(self.predictions)
        }

# Add endpoint to get monitoring metrics
@app.get("/monitoring/metrics")
async def get_monitoring_metrics():
    """Get current monitoring metrics."""
    tracker = PerformanceTracker()
    metrics = tracker.get_metrics()
    
    return {
        'timestamp': datetime.now().isoformat(),
        'metrics': metrics
    }
```

---

### 8.4 Model Versioning with MLflow

```python
# mlflow_example.py
import mlflow
import mlflow.sklearn
import mlflow.tensorflow
from sklearn.ensemble import RandomForestClassifier
from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, f1_score
import numpy as np

# Setup MLflow
mlflow.set_tracking_uri("http://localhost:5000")
mlflow.set_experiment("iris_classification")

# Load data
iris = load_iris()
X_train, X_test, y_train, y_test = train_test_split(
    iris.data, iris.target, test_size=0.2, random_state=42
)

# Train and log model
with mlflow.start_run(run_name="random_forest_v1"):
    # Log parameters
    params = {
        'n_estimators': 100,
        'max_depth': 10,
        'min_samples_split': 2,
        'random_state': 42
    }
    mlflow.log_params(params)
    
    # Train model
    model = RandomForestClassifier(**params)
    model.fit(X_train, y_train)
    
    # Evaluate
    y_pred = model.predict(X_test)
    accuracy = accuracy_score(y_test, y_pred)
    f1 = f1_score(y_test, y_pred, average='weighted')
    
    # Log metrics
    mlflow.log_metric("accuracy", accuracy)
    mlflow.log_metric("f1_score", f1)
    
    # Log model
    mlflow.sklearn.log_model(model, "model")
    
    # Log additional artifacts
    import matplotlib.pyplot as plt
    from sklearn.metrics import confusion_matrix
    import seaborn as sns
    
    cm = confusion_matrix(y_test, y_pred)
    plt.figure(figsize=(8, 6))
    sns.heatmap(cm, annot=True, fmt='d', cmap='Blues')
    plt.title('Confusion Matrix')
    plt.ylabel('True Label')
    plt.xlabel('Predicted Label')
    plt.savefig('confusion_matrix.png')
    mlflow.log_artifact('confusion_matrix.png')
    
    print(f"Model logged with accuracy: {accuracy:.4f}")

# Load model from MLflow
def load_model_from_mlflow(run_id):
    """Load model from MLflow registry."""
    model_uri = f"runs:/{run_id}/model"
    loaded_model = mlflow.sklearn.load_model(model_uri)
    return loaded_model

# Register model
def register_model(run_id, model_name="iris_classifier"):
    """Register model in MLflow Model Registry."""
    model_uri = f"runs:/{run_id}/model"
    mlflow.register_model(model_uri, model_name)

# Transition model to production
def promote_model_to_production(model_name, version):
    """Promote model version to production."""
    client = mlflow.tracking.MlflowClient()
    client.transition_model_version_stage(
        name=model_name,
        version=version,
        stage="Production"
    )

# Load production model
def load_production_model(model_name="iris_classifier"):
    """Load current production model."""
    model_uri = f"models:/{model_name}/Production"
    return mlflow.sklearn.load_model(model_uri)

# Compare models
def compare_model_runs(experiment_name="iris_classification"):
    """Compare all runs in an experiment."""
    experiment = mlflow.get_experiment_by_name(experiment_name)
    runs = mlflow.search_runs(experiment_ids=[experiment.experiment_id])
    
    # Sort by accuracy
    runs_sorted = runs.sort_values('metrics.accuracy', ascending=False)
    
    print("Top 5 Models by Accuracy:")
    print(runs_sorted[['run_id', 'metrics.accuracy', 'metrics.f1_score']].head())
    
    return runs_sorted
```

---

### 8.5 CI/CD for ML Models

```yaml
# .github/workflows/ml_pipeline.yml
name: ML Model CI/CD

on:
  push:
    branches: [ main ]
  pull_request:
    branches: [ main ]

jobs:
  test:
    runs-on: ubuntu-latest
    
    steps:
    - uses: actions/checkout@v3
    
    - name: Set up Python
      uses: actions/setup-python@v4
      with:
        python-version: '3.11'
    
    - name: Install dependencies
      run: |
        pip install -r requirements.txt
        pip install pytest pytest-cov
    
    - name: Run tests
      run: |
        pytest tests/ --cov=src --cov-report=xml
    
    - name: Upload coverage
      uses: codecov/codecov-action@v3

  train:
    needs: test
    runs-on: ubuntu-latest
    
    steps:
    - uses: actions/checkout@v3
    
    - name: Set up Python
      uses: actions/setup-python@v4
      with:
        python-version: '3.11'
    
    - name: Install dependencies
      run: pip install -r requirements.txt
    
    - name: Train model
      run: python scripts/train_model.py
    
    - name: Evaluate model
      run: python scripts/evaluate_model.py
    
    - name: Upload model artifact
      uses: actions/upload-artifact@v3
      with:
        name: trained-model
        path: models/

  deploy:
    needs: train
    runs-on: ubuntu-latest
    if: github.ref == 'refs/heads/main'
    
    steps:
    - uses: actions/checkout@v3
    
    - name: Download model artifact
      uses: actions/download-artifact@v3
      with:
        name: trained-model
        path: models/
    
    - name: Build Docker image
      run: |
        docker build -t ml-api:latest .
    
    - name: Push to registry
      run: |
        echo ${{ secrets.DOCKER_PASSWORD }} | docker login -u ${{ secrets.DOCKER_USERNAME }} --password-stdin
        docker tag ml-api:latest ${{ secrets.DOCKER_USERNAME }}/ml-api:latest
        docker push ${{ secrets.DOCKER_USERNAME }}/ml-api:latest
    
    - name: Deploy to production
      run: |
        # Deploy to cloud service (AWS, GCP, Azure)
        echo "Deploying to production..."
```

---

<a name="phase-7"></a>
## 9. Phase 7: Advanced Topics & LLMs

### 9.1 Fine-tuning Large Language Models

```python
# Fine-tune a pre-trained model on custom data
from transformers import (
    AutoTokenizer, 
    AutoModelForSequenceClassification,
    TrainingArguments, 
    Trainer
)
from datasets import load_dataset, Dataset
import torch
import pandas as pd

# Prepare custom dataset
def prepare_dataset(texts, labels):
    """Prepare dataset for fine-tuning."""
    data = {
        'text': texts,
        'label': labels
    }
    return Dataset.from_dict(data)

# Load pre-trained model and tokenizer
model_name = "distilbert-base-uncased"
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForSequenceClassification.from_pretrained(
    model_name, 
    num_labels=2
)

# Tokenize function
def tokenize_function(examples):
    return tokenizer(
        examples['text'],
        padding='max_length',
        truncation=True,
        max_length=512
    )

# Prepare data
texts = [
    "This product is amazing!",
    "Terrible experience, not recommended.",
    "Pretty good, would buy again.",
    "Worst purchase ever."
]
labels = [1, 0, 1, 0]  # 1 = positive, 0 = negative

dataset = prepare_dataset(texts, labels)
tokenized_dataset = dataset.map(tokenize_function, batched=True)

# Split dataset
train_test_split = tokenized_dataset.train_test_split(test_size=0.2)
train_dataset = train_test_split['train']
eval_dataset = train_test_split['test']

# Training arguments
training_args = TrainingArguments(
    output_dir='./results',
    num_train_epochs=3,
    per_device_train_batch_size=8,
    per_device_eval_batch_size=8,
    warmup_steps=500,
    weight_decay=0.01,
    logging_dir='./logs',
    logging_steps=10,
    evaluation_strategy="epoch",
    save_strategy="epoch",
    load_best_model_at_end=True,
)

# Compute metrics
from sklearn.metrics import accuracy_score, precision_recall_fscore_support

def compute_metrics(pred):
    labels = pred.label_ids
    preds = pred.predictions.argmax(-1)
    precision, recall, f1, _ = precision_recall_fscore_support(
        labels, preds, average='weighted'
    )
    acc = accuracy_score(labels, preds)
    return {
        'accuracy': acc,
        'f1': f1,
        'precision': precision,
        'recall': recall
    }

# Create Trainer
trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=train_dataset,
    eval_dataset=eval_dataset,
    compute_metrics=compute_metrics
)

# Train model
trainer.train()

# Evaluate
results = trainer.evaluate()
print(f"Evaluation results: {results}")

# Save fine-tuned model
model.save_pretrained('./fine_tuned_model')
tokenizer.save_pretrained('./fine_tuned_model')

# Use fine-tuned model
def predict_with_finetuned_model(text):
    """Make prediction with fine-tuned model."""
    inputs = tokenizer(text, return_tensors='pt', truncation=True, max_length=512)
    outputs = model(**inputs)
    predictions = torch.nn.functional.softmax(outputs.logits, dim=-1)
    predicted_class = predictions.argmax().item()
    confidence = predictions[0][predicted_class].item()
    
    return {
        'class': 'positive' if predicted_class == 1 else 'negative',
        'confidence': confidence
    }

# Test
result = predict_with_finetuned_model("This is absolutely fantastic!")
print(result)
```

---

### 9.2 Prompt Engineering & LangChain

```python
# Advanced prompt engineering with LangChain
from langchain import PromptTemplate, LLMChain
from langchain.llms import OpenAI
from langchain.chat_models import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from langchain.schema import HumanMessage, SystemMessage, AIMessage

# Initialize LLM (requires API key)
llm = ChatOpenAI(temperature=0.7, model_name="gpt-3.5-turbo")

# Simple prompt template
template = """
You are a helpful AI assistant that answers questions about {topic}.

Question: {question}

Answer: Let me help you with that.
"""

prompt = PromptTemplate(
    input_variables=["topic", "question"],
    template=template
)

chain = LLMChain(llm=llm, prompt=prompt)

# Use chain
result = chain.run(topic="machine learning", question="What is a neural network?")
print(result)

# Few-shot prompting
few_shot_template = """
You are an expert at classifying text sentiment.

Examples:
Text: "I love this product!"
Sentiment: Positive

Text: "This is terrible."
Sentiment: Negative

Text: "It's okay, nothing special."
Sentiment: Neutral

Now classify:
Text: "{text}"
Sentiment:
"""

few_shot_prompt = PromptTemplate(
    input_variables=["text"],
    template=few_shot_template
)

chain = LLMChain(llm=llm, prompt=few_shot_prompt)
result = chain.run(text="This exceeded my expectations!")
print(f"Sentiment: {result}")

# Chain of Thought prompting
cot_template = """
Solve this problem step by step:

Problem: {problem}

Let's think through this:
1. First, let me understand what we're looking for
2. Then, I'll break down the problem
3. Finally, I'll provide the solution

Solution:
"""

cot_prompt = PromptTemplate(
    input_variables=["problem"],
    template=cot_template
)

# Multi-step chains
from langchain.chains import SimpleSequentialChain

# Step 1: Generate title
title_chain = LLMChain(
    llm=llm,
    prompt=PromptTemplate(
        input_variables=["topic"],
        template="Generate a catchy blog post title about {topic}:"
    )
)

# Step 2: Generate outline
outline_chain = LLMChain(
    llm=llm,
    prompt=PromptTemplate(
        input_variables=["title"],
        template="Create a detailed outline for this blog post: {title}"
    )
)

# Combine chains
overall_chain = SimpleSequentialChain(
    chains=[title_chain, outline_chain],
    verbose=True
)

result = overall_chain.run("artificial intelligence")
print(result)

# Memory in conversations
from langchain.memory import ConversationBufferMemory
from langchain.chains import ConversationChain

memory = ConversationBufferMemory()
conversation = ConversationChain(
    llm=llm,
    memory=memory,
    verbose=True
)

# Multi-turn conversation
response1 = conversation.predict(input="Hi, my name is Alice")
print(response1)

response2 = conversation.predict(input="What's my name?")
print(response2)  # Should remember "Alice"

# Document Q&A with embeddings
from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import FAISS
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.chains import RetrievalQA

# Load and split documents
documents = [
    "Machine learning is a subset of AI.",
    "Deep learning uses neural networks with multiple layers.",
    "Natural language processing deals with text data.",
    "Computer vision focuses on image understanding."
]

text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=100,
    chunk_overlap=20
)

# Create embeddings and vector store
embeddings = OpenAIEmbeddings()
vectorstore = FAISS.from_texts(documents, embeddings)

# Create retrieval chain
qa_chain = RetrievalQA.from_chain_type(
    llm=llm,
    chain_type="stuff",
    retriever=vectorstore.as_retriever()
)

# Ask questions
question = "What is deep learning?"
answer = qa_chain.run(question)
print(f"Q: {question}")
print(f"A: {answer}")
```

---

### 9.3 RAG (Retrieval Augmented Generation)

```python
# Build a RAG system from scratch
from sentence_transformers import SentenceTransformer
import numpy as np
import faiss

class RAGSystem:
    """Retrieval Augmented Generation system."""
    
    def __init__(self, embedding_model_name='all-MiniLM-L6-v2'):
        self.embedding_model = SentenceTransformer(embedding_model_name)
        self.documents = []
        self.embeddings = None
        self.index = None
    
    def add_documents(self, documents):
        """Add documents to the knowledge base."""
        self.documents.extend(documents)
        
        # Generate embeddings
        new_embeddings = self.embedding_model.encode(documents)
        
        if self.embeddings is None:
            self.embeddings = new_embeddings
        else:
            self.embeddings = np.vstack([self.embeddings, new_embeddings])
        
        # Build FAISS index
        self.build_index()
    
    def build_index(self):
        """Build FAISS index for fast similarity search."""
        dimension = self.embeddings.shape[1]
        self.index = faiss.IndexFlatL2(dimension)
        self.index.add(self.embeddings.astype('float32'))
    
    def retrieve(self, query, top_k=3):
        """Retrieve most relevant documents."""
        # Encode query
        query_embedding = self.embedding_model.encode([query])
        
        # Search
        distances, indices = self.index.search(
            query_embedding.astype('float32'), 
            top_k
        )
        
        # Get documents
        retrieved_docs = [self.documents[idx] for idx in indices[0]]
        
        return retrieved_docs, distances[0]
    
    def generate_answer(self, query, retrieved_docs):
        """Generate answer using retrieved context."""
        # Combine retrieved documents
        context = "\n".join(retrieved_docs)
        
        # Create prompt
        prompt = f"""
        Based on the following context, answer the question.
        
        Context:
        {context}
        
        Question: {query}
        
        Answer:
        """
        
        # Use LLM to generate answer
        # (This would use OpenAI API or similar)
        return prompt  # Return prompt for now
    
    def query(self, query, top_k=3):
        """End-to-end RAG query."""
        # Retrieve relevant documents
        retrieved_docs, distances = self.retrieve(query, top_k)
        
        # Generate answer
        answer_prompt = self.generate_answer(query, retrieved_docs)
        
        return {
            'retrieved_docs': retrieved_docs,
            'distances': distances.tolist(),
            'answer_prompt': answer_prompt
        }

# Example usage
rag = RAGSystem()

# Add knowledge base
documents = [
    "Python is a high-level programming language created by Guido van Rossum.",
    "Machine learning is a subset of artificial intelligence.",
    "TensorFlow and PyTorch are popular deep learning frameworks.",
    "Natural language processing deals with understanding human language.",
    "Computer vision enables computers to understand images and videos.",
    "Neural networks are inspired by biological neural networks in the brain.",
    "Supervised learning uses labeled data for training.",
    "Unsupervised learning finds patterns in unlabeled data.",
    "Reinforcement learning learns through interaction with an environment.",
    "Transfer learning uses pre-trained models for new tasks."
]

rag.add_documents(documents)

# Query the system
result = rag.query("What is machine learning?")

print("Retrieved Documents:")
for i, (doc, dist) in enumerate(zip(result['retrieved_docs'], result['distances']), 1):
    print(f"{i}. {doc} (distance: {dist:.4f})")

print(f"\nGenerated Prompt:\n{result['answer_prompt']}")

# Advanced RAG with metadata filtering
class AdvancedRAG(RAGSystem):
    """RAG with metadata support."""
    
    def __init__(self, embedding_model_name='all-MiniLM-L6-v2'):
        super().__init__(embedding_model_name)
        self.metadata = []
    
    def add_documents_with_metadata(self, documents, metadata_list):
        """Add documents with metadata."""
        self.add_documents(documents)
        self.metadata.extend(metadata_list)
    
    def retrieve_with_filter(self, query, metadata_filter, top_k=3):
        """Retrieve documents with metadata filtering."""
        # First, filter by metadata
        filtered_indices = [
            i for i, meta in enumerate(self.metadata)
            if all(meta.get(k) == v for k, v in metadata_filter.items())
        ]
        
        if not filtered_indices:
            return [], []
        
        # Get embeddings for filtered documents
        filtered_embeddings = self.embeddings[filtered_indices]
        
        # Search in filtered embeddings
        query_embedding = self.embedding_model.encode([query])
        
        # Calculate distances manually
        distances = np.linalg.norm(
            filtered_embeddings - query_embedding, 
            axis=1
        )
        
        # Get top k
        top_indices = np.argsort(distances)[:top_k]
        
        retrieved_docs = [self.documents[filtered_indices[i]] for i in top_indices]
        retrieved_distances = distances[top_indices]
        
        return retrieved_docs, retrieved_distances

# Example with metadata
advanced_rag = AdvancedRAG()

docs_with_meta = [
    ("Python is great for ML", {"topic": "programming", "difficulty": "beginner"}),
    ("Neural networks are complex", {"topic": "ml", "difficulty": "advanced"}),
    ("Variables store data", {"topic": "programming", "difficulty": "beginner"}),
]

docs, metadata = zip(*docs_with_meta)
advanced_rag.add_documents_with_metadata(list(docs), list(metadata))

# Query with filter
results = advanced_rag.retrieve_with_filter(
    "How do I start?",
    metadata_filter={"difficulty": "beginner"},
    top_k=2
)
print("Filtered results:", results[0])
```

---

### 9.4 AI Agents with LangChain

```python
# Build autonomous AI agents
from langchain.agents import Tool, AgentExecutor, LLMSingleActionAgent
from langchain.prompts import StringPromptTemplate
from langchain import LLMChain
from typing import List
import re

# Define tools for the agent
def search_wikipedia(query):
    """Search Wikipedia for information."""
    # Simplified - would use actual Wikipedia API
    return f"Wikipedia search results for: {query}"

def calculate(expression):
    """Perform mathematical calculations."""
    try:
        result = eval(expression)
        return f"The answer is {result}"
    except:
        return "Invalid expression"

def get_current_time():
    """Get current time."""
    from datetime import datetime
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

# Create tools
tools = [
    Tool(
        name="Wikipedia Search",
        func=search_wikipedia,
        description="Useful for searching factual information"
    ),
    Tool(
        name="Calculator",
        func=calculate,
        description="Useful for mathematical calculations"
    ),
    Tool(
        name="Time",
        func=get_current_time,
        description="Get the current date and time"
    )
]

# Custom prompt template
template = """
You are an AI assistant with access to the following tools:

{tools}

Use this format:

Question: the input question
Thought: think about what to do
Action: the action to take (must be one of [{tool_names}])
Action Input: the input to the action
Observation: the result of the action
... (repeat Thought/Action/Action Input/Observation as needed)
Thought: I now know the final answer
Final Answer: the final answer to the original question

Question: {input}
{agent_scratchpad}
"""

class CustomPromptTemplate(StringPromptTemplate):
    template: str
    tools: List[Tool]
    
    def format(self, **kwargs) -> str:
        intermediate_steps = kwargs.pop("intermediate_steps")
        thoughts = ""
        
        for action, observation in intermediate_steps:
            thoughts += f"\nThought: {action.log}"
            thoughts += f"\nObservation: {observation}"
        
        kwargs["agent_scratchpad"] = thoughts
        kwargs["tools"] = "\n".join([f"{tool.name}: {tool.description}" for tool in self.tools])
        kwargs["tool_names"] = ", ".join([tool.name for tool in self.tools])
        
        return self.template.format(**kwargs)

# Multi-agent system
class MultiAgentSystem:
    """System with multiple specialized agents."""
    
    def __init__(self):
        self.agents = {}
    
    def add_agent(self, name, agent):
        """Add an agent to the system."""
        self.agents[name] = agent
    
    def route_query(self, query):
        """Route query to appropriate agent."""
        # Simple routing logic
        if "calculate" in query.lower() or any(op in query for op in ['+', '-', '*', '/']):
            return "math_agent"
        elif "search" in query.lower() or "what is" in query.lower():
            return "search_agent"
        else:
            return "general_agent"
    
    def process_query(self, query):
        """Process query with appropriate agent."""
        agent_name = self.route_query(query)
        
        if agent_name in self.agents:
            return self.agents[agent_name].run(query)
        else:
            return "No suitable agent found"

# Example specialized agents
class MathAgent:
    def run(self, query):
        # Extract numbers and operation
        # Perform calculation
        return "Math result"

class SearchAgent:
    def run(self, query):
        # Perform search
        return "Search results"

# Initialize multi-agent system
multi_agent_system = MultiAgentSystem()
multi_agent_system.add_agent("math_agent", MathAgent())
multi_agent_system.add_agent("search_agent", SearchAgent())

# Process queries
result = multi_agent_system.process_query("Calculate 25 * 4")
print(result)
```

---

<a name="projects"></a>
## 10. Practical Projects Portfolio

### Project 1: Sentiment Analysis API
**Skills:** Machine Learning, NLP, FastAPI, Docker

**Description:** Build a REST API that analyzes sentiment of text/reviews.

**Tech Stack:**
- scikit-learn for model training
- FastAPI for API
- Docker for deployment
- Redis for caching

**Features:**
- Text sentiment classification (positive/negative/neutral)
- Batch processing
- Model versioning
- Performance monitoring

**Deliverables:**
- Trained model with >85% accuracy
- REST API with documentation
- Docker container
- GitHub repository

---

### Project 2: Image Classification System
**Skills:** Deep Learning, Computer Vision, TensorFlow

**Description:** Build an image classifier for custom categories.

**Tech Stack:**
- TensorFlow/Keras
- Transfer learning (ResNet50)
- FastAPI
- MLflow for tracking

**Features:**
- Multi-class image classification
- Data augmentation
- Model fine-tuning
- Confidence scores

**Deliverables:**
- Trained CNN model
- Web interface for upload
- Model comparison report
- Deployment guide

---

### Project 3: Chatbot with RAG
**Skills:** NLP, LLMs, Vector Databases

**Description:** Build an intelligent chatbot using RAG architecture.

**Tech Stack:**
- LangChain
- OpenAI/Hugging Face models
- FAISS vector store
- FastAPI

**Features:**
- Context-aware responses
- Document retrieval
- Conversation memory
- Multi-turn dialogue

**Deliverables:**
- Working chatbot
- Knowledge base integration
- API documentation
- Usage examples

---

### Project 4: Recommendation System
**Skills:** Machine Learning, Collaborative Filtering

**Description:** Build a product/movie recommendation engine.

**Tech Stack:**
- scikit-learn
- Surprise library
- FastAPI
- PostgreSQL

**Features:**
- Collaborative filtering
- Content-based filtering
- Hybrid recommendations
- Cold start handling

**Deliverables:**
- Recommendation API
- Evaluation metrics
- User interface
- Performance benchmarks

---

### Project 5: Object Detection App
**Skills:** Computer Vision, Deep Learning

**Description:** Real-time object detection in images/videos.

**Tech Stack:**
- YOLOv5/YOLOv8
- PyTorch
- OpenCV
- FastAPI

**Features:**
- Multiple object detection
- Bounding box visualization
- Custom object training
- Video processing

**Deliverables:**
- Trained detector
- Web demo
- Mobile app (optional)
- Documentation

---

### Project 6: Time Series Forecasting
**Skills:** Machine Learning, LSTM, Time Series

**Description:** Predict future values from historical data.

**Tech Stack:**
- TensorFlow
- LSTM/GRU
- Prophet
- Plotly for visualization

**Features:**
- Multiple forecasting models
- Confidence intervals
- Interactive visualizations
- API endpoints

**Deliverables:**
- Forecasting models
- Comparison dashboard
- API documentation
- Performance analysis

---

### Project 7: Text Summarization Tool
**Skills:** NLP, Transformers

**Description:** Automatic text summarization using transformer models.

**Tech Stack:**
- Hugging Face Transformers
- BART/T5 models
- FastAPI
- Streamlit for UI

**Features:**
- Extractive summarization
- Abstractive summarization
- Multi-document summarization
- Customizable length

**Deliverables:**
- Summarization API
- Web interface
- Model comparison
- Documentation

---

### Project 8: Anomaly Detection System
**Skills:** Machine Learning, Unsupervised Learning

**Description:** Detect anomalies in system logs/metrics.

**Tech Stack:**
- Isolation Forest
- Autoencoder
- Prometheus
- Grafana

**Features:**
- Real-time detection
- Multiple algorithms
- Alert system
- Dashboard visualization

**Deliverables:**
- Detection pipeline
- Monitoring dashboard
- Alert configuration
- Documentation

---

### Project 9: Speech Recognition App
**Skills:** Deep Learning, Audio Processing

**Description:** Convert speech to text using deep learning.

**Tech Stack:**
- Whisper (OpenAI)
- PyTorch
- Librosa
- FastAPI

**Features:**
- Multi-language support
- Real-time transcription
- Speaker diarization
- Punctuation restoration

**Deliverables:**
- Transcription API
- Web interface
- Performance metrics
- Documentation

---

### Project 10: End-to-End ML Pipeline
**Skills:** MLOps, Full Stack ML

**Description:** Complete ML system from data to deployment.

**Tech Stack:**
- Apache Airflow
- MLflow
- Docker/Kubernetes
- Monitoring tools

**Features:**
- Automated data pipeline
- Model training orchestration
- A/B testing
- Monitoring and alerts

**Deliverables:**
- Complete ML pipeline
- CI/CD setup
- Documentation
- Production deployment

---

<a name="tools"></a>
## 11. Tools & Libraries Ecosystem

### Core ML Libraries

**Data Manipulation:**
```
NumPy - Numerical computing
Pandas - Data analysis
Polars - Fast dataframes
```

**Machine Learning:**
```
scikit-learn - Classical ML algorithms
XGBoost - Gradient boosting
LightGBM - Fast gradient boosting
CatBoost - Categorical data boosting
```

**Deep Learning:**
```
TensorFlow - Google's DL framework
PyTorch - Facebook's DL framework
Keras - High-level neural networks API
JAX - High-performance ML
```

**NLP:**
```
NLTK - Natural language toolkit
spaCy - Industrial NLP
Hugging Face Transformers - Pre-trained models
Gensim - Topic modeling
```

**Computer Vision:**
```
OpenCV - Computer vision library
Pillow - Image processing
torchvision - PyTorch vision
albumentations - Image augmentation
```

### MLOps Tools

**Experiment Tracking:**
```
MLflow - ML lifecycle management
Weights & Biases - Experiment tracking
Neptune - Metadata store
Comet - ML platform
```

**Model Serving:**
```
FastAPI - Modern API framework
Flask - Lightweight API
BentoML - Model serving
TorchServe - PyTorch serving
TF Serving - TensorFlow serving
```

**Orchestration:**
```
Apache Airflow - Workflow automation
Kubeflow - ML on Kubernetes
Prefect - Modern workflow
Dagster - Data orchestration
```

**Monitoring:**
```
Prometheus - Metrics collection
Grafana - Visualization
Evidently - ML monitoring
WhyLabs - Data quality
```

### Cloud Platforms

**AWS:**
```
SageMaker - Full ML platform
EC2 - Compute instances
S3 - Object storage
Lambda - Serverless
```

**Google Cloud:**
```
Vertex AI - ML platform
Compute Engine - VMs
Cloud Storage - Object storage
Cloud Functions - Serverless
```

**Azure:**
```
Azure ML - ML platform
Virtual Machines - Compute
Blob Storage - Object storage
Functions - Serverless
```

---

<a name="resources"></a>
## 12. Learning Resources

### Online Courses

**Fundamentals:**
1. **Andrew Ng's Machine Learning** (Coursera) - Best introduction
2. **Fast.ai Practical Deep Learning** - Hands-on approach
3. **DeepLearning.AI Specialization** - Comprehensive deep learning

**Advanced:**
1. **Stanford CS229** - Machine Learning
2. **Stanford CS231n** - Computer Vision
3. **Stanford CS224n** - NLP
4. **MIT 6.S191** - Deep Learning

**Platforms:**
- Coursera
- edX
- Udacity
- Fast.ai
- DataCamp
- Kaggle Learn
