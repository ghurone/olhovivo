from olhovivo.models.base import Base


class Veiculo(Base):
    """
    Classe para representar um veículo de transporte público.

    Attributes:
        prefixo (int): Prefixo do veículo.
        acessibilidade (bool): Indica se o veículo é acessível para pessoas com deficiência.
        hora_posicao (str): Horário de captura da posição no formato ISO 8601.
        latitude (float): Latitude da posição do veículo.
        longitude (float): Longitude da posição do veículo.
    """

    _mapping = {
        'prefixo': 'p',
        'acessibilidade': 'a',
        'hora_posicao': 'ta',
        'latitude': 'py',
        'longitude': 'px'
    }

    def __str__(self) -> str:
        return f'Veiculo({self.prefixo} ({self.latitude}, {self.longitude}))'

    def __repr__(self) -> str:
        return self.__str__()
