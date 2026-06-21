# RealOrFakeImageService

A simple web service that classifies an image as **real** or **AI-generated (fake)** using a deep learning model

## Features

- Accepts image uploads via HTTP API
- Returns prediction: `real` or `fake` with confidence score
- Lightweight and easy to deploy
- Swagger UI for manual testing

## Tech Stack

- Python 3.13+
- FastAPI
- ONNX model

## Installation

```bash
git clone https://github.com/volzock/RealOrFakeImageService.git
```

set envs like in .env.example

```bash
docker-compose up
```