# 🚀 OpticWaveSim 1.1 - Deployment Guide

**Complete deployment instructions for local and cloud environments**

---

## 📋 Table of Contents

1. [Local Development](#local-development)
2. [Streamlit Cloud Deployment](#streamlit-cloud-deployment)
3. [Docker Deployment](#docker-deployment)
4. [GitHub Actions CI/CD](#github-actions-cicd)
5. [Troubleshooting](#troubleshooting)

---

## 🏠 Local Development

### Prerequisites

- Python 3.9+
- pip or conda
- Git

### Installation Steps

```bash
# 1. Clone the repository
git clone https://github.com/aminemedouar/OpticWaveSim1.git
cd OpticWaveSim1

# 2. Create virtual environment
python -m venv venv

# 3. Activate virtual environment
# On Linux/macOS:
source venv/bin/activate

# On Windows:
venv\Scripts\activate

# 4. Install dependencies
pip install -r requirements.txt

# 5. Run the application
streamlit run main.py
```

### Access the Application

Open your browser and navigate to:
```
http://localhost:8501
```

### Development Tips

```bash
# Run with debug mode
streamlit run main.py --logger.level=debug

# Run tests
pytest tests/ -v --cov=.

# Format code
black main.py

# Check for issues
pylint main.py
```

---

## ☁️ Streamlit Cloud Deployment

### Prerequisites

- GitHub account
- Streamlit Community Cloud account (free)
- Repository on GitHub (already done!)

### Deployment Steps

#### Method 1: Using Streamlit Dashboard

1. Go to https://share.streamlit.io/
2. Click **"New app"**
3. Select repository: `aminemedouar/OpticWaveSim1`
4. Select branch: `main`
5. Select main file: `main.py`
6. Click **"Deploy"**

#### Method 2: Using Streamlit CLI

```bash
# Install Streamlit CLI
pip install streamlit

# Deploy directly from local repo
streamlit cloud deploy

# Follow the prompts to authenticate with GitHub
```

### Post-Deployment

Your app will be available at:
```
https://opticwavesim.streamlit.app
```

### Environment Variables (if needed)

Create a `.streamlit/secrets.toml` file:

```toml
# Example if you use external APIs
GROK_API_KEY = "your-key-here"
DATABASE_URL = "your-database-url"
```

**Note:** `.streamlit/secrets.toml` is in `.gitignore` for security.

---

## 🐳 Docker Deployment

### Create Dockerfile

File: `Dockerfile`

```dockerfile
FROM python:3.9-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application
COPY . .

# Expose Streamlit port
EXPOSE 8501

# Create .streamlit directory
RUN mkdir -p .streamlit

# Copy Streamlit config
COPY .streamlit/config.toml .streamlit/config.toml

# Health check
HEALTHCHECK CMD curl --fail http://localhost:8501/_stcore/health

# Run Streamlit
CMD ["streamlit", "run", "main.py"]
```

### Build and Run Docker Image

```bash
# Build image
docker build -t opticwavesim:1.1 .

# Run container locally
docker run -p 8501:8501 opticwavesim:1.1

# Run with environment variables
docker run -p 8501:8501 \
  -e GROK_API_KEY=your-key \
  opticwavesim:1.1
```

### Docker Compose (Multiple Services)

File: `docker-compose.yml`

```yaml
version: '3.8'

services:
  opticwavesim:
    build: .
    ports:
      - "8501:8501"
    environment:
      - STREAMLIT_SERVER_HEADLESS=true
      - STREAMLIT_SERVER_PORT=8501
      - STREAMLIT_LOGGER_LEVEL=info
    volumes:
      - ./.streamlit:/app/.streamlit
    restart: unless-stopped
```

Run with Docker Compose:
```bash
docker-compose up -d
```

---

## 🔄 GitHub Actions CI/CD

### Workflow File

File: `.github/workflows/ci_cd.yml`

```yaml
name: Tests & Deploy

on:
  push:
    branches: [main]
  pull_request:
    branches: [main]

jobs:
  test:
    runs-on: ubuntu-latest
    strategy:
      matrix:
        python-version: ['3.9', '3.10', '3.11']

    steps:
    - uses: actions/checkout@v3
    
    - name: Set up Python ${{ matrix.python-version }}
      uses: actions/setup-python@v4
      with:
        python-version: ${{ matrix.python-version }}
    
    - name: Install dependencies
      run: |
        python -m pip install --upgrade pip
        pip install -r requirements.txt
        pip install pytest pytest-cov
    
    - name: Run tests
      run: |
        pytest tests/ -v --cov=. --cov-report=xml
    
    - name: Upload coverage
      uses: codecov/codecov-action@v3
      with:
        files: ./coverage.xml

  deploy:
    needs: test
    runs-on: ubuntu-latest
    if: github.ref == 'refs/heads/main' && github.event_name == 'push'

    steps:
    - uses: actions/checkout@v3
    
    - name: Deploy to Streamlit Cloud
      run: |
        echo "Deployment to Streamlit Cloud triggered"
        # Streamlit Cloud auto-deploys from GitHub
```

### Workflow Triggers

The workflow runs on:
- ✅ Push to `main` branch
- ✅ Pull requests to `main` branch

### View Workflow Results

https://github.com/aminemedouar/OpticWaveSim1/actions

---

## 🧪 Testing

### Run All Tests

```bash
pytest tests/ -v --cov=.
```

### Run Specific Test File

```bash
pytest tests/test_optics.py -v
```

### Run with Coverage Report

```bash
pytest tests/ --cov=. --cov-report=html
open htmlcov/index.html
```

### Test Results

Expected output:
```
tests/test_optics.py::test_fiber_initialization PASSED
tests/test_optics.py::test_linear_propagation PASSED
tests/test_optics.py::test_qpsk_modulate PASSED
...
======================== 15 passed in 0.45s ========================
Coverage: 92%
```

---

## 📊 Performance Monitoring

### Local Profiling

```bash
# Install profiler
pip install streamlit-profiler

# Add to main.py
from streamlit_profiler import Profiler
profiler = Profiler()
profiler.start()
```

### Streamlit Cloud Monitoring

Visit the app settings in Streamlit Cloud dashboard:
- View logs
- Monitor resource usage
- Check deployment status

---

## 🔐 Security Best Practices

### Environment Variables

Never commit sensitive data. Use `.streamlit/secrets.toml`:

```toml
# .streamlit/secrets.toml (NOT in git)
database_password = "your-password"
api_key = "your-api-key"
```

Access in code:
```python
import streamlit as st
password = st.secrets["database_password"]
```

### Dependencies Security

```bash
# Check for vulnerabilities
pip install safety
safety check

# Or use GitHub security alerts
# Enable on repository settings
```

---

## 🚨 Troubleshooting

### Issue: "Module not found" Error

**Solution:**
```bash
# Reinstall dependencies
pip install -r requirements.txt --upgrade

# Clear cache
rm -rf ~/.cache/pip
pip install -r requirements.txt
```

### Issue: Port 8501 Already in Use

**Solution:**
```bash
# Use different port
streamlit run main.py --server.port=8502

# Or kill the process using 8501
# On Linux/macOS:
lsof -i :8501
kill -9 <PID>

# On Windows:
netstat -ano | findstr :8501
taskkill /PID <PID> /F
```

### Issue: Streamlit Cloud Deployment Fails

**Solution:**
1. Check `requirements.txt` compatibility
2. Verify Python version (3.9+)
3. Check repository visibility (must be public)
4. Review deployment logs in Streamlit Cloud

### Issue: App Crashes After Deployment

**Solution:**
```bash
# Test locally first
streamlit run main.py

# Check for runtime errors
streamlit run main.py --logger.level=debug

# Verify all imports are in requirements.txt
```

### Issue: Performance is Slow

**Solution:**
```python
# Add caching to Streamlit
@st.cache_data
def expensive_computation():
    # Your code
    pass

# Profile the app
pip install streamlit-profiler
```

---

## 📈 Scaling

### For High Traffic

Use Docker + Kubernetes:

```yaml
# kubernetes.yml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: opticwavesim
spec:
  replicas: 3
  selector:
    matchLabels:
      app: opticwavesim
  template:
    metadata:
      labels:
        app: opticwavesim
    spec:
      containers:
      - name: opticwavesim
        image: opticwavesim:1.1
        ports:
        - containerPort: 8501
```

---

## 📞 Support

For deployment issues:

- 📧 Email: amine.medouar@example.com
- 🐛 GitHub Issues: https://github.com/aminemedouar/OpticWaveSim1/issues
- 💬 Discussions: https://github.com/aminemedouar/OpticWaveSim1/discussions

---

## ✅ Deployment Checklist

- [ ] Local development works (`streamlit run main.py`)
- [ ] All tests pass (`pytest tests/ -v`)
- [ ] requirements.txt is up to date
- [ ] No hardcoded secrets in code
- [ ] .gitignore includes sensitive files
- [ ] GitHub repository is public
- [ ] Streamlit Cloud account created
- [ ] Deployment successful
- [ ] App accessible at https://opticwavesim.streamlit.app

---

<div align="center">

### 🚀 OpticWaveSim - Deployed & Running

**Ready for production!**

</div>
