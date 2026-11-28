# Gemini AI API – Question Answering & Customer Feedback Analysis

A REST API built with **FastAPI** that integrates Google's **Gemini API** to generate AI-powered answers and analyze customer feedback.

The API supports configurable temperature, structured JSON responses, request and response validation, token usage tracking, and error handling.

## Features

- Generate AI-powered answers using Google's Gemini API.
- Configurable temperature to control response variability.
- Analyze customer reviews using Gemini.
- Classify customer sentiment as Positive, Negative, Neutral, or Mixed.
- Extract delivery and product feedback separately.
- Generate structured JSON responses using Gemini's response schema.
- Validate request and response data using Pydantic.
- Track input, output, and total token usage for AI questions.
- Handle Gemini API errors and unexpected server errors.
- Interactive API documentation using Swagger UI.

## Technologies Used

- **Python** – Programming language
- **FastAPI** – Backend web framework
- **Google Gemini API** – AI response generation
- **Google Gen AI SDK** – Python integration with Gemini
- **Pydantic** – Request and response validation
- **Uvicorn** – ASGI server
- **Python-dotenv** – Environment variable management

## Installation and Setup

### 1. Clone the repository

```bash
git clone https://github.com/muhammedafthal/gemini-api-fastapi.git
```

### 2. Navigate to the project directory

```bash
cd gemini-api-fastapi
```

### 3. Create a virtual environment

```bash
python -m venv .venv
```

### 4. Activate the virtual environment

**macOS / Linux:**

```bash
source .venv/bin/activate
```

**Windows:**

```bash
.venv\Scripts\activate
```

### 5. Install dependencies

```bash
pip install -r requirements.txt
```

### 6. Configure environment variables

Create a `.env` file in the project root directory:

```env
GEMINI_API_KEY=your_gemini_api_key
```

Replace `your_gemini_api_key` with your actual Gemini API key.

### 7. Run the application

```bash
uvicorn main:app --reload
```

## API Endpoints

### 1. Generate AI Answer

Generates an AI-powered answer based on the user's question using Google's Gemini API.

- **Endpoint:** `/ask`
- **Method:** `POST`
- **Content-Type:** `application/json`

#### Request Body

```json
{
  "question": "What is Artificial Intelligence?",
  "temperature": 0.5
}
```

| Field | Type | Description |
|---|---|---|
| `question` | String | The question to send to Gemini. Minimum 3 characters. |
| `temperature` | Float | Controls response variability. Must be between 0.0 and 1.0. |

#### Successful Response (200 OK)

```json
{
  "success_status": 200,
  "received_question": "What is Artificial Intelligence?",
  "temperature": 0.5,
  "total_tokens": 65,
  "input_tokens": 11,
  "output_tokens": 54,
  "response": "Artificial Intelligence is the simulation of human intelligence by computer systems and machines."
}
```

*Note: Token counts and generated answers will vary depending on the request.*

#### Error Responses

| Status Code | Description |
|---|---|
| 400 | Invalid request sent to Gemini |
| 401 | Authentication failed |
| 422 | Request validation failed |
| 429 | Gemini API quota or rate limit exceeded |
| 502 | Invalid or empty AI response |
| 500 | Internal server or AI service error |

### 2. Analyze Customer Feedback

Analyzes customer reviews using Gemini and extracts sentiment, delivery feedback, and product feedback into a structured JSON response.

- **Endpoint:** `/analyze-feedback`
- **Method:** `POST`
- **Content-Type:** `application/json`

#### Request Body

```json
{
  "review": "The product quality is excellent, but delivery was late."
}
```

| Field | Type | Description |
|---|---|---|
| `review` | String | Customer review to analyze. Minimum 5 characters. |

#### Successful Response (200 OK)

```json
{
  "sentiment": "Mixed",
  "delivery_feedback": "Delivery was late",
  "product_feedback": "The product quality is excellent"
}
```

*Note: The analysis and extracted feedback will vary depending on the customer review.*

#### Error Responses

| Status Code | Description |
|---|---|
| 400 | Invalid request sent to Gemini |
| 401 | Authentication failed |
| 422 | Request validation failed |
| 429 | Gemini API quota or rate limit exceeded |
| 502 | Invalid or empty AI response |
| 500 | Internal server or AI service error |

## Interactive API Documentation

After starting the application, visit:

[http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)

Use Swagger UI to explore and test both API endpoints.

## Project Structure

```text
gemini-api-fastapi/
│
├── .venv/              # Python virtual environment
├── .env                # Environment variables (API key)
├── .gitignore          # Files excluded from Git
├── main.py             # FastAPI application
├── README.md           # Project documentation
└── requirements.txt    # Project dependencies
```