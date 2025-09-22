import uuid as uuid
from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):
    zipcode = models.CharField(blank=True, max_length=5)
    nni = models.CharField(max_length=20, null=True, blank=True)
    uuid = models.UUIDField(
        db_index=True,
        default=uuid.uuid4,
        unique=True,
        editable=False,
    )



