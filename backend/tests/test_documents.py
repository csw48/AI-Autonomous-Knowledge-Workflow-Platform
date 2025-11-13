import pytest


@pytest.mark.asyncio
async def test_document_service_roundtrip(db_session):
    from backend.app.services.documents import DocumentService

    service = DocumentService(db_session)

    await service.create_document(
        title="Spec",
        source="markdown.md",
        chunks=["hello world", "second chunk"],
        embeddings=[[0.1, 0.2], [0.3, 0.4]],
    )

    documents = await service.list_documents()
    assert len(documents) == 1
    assert documents[0].chunks[0].content == "hello world"
