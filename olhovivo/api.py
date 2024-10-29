from time import sleep
from typing import Optional

import requests

from olhovivo.utils import join_urls
from olhovivo.models.corredor import Corredor
from olhovivo.models.linha import LinhaBase, Linha
from olhovivo.models.parada import ParadaBase, Parada
from olhovivo.models.veiculo import Veiculo


class OlhoVivoAPI:
    """
    Classe para interagir com a API Olho Vivo da SPTrans, fornecendo acesso a informações sobre linhas,
    paradas, corredores, veículos e previsões de chegada de ônibus na cidade de São Paulo.
    """

    def __init__(self, n_tries: int = 5, sec_wait: int = 1) -> None:
        """
        Inicializa a classe com número de tentativas e tempo de espera entre requisições.

        Args:
            n_tries (int): Número de tentativas de requisição em caso de falha.
            sec_wait (int): Tempo de espera entre as tentativas em segundos.
        """

        self._base_url = 'https://olhovivo.sptrans.com.br/'
        self._api_url = join_urls(self._base_url, 'data')

        self._restart_session()

        self.n_tries = n_tries
        self.sec_wait = sec_wait

    def _gen_session(self) -> None:
        """
        Gera uma nova sessão de requisição para a API, incluindo headers com User-Agent.
        """

        self._session = requests.Session()
        self._session.headers.update({'User-Agent': 'sptransapi/0.0.1'})

    def _gen_cookies(self) -> None:
        """
        Solicita cookies iniciais da base URL para manter a sessão.
        """

        self._session.get(self._base_url)

    def _restart_session(self) -> None:
        """
        Reinicia a sessão, regenerando cookies e sessão HTTP.
        """

        self._gen_session()
        self._gen_cookies()

    def _get(self, url: str,
             params: Optional[dict] = None) -> requests.Response | None:
        """
        Faz uma requisição GET à API com o número de tentativas configurado.

        Args:
            url (str): URL completa da requisição.
            params (dict, opcional): Parâmetros da requisição GET.

        Returns:
            requests.Response | None: Retorna a resposta da requisição em caso de sucesso ou None.
        """

        for _ in range(self.n_tries):
            resp = self._session.get(url, params=params)

            if resp.status_code == 200:
                return resp

            sleep(self.sec_wait)
            self._restart_session()

        return None

    def _request(self, endpoint: list[str], params: Optional[dict]
                 = None, error_msg: str = 'Erro ao buscar dados'):
        """
        Realiza a requisição para um endpoint específico da API com parâmetros opcionais.

        Args:
            endpoint (list[str]): Lista de strings representando o caminho do endpoint.
            params (dict, opcional): Parâmetros da requisição.
            error_msg (str): Mensagem de erro personalizada para exceções.

        Returns:
            dict: Dados JSON da resposta da API em caso de sucesso.

        Raises:
            Exception: Lança uma exceção com a mensagem de erro se a requisição falhar.
        """

        url = join_urls(self._api_url, *endpoint)
        req = self._get(url, params=params)
        if not req:
            raise Exception(error_msg)
        return req.json()

    def get_linha(self, linha: str) -> list[LinhaBase]:
        """
        Busca informações sobre linhas de ônibus com base em um termo de busca.

        Args:
            linha (str): Número ou denominação parcial da linha.

        Returns:
            list[LinhaBase]: Lista de objetos LinhaBase representando as linhas encontradas.
        """

        data = self._request(
            ["Linha", "Buscar"],
            params={'termosBusca': linha},
            error_msg=f'Erro ao buscar linha {linha}'
        )
        return [LinhaBase(elem) for elem in data]

    def get_linha_sentido(self, linha: str,
                          sentido: int = 1) -> list[LinhaBase]:
        """
        Busca informações de uma linha específica em um sentido determinado.

        Args:
            linha (str): Número ou denominação parcial da linha.
            sentido (int): Sentido da linha, onde 1 é Terminal Principal para Secundário e 2 é o inverso.

        Returns:
            list[LinhaBase]: Lista de objetos LinhaBase representando as linhas encontradas.
        """

        data = self._request(
            ["Linha", "BuscarLinhaSentido"],
            params={'termosBusca': linha, 'sentido': sentido},
            error_msg=f'Erro ao buscar linha {linha} com sentido {sentido}'
        )
        return [LinhaBase(elem) for elem in data]

    def get_parada(self, parada: str) -> list[ParadaBase]:
        """
        Busca informações sobre paradas de ônibus com base no nome ou endereço.

        Args:
            parada (str): Nome ou endereço parcial da parada.

        Returns:
            list[ParadaBase]: Lista de objetos ParadaBase representando as paradas encontradas.
        """
        data = self._request(
            ["Parada", "Buscar"],
            params={'termosBusca': parada},
            error_msg=f'Erro ao buscar parada {parada}'
        )
        return [ParadaBase(elem) for elem in data]

    def get_parada_corredor(self, codigo_corredor: int) -> list[ParadaBase]:
        """
        Busca todas as paradas de ônibus em um determinado corredor.

        Args:
            codigo_corredor (int): Código identificador do corredor.

        Returns:
            list[ParadaBase]: Lista de objetos ParadaBase representando as paradas do corredor.
        """

        data = self._request(
            ["Parada", "BuscarParadasPorCorredor"],
            params={'codigoCorredor': codigo_corredor},
            error_msg=f'Erro ao buscar corredor {codigo_corredor}'
        )
        return [ParadaBase(elem) for elem in data]

    def get_corredores(self) -> list[Corredor]:
        """
        Retorna todos os corredores de ônibus da cidade de São Paulo.

        Returns:
            list[Corredor]: Lista de objetos Corredor representando os corredores.
        """

        data = self._request(
            ["Corredor"],
            error_msg='Erro ao buscar corredores'
        )
        return [Corredor(elem) for elem in data]

    def get_posicao(self) -> list[Linha]:
        """
        Obtém a posição atual de todos os veículos de todas as linhas de ônibus.

        Returns:
            list[Linha]: Lista de objetos Linha representando as posições dos veículos.
        """

        data = self._request(
            ["Posicao"],
            error_msg='Erro ao buscar posição'
        )
        return [Linha(linha) for linha in data.get('l', [])]

    def get_linha_posicao(self, codigo_linha: int) -> list[Veiculo]:
        """
        Obtém a posição atual dos veículos de uma linha específica.

        Args:
            codigo_linha (int): Código identificador da linha.

        Returns:
            list[Veiculo]: Lista de objetos Veiculo representando as posições dos veículos da linha.
        """

        data = self._request(
            ["Posicao", "Linha"],
            params={'codigoLinha': codigo_linha},
            error_msg=f'Erro ao buscar posição da linha {codigo_linha}'
        )
        return [Veiculo(veiculo) for veiculo in data.get('vs', [])]

    def get_previsao_linha_parada(
            self, codigo_linha: int, codigo_parada: int) -> list[Linha]:
        """
        Obtém a previsão de chegada de veículos de uma linha em uma parada específica.

        Args:
            codigo_linha (int): Código identificador da linha.
            codigo_parada (int): Código identificador da parada.

        Returns:
            list[Linha]: Lista de objetos Linha representando as previsões de chegada na parada.
        """

        data = self._request(
            ["Previsao"],
            params={
                'codigoLinha': codigo_linha,
                'codigoParada': codigo_parada},
            error_msg=f'Erro ao buscar previsão de chegada da linha {codigo_linha} na parada {codigo_parada}')
        parada = data.get('p', {})
        if parada:
            return [Linha(linha) for linha in parada.get('l', [])]
        return []

    def get_previsao_linha(self, codigo_linha: int) -> list[Parada]:
        """
        Obtém a previsão de chegada de veículos de uma linha em todas as paradas atendidas.

        Args:
            codigo_linha (int): Código identificador da linha.

        Returns:
            list[Parada]: Lista de objetos Parada representando as previsões de chegada nas paradas.
        """

        data = self._request(
            ["Previsao", "Linha"],
            params={'codigoLinha': codigo_linha},
            error_msg=f'Erro ao buscar previsão de chegada da linha {codigo_linha}'
        )
        paradas = data.get('ps', [])
        return [Parada(parada) for parada in paradas]

    def get_previsao_parada(self, codigo_parada: int) -> list[Linha]:
        """
        Obtém a previsão de chegada de todas as linhas que atendem a uma parada específica.

        Args:
            codigo_parada (int): Código identificador da parada.

        Returns:
            list[Linha]: Lista de objetos Linha representando as previsões de chegada na parada.
        """

        data = self._request(
            ["Previsao", "Parada"],
            params={'codigoParada': codigo_parada},
            error_msg=f'Erro ao buscar previsão de chegada da parada {codigo_parada}'
        )
        parada = data.get('p', {})
        if parada:
            return [Linha(linha) for linha in parada.get('l', [])]
        return []
