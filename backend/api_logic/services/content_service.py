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
        name = content_data.get('name', '').strip()
        description = content_data.get('description', '').strip()
        author_id = content_data.get('author_id')

        ContentUtils.validate_content_data(
            name=name,
            description=description,
            author_id=author_id
        )

        author = Author.objects.get(id=author_id)

        content = Content.objects.create(
            name=name,
            description=description,
            author=author,
            url=content_data.get('url', ''),
            thumbnail=content_data.get('thumbnail', '')
        )

        return content

    except Author.DoesNotExist:
        raise ValidationError({"author": "Author not found."})
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


def update_content(content_id, content_data):
    """
    Update an existing content item.
    """
    try:
        content = Content.objects.get(id=content_id)

        name = content_data.get('name', '').strip()
        description = content_data.get('description', '').strip()
        author_id = content_data.get('author_id')

        ContentUtils.validate_content_data(
            name=name,
            description=description,
            author_id=author_id
        )

        if author_id:
            author = Author.objects.get(id=author_id)
            content.author = author

        content.name = name
        content.description = description
        content.url = content_data.get('url', content.url)
        content.thumbnail = content_data.get('thumbnail', content.thumbnail)
        content.save()

        return content

    except Author.DoesNotExist:
        raise ValidationError({"author": "Author not found."})
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
