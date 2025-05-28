from typing import List
from src.application.models.related_article_dto import RelatedArticleDTO

def map_articles_from_vector_db(
    articles_with_scores: List[tuple[object, float]]
) -> List[RelatedArticleDTO]:
    mapped_articles = []
    for article, score in articles_with_scores:
        metadata = getattr(article, "metadata", {})

        topics = metadata.get("topics", None)

        # Convert topics from comma-separated string to list if needed
        if isinstance(topics, str):
            topics = [t.strip() for t in topics.split(",") if t.strip()]

        dto = RelatedArticleDTO(
            headline=metadata.get("headline"),
            summary=metadata.get("summary", ""),
            topics=topics,
            political_bias=metadata.get("political_bias"),
            score=score
        )
        mapped_articles.append(dto)

    return mapped_articles
