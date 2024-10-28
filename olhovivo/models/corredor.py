from olhovivo.models.base import Base


class Corredor(Base):
    """
    Classe para representar um corredor de ônibus.

    Attributes:
        codigo (int): Código identificador do corredor.
        nome (str): Nome do corredor.
    """

    _mapping = {
        'codigo': 'cc',
        'nome': 'nc'
    }

    def __str__(self) -> str:
        return f'Corredor({self.nome} ({self.codigo}))'

    def __repr__(self) -> str:
        return self.__str__()
