# SVG Gateway
API Gateway para os microsserviços do SVG.

## Instalação e Configuração

### Pré-requisitos

- Para rodar o projeto é necessário ter o Docker e o docker-compose instalados.

- Se ainda não existir, é preciso criar uma rede no docker com o comando `docker network create svg_shared`

### Primeiros passos

Basta clonar o repositório e rodar `docker-compose up`.

Este container roda na porta 5002 da máquina _host_.

Para fazer a comunicação com os outros serviços via código deve se fazer as requisições utilizando as variáveis de ambiente existentes no _docker-compose.yml_:

  - SVG_MONITORING_BASE_URI
  - SVG_AUTH_BASE_URI

Uma requisição pode ser construída da seguinte forma:

```python
  import os

  response = requests.get("%s/endpoint" % os.getenv('SVG_AUTH_BASE_URI'))
```

### Autenticando requisições
Para garantir apenas acesso autenticado a um endpoint qualquer, usamos o decorator `@jwt_required` do `flask_jwt_extended`. Para obter o id do usuário que fez a requisição, usamos a função `get_jwt_identity`, do mesmo pacote. Um exemplo:

```python
from flask_jwt_extended import get_jwt_identity
from flask_jwt_extended import jwt_required

@some_blueprint.route('/api/route', methods=['GET'])
@jwt_required
def auth_only_route():
    user_id = get_jwt_identity()
    do_something(user_id)
    ...
```