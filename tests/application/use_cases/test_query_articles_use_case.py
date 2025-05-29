import pytest
from unittest.mock import AsyncMock, MagicMock
from types import SimpleNamespace

from application.use_cases.query_articles_use_case import QueryArticleUseCase
from application.models.related_article_dto import RelatedArticleDTO

@pytest.mark.asyncio
async def test_query_article_use_case_returns_expected_results():
    # Arrange
    fake_query = "climate change"
    enhanced_query = "climate change impact"
    fake_results = [(SimpleNamespace(**{"metadata": {"headline": "Article 1",  "content":"content", "summary": "test"}}), 0.9),
                    (SimpleNamespace(**{"metadata": {"headline": "Article 2",  "content":"content", "summary": "test"}}), 0.8)]
    expected_dtos = [RelatedArticleDTO(headline="Article 1", content="content", summary="test", score=0.9),
                     RelatedArticleDTO(headline="Article 2", content="content", summary="test", score=0.8)]
    
    mock_repo = MagicMock()
    mock_repo.query_async = AsyncMock(return_value=fake_results)

    mock_enhancer = MagicMock()
    mock_enhancer.enhance_async = AsyncMock(return_value=enhanced_query)

    # Act
    use_case = QueryArticleUseCase(repo=mock_repo, query_enhancer=mock_enhancer)
    result = await use_case(fake_query)

    # Assert
    mock_enhancer.enhance_async.assert_awaited_once_with(fake_query)
    mock_repo.query_async.assert_awaited_once_with(enhanced_query)
    assert result == expected_dtos

@pytest.mark.asyncio
async def test_empty_query_returns_no_results():
    # Arrange
    query = ""
    enhanced_query = ""
    mock_repo = MagicMock()
    mock_repo.query_async = AsyncMock(return_value=[])

    mock_enhancer = MagicMock()
    mock_enhancer.enhance_async = AsyncMock(return_value=enhanced_query)

    use_case = QueryArticleUseCase(repo=mock_repo, query_enhancer=mock_enhancer)

    # Act
    result = await use_case(query)

    # Assert
    assert result == []
    mock_enhancer.enhance_async.assert_awaited_once_with(query)
    mock_repo.query_async.assert_awaited_once_with(enhanced_query)
    
@pytest.mark.asyncio
async def test_enhancer_returns_same_query():
    # Arrange
    query = "machine learning"
    mock_repo = MagicMock()
    mock_repo.query_async = AsyncMock(return_value=[({"title": "ML Paper"}, 0.95)])

    mock_enhancer = MagicMock()
    mock_enhancer.enhance_async = AsyncMock(return_value=query)

    dto_mock = MagicMock(spec=RelatedArticleDTO)
    RelatedArticleDTO.from_document = MagicMock(return_value=dto_mock)

    use_case = QueryArticleUseCase(repo=mock_repo, query_enhancer=mock_enhancer)

    # Act
    result = await use_case(query)

    # Assert
    assert result == [dto_mock]
    mock_enhancer.enhance_async.assert_awaited_once_with(query)
    mock_repo.query_async.assert_awaited_once_with(query)
    RelatedArticleDTO.from_document.assert_called_once()
    
@pytest.mark.asyncio
async def test_repo_returns_empty_list():
    # Arrange
    query = "nonexistent topic"
    enhanced_query = "nonexistent topic enhanced"

    mock_repo = MagicMock()
    mock_repo.query_async = AsyncMock(return_value=[])

    mock_enhancer = MagicMock()
    mock_enhancer.enhance_async = AsyncMock(return_value=enhanced_query)

    use_case = QueryArticleUseCase(repo=mock_repo, query_enhancer=mock_enhancer)
    
    # Act
    result = await use_case(query)

    # Assert
    assert result == []
    mock_enhancer.enhance_async.assert_awaited_once_with(query)
    mock_repo.query_async.assert_awaited_once_with(enhanced_query)
    
@pytest.mark.asyncio
async def test_enhancer_raises_exception():
    # Arrange
    query = "query"

    mock_repo = MagicMock()
    mock_enhancer = MagicMock()
    mock_enhancer.enhance_async = AsyncMock(side_effect=Exception("Enhancer error"))

    use_case = QueryArticleUseCase(repo=mock_repo, query_enhancer=mock_enhancer)

    # Act & Assert
    with pytest.raises(Exception, match="Enhancer error"):
        await use_case(query)

    mock_enhancer.enhance_async.assert_awaited_once_with(query)
    mock_repo.query_async.assert_not_called()
    
@pytest.mark.asyncio
async def test_repo_raises_exception():
    # Arrange
    query = "economy"
    enhanced_query = "global economy"

    mock_enhancer = MagicMock()
    mock_enhancer.enhance_async = AsyncMock(return_value=enhanced_query)

    mock_repo = MagicMock()
    mock_repo.query_async = AsyncMock(side_effect=Exception("Repo error"))

    # Act & Assert
    use_case = QueryArticleUseCase(repo=mock_repo, query_enhancer=mock_enhancer)

    with pytest.raises(Exception, match="Repo error"):
        await use_case(query)

    mock_enhancer.enhance_async.assert_awaited_once_with(query)
    mock_repo.query_async.assert_awaited_once_with(enhanced_query)
