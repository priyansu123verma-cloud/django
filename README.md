# Django Notes Application

A simple Django application for creating and managing notes with comprehensive testing and CI/CD integration.

## Features

- ✅ Create and view notes
- ✅ Form validation (minimum 10 characters for description)
- ✅ Comprehensive unit tests with Django TestCase
- ✅ Selenium UI tests for end-to-end testing
- ✅ GitHub Actions CI/CD pipeline
- ✅ Code quality checks (flake8, black, isort)
- ✅ Code coverage reports
- ✅ Bootstrap-based responsive UI

## Project Structure

```
lab15/
├── .github/
│   └── workflows/
│       └── django.yml                 # GitHub Actions CI pipeline
├── notesproject/                      # Django project root
│   ├── manage.py                      # Django management script
│   ├── requirements.txt               # Python dependencies
│   ├── db.sqlite3                     # SQLite database (created after migration)
│   ├── notesproject/                  # Project settings package
│   │   ├── __init__.py
│   │   ├── settings.py               # Django settings
│   │   ├── urls.py                   # Project URL routing
│   │   └── wsgi.py                   # WSGI application
│   ├── notes/                         # Notes app package
│   │   ├── migrations/                # Database migrations
│   │   ├── __init__.py
│   │   ├── models.py                 # Note model with validation
│   │   ├── forms.py                  # NoteForm with validation
│   │   ├── views.py                  # Views for creating/viewing notes
│   │   ├── urls.py                   # App URL routing
│   │   ├── admin.py                  # Django admin configuration
│   │   ├── apps.py                   # App configuration
│   │   ├── tests.py                  # Django unit tests
│   │   └── selenium_tests.py         # Selenium UI tests
│   │
│   └── notesproject/templates/        # HTML templates
│       ├── base.html                 # Base template
│       └── notes/
│           ├── create_note.html      # Create note form
│           ├── note_list.html        # List all notes
│           └── note_detail.html      # View single note
│
└── README.md                          # This file
```

## Installation

### Prerequisites

- Python 3.10+
- pip (Python package manager)
- Virtual environment (recommended)

### Setup Steps

1. **Navigate to the project directory:**
   ```bash
   cd notesproject
   ```

2. **Create a virtual environment (recommended):**
   ```bash
   # Windows
   python -m venv venv
   venv\Scripts\activate
   
   # macOS/Linux
   python3 -m venv venv
   source venv/bin/activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run migrations:**
   ```bash
   python manage.py migrate
   ```

5. **Create a superuser (optional, for admin panel):**
   ```bash
   python manage.py createsuperuser
   ```

## Running the Application

### Development Server

```bash
python manage.py runserver
```

The application will be available at `http://127.0.0.1:8000/`

### Access the Application

- **Notes List:** http://127.0.0.1:8000/
- **Create Note:** http://127.0.0.1:8000/create/
- **Django Admin:** http://127.0.0.1:8000/admin/

## Running Tests

### Unit Tests

```bash
# Run all unit tests
python manage.py test notes.tests

# Run specific test class
python manage.py test notes.tests.NoteModelTestCase

# Run with verbose output
python manage.py test notes.tests --verbosity=2
```

### Selenium UI Tests

```bash
# Run Selenium tests (requires Chrome/Firefox WebDriver)
python manage.py test notes.selenium_tests

# Run specific Selenium test class
python manage.py test notes.selenium_tests.SeleniumNoteTests
```

### Code Coverage

```bash
coverage run --source='notes' manage.py test notes.tests
coverage report
coverage html  # Generates HTML report in htmlcov/
```

### Direct Selenium Test Running

```bash
python notes/selenium_tests.py
```

## Code Quality Checks

### Linting with flake8

```bash
flake8 .
```

### Code Formatting with Black

```bash
black .
```

### Import Sorting with isort

```bash
isort .
```

## Model Validation

The Note model includes the following validation:

- **Title:** Required, max 200 characters
- **Description:** Required, minimum 10 characters
  - Validated in both model `clean()` method and form

### Description Validation Example

**Valid:** "This is a valid description" (26 characters) ✅

**Invalid:** "Too short" (9 characters) ❌

Error Message: "Description must be at least 10 characters long."

## Form Validation

The NoteForm includes:
- Title field (required)
- Description field (required, min 10 characters)
- Bootstrap CSS classes for styling
- IDs for Selenium testing (`id_title`, `id_description`)
- Client-side JavaScript validation

