from pydantic import BaseModel
from typing import Any, Optional


class ITDRRecordSchema(BaseModel):

    source: str
    raw_data: Optional[dict[str, Any]] = None