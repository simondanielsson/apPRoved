from pydantic import BaseModel


class ReviewResponse(BaseModel):
    """Resposne for a review."""

    review_id: int
    review_contents: list[str]
    file_names: list[str]
