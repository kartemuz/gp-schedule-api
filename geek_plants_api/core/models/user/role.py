from geek_plants_api.core.models.user.opportunity import Opportunity


class Role:
    name: str
    opportunities: list[Opportunity]
