from django.test import TestCase, Client
from django.urls import reverse
from django.core.exceptions import ValidationError
from .models import Note
from .forms import NoteForm


class NoteModelTestCase(TestCase):
    """Test cases for the Note model."""

    def test_note_creation_success(self):
        """Test that a note can be created successfully with valid data."""
        note = Note.objects.create(
            title="Test Note",
            description="This is a valid test description with enough characters."
        )
        self.assertEqual(note.title, "Test Note")
        self.assertIn("valid test description", note.description)
        self.assertIsNotNone(note.created_at)

    def test_note_creation_short_description(self):
        """Test that an error occurs if description is less than 10 characters."""
        with self.assertRaises(ValidationError):
            note = Note(
                title="Test Note",
                description="Short"
            )
            note.save()

    def test_note_clean_method(self):
        """Test that clean method validates description length."""
        note = Note(
            title="Test Note",
            description="Short"
        )
        with self.assertRaises(ValidationError) as context:
            note.clean()
        self.assertIn('description', context.exception.error_dict)

    def test_note_string_representation(self):
        """Test that note __str__ returns the title."""
        note = Note.objects.create(
            title="Test Title",
            description="This is a valid description with enough length."
        )
        self.assertEqual(str(note), "Test Title")

    def test_note_ordering(self):
        """Test that notes are ordered by creation date (newest first)."""
        note1 = Note.objects.create(
            title="Note 1",
            description="First note with valid description length."
        )
        note2 = Note.objects.create(
            title="Note 2",
            description="Second note with valid description length."
        )
        notes = Note.objects.all()
        self.assertEqual(notes[0].id, note2.id)
        self.assertEqual(notes[1].id, note1.id)


class NoteFormTestCase(TestCase):
    """Test cases for the NoteForm."""

    def test_form_valid_data(self):
        """Test that form is valid with correct data."""
        form_data = {
            'title': 'Test Note',
            'description': 'This is a valid test description.'
        }
        form = NoteForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_form_short_description(self):
        """Test that form validation catches short description."""
        form_data = {
            'title': 'Test Note',
            'description': 'Short'
        }
        form = NoteForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('description', form.errors)
        self.assertIn('at least 10 characters', str(form.errors['description']))

    def test_form_exactly_10_characters(self):
        """Test that form accepts description with exactly 10 characters."""
        form_data = {
            'title': 'Test Note',
            'description': '1234567890'  # Exactly 10 characters
        }
        form = NoteForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_form_missing_title(self):
        """Test that form is invalid without title."""
        form_data = {
            'title': '',
            'description': 'This is a valid description.'
        }
        form = NoteForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('title', form.errors)

    def test_form_missing_description(self):
        """Test that form is invalid without description."""
        form_data = {
            'title': 'Test Note',
            'description': ''
        }
        form = NoteForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('description', form.errors)


class NoteViewTestCase(TestCase):
    """Test cases for note views."""

    def setUp(self):
        """Set up test client and sample data."""
        self.client = Client()
        self.note = Note.objects.create(
            title="Test Note",
            description="This is a valid test description for testing."
        )

    def test_note_list_view(self):
        """Test that note list view returns correct data."""
        response = self.client.get(reverse('note_list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.note.title)
        self.assertTemplateUsed(response, 'notes/note_list.html')

    def test_note_detail_view(self):
        """Test that note detail view displays correct note."""
        response = self.client.get(reverse('note_detail', args=[self.note.id]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.note.title)
        self.assertContains(response, self.note.description)
        self.assertTemplateUsed(response, 'notes/note_detail.html')

    def test_create_note_view_get(self):
        """Test that create note view returns form on GET."""
        response = self.client.get(reverse('create_note'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'notes/create_note.html')
        self.assertIsInstance(response.context['form'], NoteForm)

    def test_create_note_view_post_valid(self):
        """Test that valid POST creates a note and redirects."""
        data = {
            'title': 'New Note',
            'description': 'This is a new valid test description.'
        }
        response = self.client.post(reverse('create_note'), data)
        self.assertEqual(response.status_code, 302)  # Redirect
        self.assertTrue(Note.objects.filter(title='New Note').exists())

    def test_create_note_view_post_invalid(self):
        """Test that invalid POST shows form with errors."""
        data = {
            'title': 'Test',
            'description': 'Short'  # Too short
        }
        response = self.client.post(reverse('create_note'), data)
        self.assertEqual(response.status_code, 200)  # No redirect
        self.assertFormError(response, 'form', 'description', 'Description must be at least 10 characters long.')

    def test_create_note_view_empty_title(self):
        """Test that empty title causes form error."""
        data = {
            'title': '',
            'description': 'This is a valid description.'
        }
        response = self.client.post(reverse('create_note'), data)
        self.assertEqual(response.status_code, 200)
        self.assertTrue('title' in response.context['form'].errors or 'form' in response.context)


class NoteIntegrationTestCase(TestCase):
    """Integration tests for the notes app."""

    def test_complete_workflow(self):
        """Test complete workflow: create note, view list, view detail."""
        # Create a note via POST
        data = {
            'title': 'Integration Test Note',
            'description': 'This is a test note created during integration testing.'
        }
        response = self.client.post(reverse('create_note'), data)
        self.assertEqual(response.status_code, 302)

        # Verify note appears in list
        response = self.client.get(reverse('note_list'))
        self.assertContains(response, 'Integration Test Note')

        # Get the created note
        note = Note.objects.get(title='Integration Test Note')

        # View note detail
        response = self.client.get(reverse('note_detail', args=[note.id]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, note.description)

    def test_validation_flow(self):
        """Test validation error handling in the workflow."""
        # Attempt to create note with short description
        data = {
            'title': 'Invalid Note',
            'description': 'Bad'
        }
        response = self.client.post(reverse('create_note'), data)
        self.assertEqual(response.status_code, 200)
        self.assertFormError(response, 'form', 'description', 'Description must be at least 10 characters long.')
        
        # Verify note was not created
        self.assertFalse(Note.objects.filter(title='Invalid Note').exists())
