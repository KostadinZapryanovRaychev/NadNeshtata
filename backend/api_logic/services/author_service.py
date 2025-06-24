from sqlite3 import IntegrityError
from django.contrib.auth.models import User
from rest_framework.exceptions import ValidationError
from api_logic.serializers import AuthorSerializer
from api_logic.utils import AuthorUtils
from api_logic.models import Author


def create_author(autho_data):
    """
    Create an author profile for a user.
    """
    try:
        AuthorUtils.validate_author_data(
            user=autho_data.get('user', ''),
            bio=autho_data.get('bio', ''),
            profile_picture=autho_data.get('profile_picture', '')
        )
        author = Author.objects.create(
            user=autho_data.get('user', ''),
            bio=autho_data.get('bio', ''),
            profile_picture=autho_data.get('profile_picture', '')
        )
        return author
    except IntegrityError as e:
        raise ValidationError(f"User creation failed: {str(e)}")


def get_author_by_id(id):
    """
    Retrieve an author profile by its ID.
    """
    try:
        author = Author.objects.get(id=id)
        return author
    except Author.DoesNotExist:
        raise ValidationError("Author not found.")
    except Exception as e:
        raise ValidationError(f"Failed to retrieve author: {str(e)}")


def update_author(author_id, new_author_data):
    """
    Update an existing author profile.
    """
    try:
        author = Author.objects.get(id=author_id)
        serializer = AuthorSerializer(
            author, data=new_author_data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return serializer.data
        else:
            raise ValidationError(serializer.errors)
    except Author.DoesNotExist:
        raise ValidationError("Author not found.")
    except Exception as e:
        raise ValidationError(f"Failed to update author: {str(e)}")


def delete_author(author_id):
    """
    Delete an author profile by its ID.
    """
    try:
        author = Author.objects.get(id=author_id)
        author.delete()
        return {"message": "Author deleted successfully."}
    except Author.DoesNotExist:
        raise ValidationError("Author not found.")
    except Exception as e:
        raise ValidationError(f"Failed to delete author: {str(e)}")


def get_all_authors():
    """
    Retrieve all authors in the system.
    """
    try:
        authors = Author.objects.all()
        serializer = AuthorSerializer(authors, many=True)
        return serializer.data
    except Exception as e:
        raise ValidationError(f"Failed to retrieve authors: {str(e)}")
