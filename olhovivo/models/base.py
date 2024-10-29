class Base:
    """
    Classe base para mapeamento de atributos de dicionários JSON para atributos de objeto.
    """

    _mapping: dict = {}

    def __init__(self, kwargs: dict) -> None:
        """
        Inicializa um objeto base mapeando os valores do dicionário para os atributos do objeto.

        Args:
            kwargs (dict): Dicionário de dados onde as chaves correspondem aos valores dos atributos
                           mapeados por `_mapping`.
        """

        for attr, key in self._mapping.items():
            setattr(self, attr, kwargs.get(key))
