# Actor Portfolio

A Flask-based portfolio website for showcasing theatrical work and performances.

## Setup

1. Create virtual environment:
   ```bash
   python3.12 -m venv venv
   source venv/bin/activate
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Create a `.env` file:
   ```bash
   cp .env.example .env
   # then edit .env to add your configuration
   ```

4. Run the application:
   ```bash
   python3.12 wsgi.py
   ```

## Configuration

`create_app` accepts a configuration profile name:

- `development`
- `testing`
- `production`

Call the factory with the desired profile:

```python
from app import create_app

app = create_app("production")
```

Without an argument, the development configuration is used.

## Dependencies

The project relies on the following Python packages for HTTP requests and HTML parsing:

- `requests`
- `beautifulsoup4`
- `lxml` (used by Beautiful Soup for faster parsing)

## Development

- Run tests: `pytest`
- Format code: `black .`
- Lint code: `flake8 .`
- Install pre-commit hooks: `pre-commit install`

## Docker

Build and run with Docker:
```bash
docker build -t actor-portfolio .
docker run -p 5000:5000 actor-portfolio
```

### Docker Compose

For a production-style deployment using Nginx as a reverse proxy, you can use
`docker-compose`:

```bash
# Copy environment variables
cp .env.example .env

# Build and start the services
docker-compose up --build
```

The application will be available on port `80` and static files are served
directly by Nginx.

## Citation

To cite this project, please use the metadata provided in [CITATION.cff](CITATION.cff).

## License

This project is licensed under the [MIT License](LICENSE).
