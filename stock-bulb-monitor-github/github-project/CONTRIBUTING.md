# Contributing to Stock Bulb Monitor

First off, thank you for considering contributing to Stock Bulb Monitor! 🎉

## How Can I Contribute?

### Reporting Bugs

Before creating bug reports, please check existing issues. When you create a bug report, include as many details as possible:

- **Use a clear and descriptive title**
- **Describe the exact steps to reproduce the problem**
- **Provide specific examples**
- **Describe the behavior you observed and what you expected**
- **Include log files** (remove sensitive data!)
- **Specify your environment** (OS, Python version, etc.)

### Suggesting Enhancements

Enhancement suggestions are tracked as GitHub issues. When creating an enhancement suggestion:

- **Use a clear and descriptive title**
- **Provide a detailed description of the suggested enhancement**
- **Explain why this enhancement would be useful**
- **List some examples of how it would be used**

### Pull Requests

1. Fork the repo and create your branch from `main`
2. If you've added code, add tests
3. Ensure the test suite passes
4. Make sure your code follows the existing style
5. Write a clear commit message
6. Submit your pull request!

## Development Setup

```bash
# Clone your fork
git clone https://github.com/YOUR_USERNAME/stock-bulb-monitor.git
cd stock-bulb-monitor

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Copy config template
cp config.json.template config.json
# Edit config.json with your credentials
```

## Coding Guidelines

### Python Style

- Follow PEP 8
- Use meaningful variable names
- Add docstrings to functions and classes
- Keep functions focused and small
- Add type hints where appropriate

### Commit Messages

- Use the present tense ("Add feature" not "Added feature")
- Use the imperative mood ("Move cursor to..." not "Moves cursor to...")
- Limit the first line to 72 characters
- Reference issues and pull requests

### Testing

Before submitting:

```bash
# Test Zerodha connection
python zerodha_api.py

# Test WiZ bulb
python test_bulb.py

# Run main application
python main.py
```

## Priority Contributions

We'd especially love help with:

1. **Angel One Integration** - FREE API alternative to Zerodha
2. **Web Dashboard** - Real-time P&L visualization
3. **Telegram Notifications** - Alert on major movements
4. **Multiple Bulb Support** - Control multiple bulbs
5. **Historical Tracking** - Database for P&L history
6. **Docker Support** - Containerization
7. **Tests** - Unit and integration tests

## Code of Conduct

- Be respectful and inclusive
- Welcome newcomers
- Focus on what is best for the community
- Show empathy towards others

## Questions?

Feel free to open an issue with your question!

---

Thank you for contributing! 🚀
