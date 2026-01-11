# Contributing to Formula Student Telemetry System

Thank you for your interest in contributing! This document provides guidelines and instructions for contributing.

## Code of Conduct

- Be respectful and professional
- Welcome diverse perspectives
- Focus on constructive feedback
- Help others learn and grow

## How to Contribute

### Reporting Bugs

1. Check if the bug has already been reported in Issues
2. Create a new issue with a clear title
3. Describe the bug with:
   - Step-by-step reproduction instructions
   - Expected behavior vs actual behavior
   - Python version and OS
   - Error messages and stack traces
   - Screenshots if applicable

### Suggesting Enhancements

1. Check existing issues for duplicate suggestions
2. Create an issue with a clear title starting with "Enhancement:"
3. Provide detailed description of the enhancement
4. Explain the motivation and use cases
5. Include examples or mock-ups if helpful

### Pull Requests

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/my-feature`
3. Make your changes
4. Write or update tests for new functionality
5. Ensure all tests pass: `pytest tests/ -v`
6. Commit with clear messages: `git commit -m "Add my feature"`
7. Push to your fork: `git push origin feature/my-feature`
8. Open a Pull Request with clear description

## Development Setup

### Prerequisites
- Python 3.8+
- Git
- pip or conda

### Installation

```bash
# Clone repository
git clone https://github.com/yourusername/fs-telemetry.git
cd fs-telemetry

# Create virtual environment
python -m venv venv
source venv/bin/activate  # Linux/Mac
# or
venv\Scripts\activate  # Windows

# Install dependencies
pip install -r requirements.txt
pip install -e .[dev,gui]

# Verify installation
python app.py
```

## Development Guidelines

### Code Style

- Follow [PEP 8](https://www.python.org/dev/peps/pep-0008/)
- Use meaningful variable and function names
- Maximum line length: 100 characters
- Use 4 spaces for indentation

### Comments and Documentation

- **All comments must be in English**
- Docstrings for all modules, classes, and functions
- Use triple quotes (""") for docstrings
- Include parameter descriptions and return types

Example:
```python
def calculate_average_speed(data_points: list) -> float:
    """
    Calculate the average speed from telemetry data points.
    
    :param data_points: List of TelemetryData objects
    :return: Average speed in km/h
    """
    if not data_points:
        return 0.0
    return sum(d.speed for d in data_points) / len(data_points)
```

### Testing

- Write tests for new features
- Ensure all tests pass before submitting PR
- Aim for >80% code coverage
- Use descriptive test names

```bash
# Run all tests
pytest tests/ -v

# Run specific test file
pytest tests/test_csv_parser.py -v

# Generate coverage report
pytest tests/ --cov=. --cov-report=html
```

### Commit Messages

- Use present tense: "Add feature" not "Added feature"
- Use imperative mood: "Move cursor to..." not "Moves cursor to..."
- Keep subject line under 50 characters
- Reference issues: "Fix #123" or "Closes #456"
- Separate subject from body with blank line

Example:
```
Add real-time speed visualization

- Implement PyQt5 speed gauge widget
- Update GUI to display live speed data
- Add unit tests for speed calculation

Fixes #123
```

### File Organization

```
fs-telemetry/
├── acquisition/       # Data source implementations
├── parsing/          # Data parsing logic
├── data/             # Data management
├── log_handlers/     # Logging functionality
├── gui/              # GUI components
├── visualization/    # Display utilities
├── tests/            # Unit tests
└── replay/           # Replay functionality
```

### Adding New Features

1. Create a feature branch
2. Add your code to appropriate module
3. Write comprehensive docstrings
4. Write unit tests (minimum 80% coverage)
5. Update README if needed
6. Ensure all tests pass
7. Submit Pull Request

## Documentation

### Updating Documentation

- Use clear, concise language
- Include code examples
- Keep README up to date
- Document API changes
- Update CHANGELOG for significant changes

### README Updates

- Keep feature list current
- Update installation instructions
- Add examples for new features
- Fix broken links

## Testing Checklist

Before submitting a PR, ensure:

- [ ] All tests pass: `pytest tests/ -v`
- [ ] Code coverage: `pytest --cov=. --cov-report=html`
- [ ] Code style: follows PEP 8
- [ ] Docstrings: all functions documented
- [ ] Comments: all in English
- [ ] No debug prints or commented code
- [ ] Works on Windows, Linux, and macOS
- [ ] No new dependencies without discussion

## Review Process

Pull Requests will be reviewed for:

1. Code quality and style
2. Test coverage and passing tests
3. Documentation completeness
4. Performance implications
5. Security considerations
6. API compatibility

## Getting Help

- Check existing issues and discussions
- Read the documentation
- Ask questions in issues (be specific)
- Check Discord/Slack community (if available)

## License

By contributing, you agree that your contributions will be licensed under the MIT License.

## Recognition

Contributors will be recognized in:
- README contributors section
- GitHub contributor graph
- Release notes (for significant contributions)

---

Thank you for contributing to Formula Student Telemetry System! 🏎️
