# TV Shows CRUD Application

A Django-based web application for managing TV shows with full CRUD (Create, Read, Update, Delete) functionality. This project implements RESTful routing conventions with custom validation using Django managers.

## 📋 Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Technology Stack](#technology-stack)
- [Installation](#installation)
- [Project Structure](#project-structure)
- [Database Models](#database-models)
- [Validation System](#validation-system)
- [Views & Routing](#views--routing)
- [Templates](#templates)
- [Usage Guide](#usage-guide)
- [API Endpoints](#api-endpoints)
- [Troubleshooting](#troubleshooting)
- [Future Enhancements](#future-enhancements)

---

## Overview

The TV Shows CRUD Application allows users to:
- **Create** new TV show entries with detailed information
- **Read** a list of all shows or individual show details
- **Update** existing show information
- **Delete** shows from the database

The application uses a custom validation system built into Django managers, eliminating the need for Django forms while maintaining robust error handling.

---

## Features

### ✨ Core Functionality
- ✅ Full CRUD operations for TV shows
- ✅ Custom validation in manager methods
- ✅ Error handling with detailed messages
- ✅ Form data persistence on validation errors
- ✅ Success/error message notifications
- ✅ Clean, professional UI design

### 🔍 Validation Features
- Title validation (required, 2-255 characters)
- Network validation (required, 2-100 characters)
- Release date validation (required, cannot be future date)
- Description validation (optional, max 1000 characters)
- Custom error messages per field
- Data preservation on form submission errors

### 🎨 User Interface
- Responsive design with clean styling
- Intuitive navigation between pages
- Table view for all shows
- Detailed view for individual shows
- Easy-to-use forms with error display
- Success notifications after actions

### 📊 Database Features
- Automatic timestamps (created_at, updated_at)
- Efficient data management with SQLite
- Model ordering and formatting methods
- Custom manager with validation methods

---

## Technology Stack

| Component | Technology |
|-----------|-----------|
| **Framework** | Django 6.0+ |
| **Database** | SQLite3 |
| **Frontend** | HTML5 + CSS3 |
| **Python** | 3.8+ |
| **Validation** | Custom Manager Methods |

---

## Installation

### Prerequisites
- Python 3.8 or higher
- pip (Python package manager)
- Virtual environment (recommended)

### Step 1: Create Virtual Environment

```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate
```

### Step 2: Install Django

```bash
pip install django
```

### Step 3: Create Project Structure

```bash
# Create Django project
django-admin startproject tv_shows_project
cd tv_shows_project

# Create Django app
python manage.py startapp shows
```

### Step 4: Add App to Settings

In `tv_shows_project/settings.py`, add `'shows'` to `INSTALLED_APPS`:

```python
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'shows',  # Add this line
]
```

### Step 5: Create Database

```bash
# Create migrations
python manage.py makemigrations

# Apply migrations
python manage.py migrate
```

### Step 6: Run Server

```bash
python manage.py runserver
```

Visit: **http://localhost:8000/shows/**

---

## Project Structure

```
tv_shows_project/
├── tv_shows_project/
│   ├── settings.py          # Django settings
│   ├── urls.py              # Main URL routing
│   ├── asgi.py
│   └── wsgi.py
│
├── shows/
│   ├── migrations/          # Database migrations
│   │   └── 0001_initial.py
│   │
│   ├── models.py            # Show model & ShowManager
│   ├── views.py             # CRUD view functions
│   ├── urls.py              # App URL routing
│   │
│   ├── templates/shows/
│   │   ├── base.html        # Base template (CSS + layout)
│   │   ├── index.html       # List all shows (READ)
│   │   ├── new.html         # Create form (CREATE)
│   │   ├── show.html        # Show details (READ ONE)
│   │   └── edit.html        # Edit form (UPDATE)
│   │
│   ├── admin.py             # Django admin configuration
│   ├── apps.py
│   └── tests.py
│
├── manage.py                # Django management script
├── db.sqlite3               # SQLite database
└── README.md                # This file
```

---

## Database Models

### Show Model

The `Show` model represents a television show with the following fields:

```python
class Show(models.Model):
    title = CharField(max_length=255)              # Show title
    network = CharField(max_length=100)            # Network name
    release_date = DateField()                     # Original air date
    description = TextField(blank=True, null=True) # Show description
    created_at = DateTimeField(auto_now_add=True)  # Creation timestamp
    updated_at = DateTimeField(auto_now=True)      # Last update timestamp
    
    objects = ShowManager()  # Custom manager
```

#### Fields Description

| Field | Type | Details |
|-------|------|---------|
| `title` | CharField | Max 255 characters, required |
| `network` | CharField | Max 100 characters, required |
| `release_date` | DateField | Cannot be future date |
| `description` | TextField | Optional, max 1000 characters |
| `created_at` | DateTimeField | Auto-set on creation |
| `updated_at` | DateTimeField | Auto-updated on save |

---

## Validation System

### ShowManager Custom Methods

The `ShowManager` class provides custom validation and CRUD methods:

#### 1. `create_validator(data)`

Validates show data and returns error dictionary.

**Parameters:**
- `data` (dict): Dictionary containing title, network, release_date, description

**Returns:**
- `errors` (dict): Dictionary of field errors (empty if valid)

**Validation Rules:**
```
Title:
  - Required
  - Minimum 2 characters
  - Maximum 255 characters

Network:
  - Required
  - Minimum 2 characters
  - Maximum 100 characters

Release Date:
  - Required
  - Valid date format (YYYY-MM-DD)
  - Cannot be future date

Description:
  - Optional
  - Maximum 1000 characters
```

**Example Usage:**
```python
data = {
    'title': 'Stranger Things',
    'network': 'Netflix',
    'release_date': '2016-07-15',
    'description': 'A sci-fi horror series...'
}

errors = Show.objects.create_validator(data)
# Returns: {} (if valid)
# Returns: {'title': 'Title is required'} (if invalid)
```

#### 2. `create_show(data)`

Creates a new show with validation.

**Returns:**
```python
{
    'success': True/False,
    'errors': {},  # Empty dict if successful
    'show': Show object or None
}
```

**Example:**
```python
result = Show.objects.create_show(data)

if result['success']:
    show = result['show']
    print(f"Created: {show.title}")
else:
    errors = result['errors']
    print(f"Error: {errors['title']}")
```

#### 3. `update_show(show_id, data)`

Updates an existing show with validation.

**Parameters:**
- `show_id` (int): ID of show to update
- `data` (dict): Updated show data

**Returns:**
Same structure as `create_show()`

---

## Views & Routing

### URL Structure (RESTful)

| HTTP | URL Path | View Function | Action |
|------|----------|---------------|--------|
| GET | `/shows/` | `shows_list` | List all shows |
| GET | `/shows/new/` | `shows_new` | Show create form |
| POST | `/shows/create/` | `shows_create` | Process create |
| GET | `/shows/<id>/` | `shows_detail` | Show details |
| GET | `/shows/<id>/edit/` | `shows_edit` | Show edit form |
| POST | `/shows/<id>/update/` | `shows_update` | Process update |
| GET | `/shows/<id>/delete/` | `shows_delete` | Delete show |

### View Functions

#### 1. `shows_list(request)` - READ ALL

Displays table of all shows with action links.

```python
# URL: GET /shows/
# Template: index.html
# Context: {'shows': queryset}
```

#### 2. `shows_new(request)` - CREATE FORM

Displays empty form for creating new show.

```python
# URL: GET /shows/new/
# Template: new.html
# Context: {'errors': {}, 'old_data': {}}
```

#### 3. `shows_create(request)` - CREATE PROCESS

Handles form submission and creates show.

```python
# URL: POST /shows/create/
# Validates data
# On success: Redirects to show detail page
# On error: Re-renders form with errors
```

#### 4. `shows_detail(request, pk)` - READ ONE

Displays complete show information.

```python
# URL: GET /shows/<id>/
# Template: show.html
# Context: {'show': Show object}
```

#### 5. `shows_edit(request, pk)` - UPDATE FORM

Displays form pre-filled with current show data.

```python
# URL: GET /shows/<id>/edit/
# Template: edit.html
# Context: {'show': Show, 'errors': {}, 'old_data': {...}}
```

#### 6. `shows_update(request, pk)` - UPDATE PROCESS

Handles form submission and updates show.

```python
# URL: POST /shows/<id>/update/
# Validates data
# On success: Redirects to show detail page
# On error: Re-renders form with errors
```

#### 7. `shows_delete(request, pk)` - DELETE

Deletes show from database.

```python
# URL: GET /shows/<id>/delete/
# Deletes show record
# Redirects to shows list
```

---

## Templates

All templates extend `base.html` which contains:
- HTML structure
- CSS styling
- Message display
- Common layout

### Template Files

#### 1. **base.html** - Base Layout

Contains:
- HTML5 boilerplate
- Complete CSS styling
- Message notification system
- Block for content injection

**CSS Features:**
- Clean, professional styling
- Form input styling
- Table styling with hover effects
- Button styling (primary, danger)
- Error message styling
- Responsive design

#### 2. **index.html** - List View

Displays all shows in table format.

**Features:**
- Table with: ID, Title, Network, Release Date, Actions
- "Add New Show" button link
- Show/Edit/Delete links for each row
- Handles empty state (no shows)

**Context:**
```python
{'shows': Show.objects.all()}
```

#### 3. **new.html** - Create Form

Form for creating new show.

**Form Fields:**
- Title (text input, required)
- Network (text input, required)
- Release Date (date input, required)
- Description (textarea, optional)

**Features:**
- Field validation error display
- Data persistence on error
- Create/Cancel buttons
- Back link

#### 4. **show.html** - Detail View

Displays full show information.

**Information Displayed:**
- Show ID and Title
- Network
- Release Date (formatted)
- Description
- Last Updated timestamp

**Actions Available:**
- Edit button
- Delete button
- Back to list button

#### 5. **edit.html** - Update Form

Form for editing existing show.

**Features:**
- Pre-filled with current show data
- Same fields as create form
- Field validation error display
- Update/Cancel buttons
- Back links

---

## Usage Guide

### Creating a Show

1. Navigate to **http://localhost:8000/shows/**
2. Click **"+ Add a New Show"** button
3. Fill in the form:
   - **Title**: Enter show title (2-255 characters)
   - **Network**: Enter network name (2-100 characters)
   - **Release Date**: Select date (cannot be today or future)
   - **Description**: Enter show description (optional, max 1000 chars)
4. Click **"Create"** button
5. On success, you'll be redirected to the show's detail page

**Example Data:**
```
Title: Stranger Things
Network: Netflix
Release Date: 2016-07-15
Description: A sci-fi horror series about a small town
```

### Viewing Shows

**List View:**
- Go to **http://localhost:8000/shows/**
- See all shows in a table
- Click "Show" link to view details

**Detail View:**
- Click "Show" link from list
- Or navigate directly: **http://localhost:8000/shows/1/**
- View all show information
- See last updated timestamp

### Editing a Show

1. Click **"Edit"** from list or detail page
2. Form appears pre-filled with current data
3. Modify any fields
4. Click **"Update"** button
5. On success, redirected to updated show's detail page

### Deleting a Show

1. Click **"Delete"** from list or detail page
2. Show is immediately removed
3. Redirected to shows list

---

## API Endpoints

### Summary

```
# Create a show
POST /shows/create/
  Parameters: title, network, release_date, description

# Read all shows
GET /shows/

# Read one show
GET /shows/<id>/

# Update a show
POST /shows/<id>/update/
  Parameters: title, network, release_date, description

# Delete a show
GET /shows/<id>/delete/
```

### Using cURL Examples

```bash
# Create show
curl -X POST http://localhost:8000/shows/create/ \
  -d "title=Breaking Bad&network=AMC&release_date=2008-01-20&description=Drug drama"

# View show
curl http://localhost:8000/shows/1/

# Delete show
curl http://localhost:8000/shows/1/delete/
```

---

## Error Handling

### Validation Error Messages

The system displays specific error messages for each field:

```
Title Errors:
  - "Title is required"
  - "Title must be at least 2 characters"
  - "Title must be less than 255 characters"

Network Errors:
  - "Network is required"
  - "Network must be at least 2 characters"
  - "Network must be less than 100 characters"

Release Date Errors:
  - "Release date is required"
  - "Release date cannot be in the future"
  - "Invalid date format"

Description Errors:
  - "Description must be less than 1000 characters"
```

### Error Display

- Errors display in red boxes below each field
- Form data is preserved on validation error
- User can correct mistakes and resubmit
- Error messages are descriptive and helpful

---

## Troubleshooting

### Issue: ModuleNotFoundError: No module named 'django'

**Solution:**
```bash
pip install django
```

### Issue: No migrations detected

**Solution:**
```bash
python manage.py makemigrations shows
python manage.py migrate
```

### Issue: Port 8000 already in use

**Solution:**
```bash
python manage.py runserver 8001  # Use different port
```

### Issue: Database locked error

**Solution:**
```bash
# Delete database and recreate
rm db.sqlite3
python manage.py migrate
```

### Issue: Template not found error

**Solution:**
- Ensure `'shows'` is in `INSTALLED_APPS`
- Check template paths are correct
- Restart Django server

### Issue: Form data not persisting on error

**Solution:**
- Check that `old_data` is passed in context
- Ensure template uses `{{ old_data.field_name }}`

### Issue: CSS not loading

**Solution:**
- CSS is inline in base.html (no static files needed)
- If styling is missing, check base.html is properly extended
- Verify no CSS syntax errors

---

## Django Admin

### Register Show Model (Optional)

In `shows/admin.py`:

```python
from django.contrib import admin
from .models import Show

@admin.register(Show)
class ShowAdmin(admin.ModelAdmin):
    list_display = ('title', 'network', 'release_date', 'created_at')
    search_fields = ('title', 'network')
    list_filter = ('network', 'release_date')
    readonly_fields = ('created_at', 'updated_at')
```

### Access Admin

1. Create superuser:
```bash
python manage.py createsuperuser
```

2. Login at:
```
http://localhost:8000/admin/
```

---

## Development Commands

```bash
# Start development server
python manage.py runserver

# Create superuser
python manage.py createsuperuser

# Make migrations
python manage.py makemigrations

# Apply migrations
python manage.py migrate

# Run tests (if created)
python manage.py test

# Django shell
python manage.py shell

# Collect static files
python manage.py collectstatic

# Reset database
rm db.sqlite3
python manage.py migrate
```

---

## Future Enhancements

### Potential Features

- [ ] User authentication & authorization
- [ ] Search functionality
- [ ] Pagination for large datasets
- [ ] Show ratings/reviews system
- [ ] Image uploads for show posters
- [ ] Filter by network
- [ ] Sort by release date
- [ ] Show statistics/dashboard
- [ ] Export to CSV/PDF
- [ ] REST API endpoints
- [ ] Mobile app
- [ ] Email notifications
- [ ] Comments/discussions
- [ ] Favorites/watchlist
- [ ] Advanced search filters

### Performance Improvements

- [ ] Database indexing
- [ ] Caching system
- [ ] Pagination
- [ ] Query optimization
- [ ] Static file CDN

### Code Quality

- [ ] Unit tests
- [ ] Integration tests
- [ ] Code coverage
- [ ] API documentation
- [ ] Type hints

---

## Contributing

This is a learning project. Feel free to:
- Fork and modify
- Add new features
- Improve validation
- Enhance UI
- Add tests

---

## License

This project is open source and available for educational purposes.

---

## Support & Questions

For issues or questions:
1. Check the Troubleshooting section
2. Review code comments
3. Test with simple data first
4. Check Django documentation

---

## Summary

This TV Shows CRUD application demonstrates:
- ✅ Django fundamentals
- ✅ Custom model managers
- ✅ Form validation without Django Forms
- ✅ RESTful routing conventions
- ✅ Template inheritance
- ✅ Error handling
- ✅ Clean code practices
- ✅ User-friendly interface

Perfect for learning Django or as a foundation for larger projects!

---

**Last Updated:** 2024  
**Django Version:** 6.0+  
**Python Version:** 3.8+