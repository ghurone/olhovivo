# OlhoVivoAPI

OlhoVivoAPI é um pacote Python para facilitar a interação com a API Olho Vivo da SPTrans, fornecendo acesso a dados de transporte público da cidade de São Paulo, como linhas de ônibus, paradas, corredores, posições de veículos e previsões de chegada.

## Requisitos

- Python 3.7 ou superior
- Bibliotecas necessárias:
  - `requests`

## Instalação

1. Clone este repositório:
   ```bash
    git clone https://github.com/ghurone/olhovivoapi.git
    ```
2. Instale as dependencias:
    ```bash
    pip install -r requirements.txt
    ```

## Uso Básico

```python
from olhovivo import OlhoVivoAPI

# Inicializa a API com tentativas de requisição e tempo de espera
api = OlhoVivoAPI(n_tries=3, sec_wait=2)

# Exemplo: Buscar uma linha de ônibus
linhas = api.get_linha("8000")
print(linhas)

# Exemplo: Obter posição de veículos em uma linha
veiculos = api.get_linha_posicao(8000)  # Código da linha
print(veiculos)

# Exemplo: Previsão de chegada para uma linha em uma parada
previsao = api.get_previsao_linha_parada(codigo_linha=8000, codigo_parada=67890)
print(previsao)
```