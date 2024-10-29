from olhovivo.models.base import Base
from olhovivo.models.veiculo import Veiculo


class LinhaBase(Base):
    """
    Classe base para representar informações de linhas de ônibus.

    Attributes:
        codigo (int): Código identificador da linha.
        circular (bool): Indicador se a linha é circular.
        numero (str): Número da linha.
        sentido (int): Sentido da operação da linha.
        modo (int): Tipo de operação da linha.
        terminal_principal (str): Nome do terminal principal da linha.
        terminal_secundario (str): Nome do terminal secundário da linha.
        nome (str): Nome da linha no sentido especificado.
    """

    _mapping = {
        'codigo': 'cl',
        'circular': 'lc',
        'numero': 'lt',
        'sentido': 'sl',
        'modo': 'tl',
        'terminal_principal': 'tp',
        'terminal_secundario': 'ts'
    }

    def __init__(self, kwargs: dict):
        super().__init__(kwargs)
        self.nome = self.terminal_principal if self.sentido == 2 else self.terminal_secundario

    def __str__(self) -> str:
        return f'Onibus({self.numero}-{self.modo} {self.nome})'

    def __repr__(self) -> str:
        return self.__str__()


class Linha(LinhaBase):
    """
    Classe para representar o movimento de uma linha com veículos em operação.

    Attributes:
        Todos os atributos de LinhaBase.

        saida (str): Letreiro de destino da linha.
        chegada (str): Letreiro de origem da linha.
        quantidade_veiculos (int): Quantidade de veículos localizados.
        _veiculos (list[dict]): Lista de dicionários com dados dos veículos.
    """

    _mapping = LinhaBase._mapping.copy()
    _mapping.update({
        '_numero_modo': 'c',
        'saida': 'lt1',
        'chegada': 'lt0',
        'quantidade_veiculos': 'qv',
        '_veiculos': 'vs'
    })

    def __init__(self, kwargs):
        super().__init__(kwargs)
        self.numero, self.modo = self._numero_modo.split('-')
        self.terminal_principal = self.saida if self.sentido == 1 else self.chegada
        self.terminal_secundario = self.chegada if self.sentido == 1 else self.saida

    def __str__(self) -> str:
        return f'LinhaMovimento({self.numero}-{self.modo} {self.saida} -> {self.chegada})'

    def __repr__(self) -> str:
        return self.__str__()

    def get_veiculos(self) -> list[Veiculo]:
        return [Veiculo(veiculo) for veiculo in self._veiculos]
