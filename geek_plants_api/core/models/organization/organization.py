from geek_plants_api.core.models.organization.social_network import SocialNetwork


class Organization:
    address: str
    phone: str
    email: str

    social_networks: list[SocialNetwork]

    def __init__(self, address: str, phone: str, email: str, social_networks: list[SocialNetwork]):
        self.address = address
        self.phone = phone
        self.email = email
        self.social_networks = social_networks
