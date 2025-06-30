# Job Search Application

A project for searching job vacancies across various platforms.

## Project Structure
````
job_search/
├── .github/
│ └── workflows/ # GitHub Actions workflows
├── src/
│ ├── api/ # API integration modules
│ ├── cli/ # Command-line components
│ ├── exceptions/ # Custom exceptions
│ ├── file_workers/ # File operations
│ ├── models/ # Data models
│ ├── utils/ # Utility functions
│ └── vacancies/ # Vacancies module
├── tests/ # Test files
├── .gitignore
├── LICENSE
├── pyproject.toml # Project configuration
└── requirements.txt # Dependencies
````
## Installation

1. Clone the repository:
```
git clone https://github.com/AlyonaSytnik/job_search.git
cd job_search
```
Install dependencies:
````
pip install -r requirements.txt
````
## Usage
CLI Interface
The primary way to interact with the application is through the command line:
```
python src/cli/main.py
```

## Configuration
You can set configuration parameters in the config.ini file.

# Testing
Run tests with:
```
pytest tests/
```
## Contributing
Fork the repository

Create your feature branch (git checkout -b feature/AmazingFeature)

Commit your changes (git commit -m 'Add some AmazingFeature')

Push to the branch (git push origin feature/AmazingFeature)

Open a Pull Request

## Coverage

```

File	         statements	missing	excluded	coverage
src\__init__.py	         0	  0	    0	          100%
src\api.py	        13	  1	    0	           92%
src\fileworker.py	57	  6	    0	           89%
src\utils.py	        36	  15	    0	           58%
src\vacancy.py	        32	  0	    0	          100%
Total	               138	  22	    0	           84%

```