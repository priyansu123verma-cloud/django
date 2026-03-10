from django.db import models


class Note(models.Model):
    """
    Note model with title and description fields.
    Description must be at least 10 characters long.
    """
    title = models.CharField(max_length=200)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def clean(self):
        """Validate that description is at least 10 characters long."""
        from django.core.exceptions import ValidationError
        if len(self.description) < 10:
            raise ValidationError(
                {'description': 'Description must be at least 10 characters long.'}
            )

    def save(self, *args, **kwargs):
        """Clean and save the model."""
        self.clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name_plural = "Notes"
        ordering = ['-created_at']
