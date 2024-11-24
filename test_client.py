import pytest
import asyncio
from client import process_response

@pytest.mark.asyncio
async def test_process_response():
    """Test the analysis logic."""
    test_message = "This is an AI-related response."
    feedback = await process_response(test_message)
    assert "score" in feedback
    assert "feedback" in feedback
    assert isinstance(feedback["score"], int)
    assert isinstance(feedback["feedback"], str)
