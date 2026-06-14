from django.db import models

# Create your models here.
from django.db import models
from datetime import date


class ShowManager(models.Manager):
    """Custom manager with validation"""

    def create_validator(self, data):
        """Validate show data and return errors dictionary"""
        errors = {}

        title = data.get('title', '').strip()
        network = data.get('network', '').strip()
        release_date = data.get('release_date')
        description = data.get('description', '').strip()

        # Title validation
        if not title:
            errors['title'] = 'Title is required'
        elif len(title) < 2:
            errors['title'] = 'Title must be at least 2 characters'
        elif len(title) > 255:
            errors['title'] = 'Title must be less than 255 characters'

        # Network validation
        if not network:
            errors['network'] = 'Network is required'
        elif len(network) < 2:
            errors['network'] = 'Network must be at least 2 characters'
        elif len(network) > 100:
            errors['network'] = 'Network must be less than 100 characters'

        # Release date validation
        if not release_date:
            errors['release_date'] = 'Release date is required'
        else:
            try:
                # If it's a string, convert to date
                if isinstance(release_date, str):
                    from datetime import datetime
                    release_date = datetime.strptime(release_date, '%Y-%m-%d').date()

                if release_date > date.today():
                    errors['release_date'] = 'Release date cannot be in the future'
            except:
                errors['release_date'] = 'Invalid date format'

        # Description validation (optional but max length)
        if description and len(description) > 1000:
            errors['description'] = 'Description must be less than 1000 characters'

        return errors

    def create_show(self, data):
        """Create show if no validation errors"""
        errors = self.create_validator(data)

        if errors:
            return {'success': False, 'errors': errors, 'show': None}

        title = data.get('title', '').strip()
        network = data.get('network', '').strip()
        release_date = data.get('release_date')
        description = data.get('description', '').strip()

        if isinstance(release_date, str):
            from datetime import datetime
            release_date = datetime.strptime(release_date, '%Y-%m-%d').date()

        show = self.create(
            title=title,
            network=network,
            release_date=release_date,
            description=description
        )

        return {'success': True, 'errors': {}, 'show': show}

    def update_show(self, show_id, data):
        """Update show with validation"""
        errors = self.create_validator(data)

        if errors:
            return {'success': False, 'errors': errors, 'show': None}

        try:
            show = self.get(id=show_id)
            show.title = data.get('title', '').strip()
            show.network = data.get('network', '').strip()

            release_date = data.get('release_date')
            if isinstance(release_date, str):
                from datetime import datetime
                release_date = datetime.strptime(release_date, '%Y-%m-%d').date()
            show.release_date = release_date

            show.description = data.get('description', '').strip()
            show.save()

            return {'success': True, 'errors': {}, 'show': show}
        except:
            return {'success': False, 'errors': {'general': 'Show not found'}, 'show': None}


class Show(models.Model):
    title = models.CharField(max_length=255)
    network = models.CharField(max_length=100)
    release_date = models.DateField()
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = ShowManager()

    class Meta:
        ordering = ['id']
        verbose_name_plural = "Shows"

    def __str__(self):
        return f"{self.title} ({self.network})"

    def get_formatted_date(self):
        """Return date in readable format"""
        return self.release_date.strftime('%B %d, %Y')