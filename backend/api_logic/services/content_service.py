from sqlite3 import IntegrityError
from rest_framework.exceptions import ValidationError
from api_logic.serializers import AuthorSerializer
from api_logic.utils import ContentUtils
from api_logic.models import Content, Author


def create_content(content_data):
    """
    Create a new content item.
    """
    try:
        ContentUtils.validate_content_data(
            title=content_data.get('title', ''),
            body=content_data.get('body', ''),
            author=content_data.get('author', '')
        )
        content = Content.objects.create(
            title=content_data.get('title', ''),
            body=content_data.get('body', ''),
            author=content_data.get('author', '')
        )
        return content
    except IntegrityError as e:
        raise ValidationError(f"Content creation failed: {str(e)}")


def get_content_by_id(id):
    """
    Retrieve a content item by its ID.
    """
    try:
        content = Content.objects.get(id=id)
        return content
    except Content.DoesNotExist:
        raise ValidationError("Content not found.")
    except Exception as e:
        raise ValidationError(f"Failed to retrieve content: {str(e)}")


def update_content(content_id, new_content_data):
    """
    Update an existing content item.
    """
    try:
        content = Content.objects.get(id=content_id)
        serializer = AuthorSerializer(
            content, data=new_content_data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return serializer.data
        else:
            raise ValidationError(serializer.errors)
    except Content.DoesNotExist:
        raise ValidationError("Content not found.")
    except Exception as e:
        raise ValidationError(f"Failed to update content: {str(e)}")


def delete_content(content_id):
    """
    Delete a content item by its ID.
    """
    try:
        content = Content.objects.get(id=content_id)
        content.delete()
        return {"detail": "Content deleted successfully."}
    except Content.DoesNotExist:
        raise ValidationError("Content not found.")
    except Exception as e:
        raise ValidationError(f"Failed to delete content: {str(e)}")


def get_all_content():
    """
    Retrieve all content items.
    """
    try:
        content_list = Content.objects.all()
        return content_list
    except Exception as e:
        raise ValidationError(f"Failed to retrieve content: {str(e)}")


def get_content_by_author(author_id):
    """
    Retrieve all content items by a specific author.
    """
    try:
        author = Author.objects.get(id=author_id)
        content_list = Content.objects.filter(author=author)
        return content_list
    except Author.DoesNotExist:
        raise ValidationError("Author not found.")
    except Exception as e:
        raise ValidationError(
            f"Failed to retrieve content by author: {str(e)}")