## Views and URLs

| URL | View | Method | Description |
|-----|------|--------|-------------|
| `/` | `note_list` | GET | Display all notes |
| `/create/` | `create_note` | GET, POST | Create a new note |
| `/note/<id>/` | `note_detail` | GET | View a single note |

## GitHub Actions CI Pipeline

The `.github/workflows/django.yml` file configures automated testing with:

- **Triggers:** Push to main/develop, Pull requests
- **Python Versions:** 3.10, 3.11, 3.12
- **Jobs:**
  - `test`: Run Django unit tests on multiple Python versions
  - `selenium-tests`: Run Selenium UI tests (requires Chrome)
  - `lint`: Code quality checks (flake8, black, isort)

### CI Steps

1. Check out code
2. Set up Python
3. Install dependencies
4. Run migrations
5. Run Django unit tests
6. Generate coverage report
7. Collect static files
8. Run Selenium tests (if unit tests pass)
9. Run code quality checks

## Testing Strategy

### Unit Tests (48 test cases)

1. **Model Tests (NoteModelTestCase)**
   - Note creation with valid data
   - Validation errors for short descriptions
   - Clean method validation
   - String representation
   - Model ordering

2. **Form Tests (NoteFormTestCase)**
   - Form validation with valid/invalid data
   - Edge cases (exactly 10 characters)
   - Required field validation

3. **View Tests (NoteViewTestCase)**
   - Note list display
   - Note detail display
   - Create note form display
   - POST request handling (valid/invalid)
   - Redirect behavior
   - Error messages

4. **Integration Tests (NoteIntegrationTestCase)**
   - Complete workflow (create → list → detail)
   - Validation error flow

### Selenium UI Tests (10+ test cases)

1. **SeleniumNoteTests**
   - Create note successfully
   - View note details
   - Short description validation error display
   - Empty description validation error
   - Empty title validation error
   - Navigation between pages
   - Create multiple notes

2. **SeleniumFormFieldsTest**
   - Form field placeholders
   - CSRF token presence

## Troubleshooting

### Port Already in Use

```bash
# Use a different port
python manage.py runserver 8001
```

### Database Issues

```bash
# Reset database (WARNING: deletes all data)
rm db.sqlite3
python manage.py migrate
```

### Missing Static Files

```bash
python manage.py collectstatic
```

### Selenium WebDriver Issues

1. **Install Chrome:** Download from https://www.google.com/chrome/
2. **Install ChromeDriver:** Download from https://chromedriver.chromium.org/
3. **Or use Firefox:** Install geckodriver for Firefox

### Migration Issues

```bash
# Create fresh migrations
python manage.py makemigrations
python manage.py migrate
```

## Environment Variables

You can customize Django settings by setting environment variables:

```bash
# Windows
set DEBUG=False
set SECRET_KEY=your-secret-key

# macOS/Linux
export DEBUG=False
export SECRET_KEY=your-secret-key
```

## Deployment Considerations

Before deploying to production:

1. Set `DEBUG = False` in settings.py
2. Set a secure `SECRET_KEY`
3. Configure `ALLOWED_HOSTS` properly
4. Use PostgreSQL instead of SQLite
5. Set up proper HTTPS/SSL
6. Configure static files serving (S3, CloudFront, etc.)
7. Set up proper database backups
8. Enable security middleware (SECURE_SSL_REDIRECT, etc.)

## Common Django Commands

```bash
# Create a new app
python manage.py startapp appname

# Create migrations
python manage.py makemigrations

# Apply migrations
python manage.py migrate

# Run development server
python manage.py runserver

# Create superuser
python manage.py createsuperuser

# Access Django shell
python manage.py shell

# Collect static files
python manage.py collectstatic

# Run specific management command
python manage.py <command> [options]
```

## Contributing

1. Create a new branch for your feature
2. Make your changes
3. Run tests to ensure everything passes
4. Submit a pull request

## License

This project is created for educational purposes.

## Additional Resources

- [Django Official Documentation](https://docs.djangoproject.com/)
- [Django Testing Documentation](https://docs.djangoproject.com/en/4.2/topics/testing/)
- [Selenium Documentation](https://www.selenium.dev/documentation/)
- [GitHub Actions Documentation](https://docs.github.com/en/actions)

---

**Last Updated:** March 2026
