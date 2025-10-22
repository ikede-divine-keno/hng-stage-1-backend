# hng-stage-1-backend String Analyzer API 🚀
GitHub repo for HNG Stage 1 backend track

![Python](https://img.shields.io/badge/Python-3.10+-blue.svg)
![FastAPI](https://img.shields.io/badge/FastAPI-0.115.2-green.svg)
![Railway](https://img.shields.io/badge/Deployed-Railway-blueviolet.svg)

## String Analyzer API

A RESTful API built with FastAPI for analyzing strings and storing their computed properties, such as length, palindrome status, unique characters, word count, SHA-256 hash, and character frequency map. The API supports creating, retrieving, filtering (including natural language queries), and deleting strings.

The project uses in-memory storage for simplicity, resetting on server restart. For production persistence, consider switching to SQLite or Redis

## Features

- **Create/Analyze Strings**: POST `/strings` to compute and store string properties.
- **Retrieve Specific String**: GET `/strings/{string_value}` to fetch a stored string.
- **Filter Strings**: GET `/strings` with query parameters (e.g., `is_palindrome=true&min_length=5`).
- **Natural Language Filtering**: GET `/strings/filter-by-natural-language?query=...` for queries like "all single word palindromic strings".
- **Delete Strings**: DELETE `/strings/{string_value}` to remove a string.
- **Interactive Docs**: Swagger UI at `/docs` and ReDoc at `/redoc`.
- **CORS**: Enabled with `allow_origins=["*"]` for cross-origin access, ideal for bot testing.
- **Error Handling**: Returns 400, 404, 409, 422 with descriptive messages.
- **Status Codes**: 201 for POST, 200 for GET, 204 for DELETE.

## Project Structure

```
string-analyzer-api/
├── app/
│   ├── __init__.py       # Makes 'app' a Python package
│   ├── main.py           # FastAPI app with routes and CORS middleware
│   ├── models.py         # Pydantic models for request/response validation
│   ├── storage.py       # In-memory storage and string property computation
├── README.md             # This documentation
└── requirements.txt      # Dependencies (fastapi, uvicorn)
```

- **app/main.py**: Defines API routes and CORS settings.
- **app/models.py**: Pydantic models (`StringRequest`, `StringResponse`, `StringsListResponse`, `NaturalLanguageResponse`).
- **app/storage.py**: Manages in-memory storage
- **requirements.txt**:
  ```
  fastapi
  uvicorn
  ```

## Prerequisites

- **Python**: 3.8+ (tested on 3.12).
- **Git**: For cloning the repository.
- **Virtual Environment**: Recommended (e.g., `venv`).
- **Optional**: Railway account for deployment, SQLite/Redis for persistent storage.

## Setup Instructions

1. **Fork and Clone the Repository**:
   Fork the project then clone from GitHub to your local machine:
   ```bash
   git clone https://github.com/your-username/hng-stage-1-backend.git
   cd hng-stage-1-backend/string-analyzer-api
   ```
   Replace `your-username` with the actual GitHub username or repository URL.

2. **Set Up Virtual Environment**:
   Create and activate a virtual environment:
   ```bash
   python -m venv venv
   ```
   - Windows: `venv\Scripts\activate`
   - Unix/Mac: `source venv/bin/activate`

3. **Install Dependencies**:
   Install required packages from `requirements.txt`:
   ```bash
   pip install -r requirements.txt
   ```

4. **Verify Project Files**:
   Ensure the project structure matches the above, with `app/main.py`, `app/models.py`, and `app/storage.py` in place.

## Running Locally

Start the development server with hot-reloading:
```bash
uvicorn app.main:app --reload --port 8000
```

- **URL**: `http://127.0.0.1:8000`
- **Swagger UI**: `http://127.0.0.1:8000/docs`
- **ReDoc**: `http://127.0.0.1:8000/redoc`
- **Note**: In-memory storage resets on server restart. Use a single worker to ensure data consistency for testing.

For production-like testing (no reload):
```bash
uvicorn app.main:app --host 0.0.0.0 --port 8000
```

**Important**: Avoid multiple workers (`--workers N`) with in-memory storage, as each worker has an isolated dictionary, causing inconsistent results for bot testing (e.g., 404s for GETs). Use SQLite/Redis for multi-worker setups.

## Testing

### Interactive Testing
- Access Swagger UI at `http://127.0.0.1:8000/docs` to test endpoints interactively.
- Add strings via POST `/strings` before testing GET/DELETE.

### Curl Test Examples
Run these commands to test locally (`http://127.0.0.1:8000`). Populate storage first for meaningful results.

1. **POST /strings** (Analyze and Store):
   ```bash
   curl -i -X POST http://127.0.0.1:8000/strings -H "Content-Type: application/json" -d '{"value": "hello world"}'
   ```
   - **Expect**: HTTP 201, JSON with `id`, `value`, `properties`, `created_at`.
   - **Errors**: 409 (duplicate), 422 (invalid input).

2. **GET /strings/{string_value}** (Specific String):
   ```bash
   curl -i http://127.0.0.1:8000/strings/hello%20world
   ```
   - **Expect**: HTTP 200, string data.
   - **Errors**: 404 (not found).

3. **GET /strings** (Filtered List):
   ```bash
   curl -i "http://127.0.0.1:8000/strings?is_palindrome=true&min_length=5&word_count=1&contains_character=a"
   ```
   - **Expect**: HTTP 200, JSON with `data`, `count`, `filters_applied`.
   - **Errors**: 400 (invalid params).

4. **GET /strings/filter-by-natural-language** (Natural Language):
   ```bash
   curl -i "http://127.0.0.1:8000/strings/filter-by-natural-language?query=all%20single%20word%20palindromic%20strings"
   ```
   - **Expect**: HTTP 200, JSON with `data`, `count`, `interpreted_query` (no `filters_applied` or `null`).
   - **Errors**: 400 (unparsable query), 422 (conflicting filters).

5. **DELETE /strings/{string_value}**:
   ```bash
   curl -i -X DELETE http://127.0.0.1:8000/strings/hello%20world
   ```
   - **Expect**: HTTP 204 (empty body).
   - **Errors**: 404 (not found).

**Test Setup**:
- Add test data:
  ```bash
  curl -X POST http://127.0.0.1:8000/strings -H "Content-Type: application/json" -d '{"value": "racecar"}'
  curl -X POST http://127.0.0.1:8000/strings -H "Content-Type: application/json" -d '{"value": "level"}'
  ```
- Run tests to verify status codes (200, 201, 204) and error handling (400, 404, 409, 422).

**Edge Cases**:
- Empty strings: Blocked (422).
- Special characters: Handled correctly.
- Server restart: Clears in-memory storage.

## Deployment on Railway

Railway is a cloud platform for deploying web apps with GitHub integration and automatic scaling. Below are steps to deploy the API.

### Prerequisites
- GitHub repository with the project.
- Railway account ([railway.app](https://railway.app)).

### Steps
1. **Push to GitHub**:
   Ensure the project is in a GitHub repository:
   ```bash
   git add .
   git commit -m "Initial commit"
   git push origin main
   ```
   If not yet pushed, set up the remote:
   ```bash
   git remote add origin https://github.com/your-username/string-analyzer-api.git
   git push -u origin main
   ```

2. **Create Railway Project**:
   - Log in to Railway dashboard.
   - Click "New Project" > "Deploy from GitHub repo".
   - Authorize Railway and select your repository.
   - Railway auto-detects Python and installs `requirements.txt`.

3. **Configure Deployment**:
   - **Start Command**: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`
     - `$PORT` is provided by Railway.
   - **Build Command**: Leave default (`pip install -r requirements.txt`).
   - **Environment Variables**: None needed for in-memory storage. For SQLite, add a volume (e.g., `/app/strings.db`) and set `DATABASE_URL=sqlite:////app/strings.db`.

4. **Deploy**:
   - Click "Deploy". Railway builds and deploys.
   - Access at the generated URL (e.g., `https://your-app.railway.app`).
   - Check logs in the Railway dashboard for errors.

5. **Custom Domain (Optional)**:
   - Add a domain in Railway settings and update DNS records.

### Deployment Notes
- **In-Memory Storage**: Resets on redeploy or restart. For persistence, update `storage.py` to use SQLite or Redis(add `sqlalchemy`, `aiosqlite` or `redis` to `requirements.txt`).
- **Single Worker**: Recommended to avoid data inconsistencies with in-memory storage. Set in Railway’s start command or use SQLite/Redis for multi-worker support.
- **Monitoring**: Use Railway’s logs and metrics for debugging.
- **Costs**: Free tier for testing; review Railway’s pricing for production.

For details, see [Railway’s FastAPI guide](https://docs.railway.com/guides/fastapi).

## Production Considerations

- **Single Worker**: Use `uvicorn app.main:app --host 0.0.0.0 --port 8000` for in-memory storage to ensure bot testing consistency (avoids isolated dictionaries).
- **Persistence**: Switch to SQLite for data persistence:
  ```bash
  pip install sqlalchemy aiosqlite
  ```
  Update `storage.py`
- **No `--reload`**: Avoid in production to prevent restarts and performance overhead.
- **Reverse Proxy**: Deploy behind Nginx for load balancing and SSL.
- **SSL**: Use Let’s Encrypt for HTTPS.

## Troubleshooting

- **404 on /strings/filter-by-natural-language**: Ensure routes in `main.py` are ordered correctly (`/strings/filter-by-natural-language` before `/strings/{string_value}`).
- **Pydantic Errors**: Verify `models.py` uses `Union[str, int, bool]` for `filters_applied` and `interpreted_query`.
- **Inconsistent Data**: Use single worker or SQLite/Redis for bot testing.
- **Railway Errors**: Check logs for port binding or dependency issues.

## Contributing

- Fork the repository.
- Create a feature branch (`git checkout -b feature/xyz`).
- Commit changes (`git commit -m "Add feature"`).
- Push and open a pull request.