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

3. Run the application:
   ```bash
   python3.12 app.py
   ```

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

## Citation

To cite this project, please use the metadata provided in [CITATION.cff](CITATION.cff).

## License

This project is licensed under the [MIT License](LICENSE).
