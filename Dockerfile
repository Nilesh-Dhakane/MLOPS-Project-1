FROM python:3.10-slim

# ✅ Correct environment variables (your syntax was wrong)
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

# ✅ Correct working directory
WORKDIR /app

# ✅ System dependencies (for sklearn, lightgbm, xgboost, etc.)
RUN apt-get update && apt-get install -y --no-install-recommends \
    libgomp1 \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# ✅ Copy project files
COPY . .

# ✅ Install Python dependencies from setup.py
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -e .

# ✅ Expose Flask port
EXPOSE 5000

# ✅ Runtime execution (THIS FIXES YOUR ERROR)
CMD ["bash", "-c", "python pipeline/pipeline.py && python app.py"]

