from pydantic import BaseModel


class CensysResponse(BaseModel):

    host: str
    technologies: str
    protocols: str
    titles: str
    source: str
