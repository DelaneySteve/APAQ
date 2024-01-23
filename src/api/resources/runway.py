from pydantic import BaseModel
# from api.resources.enumerations import RunwaySurface

class Runway(BaseModel):
    length: int
    # surface: RunwaySurface
