from olhovivo.models.base import Base
from olhovivo.models.veiculo import Veiculo


class ParadaBase(Base):
    """
    Classe base para representar uma parada de ônibus.

    Attributes:
        codigo (int): Código identificador da parada.
        nome (str): Nome da parada.
        endereco (str): Endereço de localização da parada.
        latitude (float): Latitude da parada.
        longitude (float): Longitude da parada.
    """

    _mapping = {
        'codigo': 'cp',
        'nome': 'np',
        'endereco': 'ed',
        'latitude': 'py',
        'longitude': 'px'
    }

    def __str__(self) -> str:
        return f'Parada({self.nome} - ({self.latitude}, {self.longitude}))'

    def __repr__(self) -> str:
        return self.__str__()


class Parada(ParadaBase):
    """
    Classe para representar uma parada de ônibus com veículos em operação.

    Attributes:
        Todos os atributos de ParadaBase.
        _veiculos (list[dict]): Lista de dicionários com dados dos veículos na parada.
    """

    _mapping = ParadaBase._mapping.copy()
    _mapping.update({
        '_veiculos': 'vs',
    })

    def __init__(self, kwargs):
        super().__init__(kwargs)

    def get_veiculos(self) -> list[Veiculo]:
        return [Veiculo(veiculo) for veiculo in self._veiculos]
