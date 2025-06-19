# Actor Portfolio

A Flask-based portfolio website for showcasing theatrical work and performances.

## Setup

1. Create virtual environment:
   ```bash
   python -m venv venv
   venv\Scripts\activate
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Run the application:
   ```bash
   python app.py
   ```

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
## License

This project is licensed under the [MIT License](LICENSE).
