from pydantic import ConfigDict, BaseModel
from pydantic.alias_generators import to_camel


class StandardModel(BaseModel):
    """A standard Pydantic model that all other models can inherit from."""
    model_config = ConfigDict(
        str_strip_whitespace=True,
        alias_generator=to_camel,
        populate_by_name=True,
    )
