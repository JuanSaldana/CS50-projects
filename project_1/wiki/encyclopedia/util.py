import re
import markdown2
from django.core.files.base import ContentFile
from django.core.files.storage import default_storage


def list_entries():
    """
    Returns a list of all names of encyclopedia entries.
    """
    _, filenames = default_storage.listdir("entries")
    return list(sorted(re.sub(r"\.md$", "", filename)
                for filename in filenames if filename.endswith(".md")))


def save_entry(title, content):
    """
    Saves an encyclopedia entry, given its title and Markdown
    content. If an existing entry with the same title already exists,
    it is replaced.
    """
    filename = f"entries/{title}.md"
    if default_storage.exists(filename):
        default_storage.delete(filename)
    default_storage.save(filename, ContentFile(content))


def get_entry(title):
    """
    Retrieves an encyclopedia entry by its title. If no such
    entry exists, the function returns None.
    """
    try:
        f = default_storage.open(f"entries/{title}.md")
        return f.read().decode("utf-8")
    except FileNotFoundError:
        f = default_storage.open("entries/error/NOTFOUND.md")
        return f.read().decode("utf-8")


def render_entry(title):
    """
    Renders an encyclopedia entry.
    """
    entry = get_entry(title)
    # if entry is None:
    #     return open("encyclopedia/templates/encyclopedia/notfound.html").read()
    return markdown2.markdown(entry)


def search_entry(title: str):
    """
    Searches for an entry in the encyclopedia.
    """
    entries = list_entries()
    matching_entries = [
        entry for entry in entries if title.lower() in entry.lower()] or None

    if matching_entries and title in matching_entries:
        return title
    else:
        return matching_entries
