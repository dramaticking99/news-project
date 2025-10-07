from typing import List
from .mongodb import get_database
from ..models.article import Article

async def get_articles_batch(skip: int = 0, limit: int = 20) -> List[Article]:
    """
    Retrieves a paginated list of articles from the database.

    Args:
        skip (int): The number of articles to skip (for pagination).
        limit (int): The maximum number of articles to return.

    Returns:
        A list of Article objects.
    """
    db = await get_database()
    articles_collection = db["articles"]
    
    # The find() method returns a cursor that we can iterate over
    cursor = articles_collection.find().skip(skip).limit(limit)
    
    # Use a list comprehension to build the list of articles
    articles = [Article(**raw_article) async for raw_article in cursor]
    
    return articles