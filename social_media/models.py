from django.db import models
import uuid


class Post(models.Model):
    unique_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, db_index=True)
    content = models.TextField()

    def __str__(self):
        return str(self.unique_id)
