from django.core.exceptions import ValidationError
from dateutil.relativedelta import relativedelta
from django.utils import timezone

def validate_image(img):
    size = img.size
    format = img.name.split(".")[-1]

    avaible_formats = [
        'png',
        'jpeg',
        'jpg',
    ]

    if size > 4194304:
        raise ValidationError("Image size must be less than 4MB")
    if format not in avaible_formats:
        raise ValidationError("Image extension is not avaible")    
    return img

def validate_date_of_birth(date):
    if date > timezone.now() - relativedelta(years=16):
        raise ValidationError("You have to be at least 16 years old.")
    return date