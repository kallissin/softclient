# SoftClient

Plataforma que registra um técnico em um equipamento de informática, para que ele possa atender chamados das empresas dando manutenção no equipamento no qual ele domina.

### Rodando a aplicação:

Após clonar do Git, digite no terminal:

- `python -m venv venv`
- `source venv/bin/activate`
- `pip install -r requirements.txt`
- `flask run`

## Deploy da aplicação:

`https://softclient.herokuapp.com/api`

## Endpoints

1. Company
   - Login Company
2. User
   - Login User
3. Orders
4. Technicians

### Company

Endpoint referente ao login da empresa, criação da empresa, obtenção de todas empresas cadastradas, obtenção de apenas uma empresa, obtenção de todos os usuários de determinada empresa e remoção de uma empresa cadastrada.

#### Login Company

Rota responsável pelo login da empresa. Retorna um token de acesso para que os outros métodos sejam liberados.

|     **url**      | **method** |  **status**   |
| :--------------: | :--------: | :-----------: |
| `/company/login` |   `POST`   | `token - 404` |

**BODY**

```json
{
  "username": "kenzie",
  "password": "123456"
}
```

**RESPONSE**

```json
{
  "token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTYzOTQxNzU3NCwianRpIjoiZjk1MTA1NDMtYTA2MC00MWYxLWIwOTItYzZjYTE0OTM1YzAzIiwidHlwZSI6ImFjY2VzcyIsInN1YiI6eyJpZCI6MSwiY25waiI6IjIwMjMyMjEyMjMyMzQyIiwidHJhZGluZ19uYW1lIjoiS2VsdmluaG8gRGUgQ1x1MDBmM2RpZ28gTHRkYS4iLCJjb21wYW55X25hbWUiOiJLZWx2aW4gVGkgVWx0cmEgU3BlZWQiLCJ1c2VybmFtZSI6ImtlbnppZSIsInJvbGUiOiJhZG1pbiJ9LCJuYmYiOjE2Mzk0MTc1NzQsImV4cCI6MTYzOTQxODQ3NH0.PBCz4BG683VB4uIW1H0Ki2HSSqaQQu7WOVNWniRuEqI"
}
```

#### GET Company

Rota para obter todas as empresas cadastradas.

|  **url**   | **method** | **status** |
| :--------: | :--------: | :--------: |
| `/company` |   `GET`    |   `201`    |

**RESPONSE**

```json
[
  {
    "id": 1,
    "cnpj": "00.500.497/0001-07",
    "trading_name": "Soft Client Inc.",
    "company_name": "Softclient",
    "users": []
  }
]
```

#### POST Company

Rota para cadastrar uma empresa.

|  **url**   | **method** | **status**  |
| :--------: | :--------: | :---------: |
| `/company` |   `POST`   | `201 - 400` |

Formato dos campos:

- **"cnpj"**: deve ser colocado todos os 14 dígitos, sem pontuação;
- **"username"**: string, o usuário que decide o username;
- **"password"**: string, o usuário que decide o password;

**BODY**

```json
{
  "cnpj": "00500497000107",
  "trading_name": "Soft Client Inc.",
  "company_name": "SoftClient",
  "username": "kenzie",
  "password": "123456"
}
```

**RESPONSE**

```json
{
  "id": 1,
  "cnpj": "00.500.497/0001-07",
  "trading_name": "Soft Client Inc.",
  "company_name": "Softclient"
}
```

#### GET One Company

Rota que pega uma única empresa, pelo seu id.

|       **url**        | **method** | **status**  |
| :------------------: | :--------: | :---------: |
| `company/company_id` |   `GET`    | `200 - 404` |

**RESPONSE**

```json
{
  "id": 2,
  "cnpj": "81.124.839/0001-33",
  "trading_name": "Wal-Mart Inc",
  "company_name": "Walmart",
  "users": []
}
```

#### DELETE Company

Rota que deleta uma empresa, recebendo o seu id.

|        **url**        | **method** | **status**  |
| :-------------------: | :--------: | :---------: |
| `/company/company_id` |  `DELETE`  | `204 - 400` |

**RESPONSE - status**

`204`

#### GET Company Users

Rota que pega os usuários cadastrados referentes à empresa.

|           **url**           | **method** | **status**  |
| :-------------------------: | :--------: | :---------: |
| `/company/company_id/users` |   `GET`    | `200 - 400` |

1 - Caso não haja nenhum usuário cadastrado

**RESPONSE**

```json
[]
```

2 - Caso tenha algum usuário cadastrado

**RESPONSE**

```json
[
  {
    "id": 1,
    "name": "Marcelo",
    "email": "marcelo@gmail.com.br",
    "birthdate": "Fri, 22 Nov 1996 00:00:00 GMT",
    "active": true,
    "role": "tech"
  }
]
```

### User

Endpoint referente a criação de usuário, alteração de usuários, obtenção de todos os usuários, obtenção de usuário por filtragem (email e nome), remoção de um usuário, pesquisa de usuários que solicitaram um serviço e pesquisa de um usuário de certa empresa.

#### Login User

Rota responsável pela autenticação do usuário, para ter acesso aos métodos.

**BODY**

```json
{
  "email": "guilherme@gmail.com",
  "password": "aa1123"
}
```

**RESPONSE**

```json
{
  "token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTYzOTQyMDg0NywianRpIjoiMjUxMjMwYjMtNzMzNS00ZTBhLWJiZjgtYzVjMWZhMTljZGM3IiwidHlwZSI6ImFjY2VzcyIsInN1YiI6eyJpZCI6MywibmFtZSI6Ikd1aWxoZXJtZSIsImVtYWlsIjoiZ3VpbGhlcm1lQGdtYWlsLmNvbSIsImJpcnRoZGF0ZSI6IkZyaSwgMjIgTm92IDE5OTYgMDA6MDA6MDAgR01UIiwiYWN0aXZlIjp0cnVlLCJyb2xlIjoiYWRtaW4ifSwibmJmIjoxNjM5NDIwODQ3LCJleHAiOjE2Mzk0MjE3NDd9.-rPdtRqXgaHYRwUm8CDw5DbagGAQEd927Of9tRa5fbo"
}
```

#### POST User

Rota referente a criação de um usuário.

| **url** | **method** |    **status**     |
| :-----: | :--------: | :---------------: |
| `/user` |   `POST`   | `201 - 400 - 409` |

Formato dos campos:

- **"name"**: string com 150 caracteres;
- **"email"**: string;
- **"password"**: string;
- **"birthdate"**: data no formato XX/XX/XXXX;
- **"position"**: cargo na empresa, string;
- **"role"**: permissões que são concedidas ao usuário (user/tech);

**BODY**

```json
{
  "name": "Joãozinho Camargo",
  "email": "joaocamargo@gmail.com.br",
  "password": "12345",
  "birthdate": "22/11/1996",
  "role": "user",
  "company_id": 1
}
```

**RESPONSE**

```json
{
  "id": 3,
  "name": "Joãozinho Camargo",
  "email": "joaocamargo@gmail.com.br",
  "birthdate": "22/11/1996",
  "active": true,
  "role": "user",
  "company_name": "Softclient"
}
```

#### GET Users

Rota para obter todos os usuários cadastrados.

| **url** | **method** | **status** |
| :-----: | :--------: | :--------: |
| `/user` |   `GET`    |   `200`    |

**RESPONSE**

```json
[
  {
    "id": 1,
    "name": "Zézinho Da Silva",
    "email": "zezinhosilva@gmail.com.br",
    "active": true,
    "birthdate": "22/11/1996",
    "role": "tech",
    "company": {
      "id": 1,
      "trading_name": "Soft Client Inc.",
      "cnpj": "00500497000107"
    }
  }
]
```

#### GET One user by id

Rota referente a pesquisa de um usuário, passando o id dele.

|     **url**     | **method** | **status**  |
| :-------------: | :--------: | :---------: |
| `/user/user_id` |   `GET`    | `200 - 404` |

**RESPONSE**

```json
{
  "id": 1,
  "name": "Zézinho Da Silva",
  "email": "zezinhosilva@gmail.com.br",
  "active": true,
  "birthdate": "22/11/1996",
  "role": "basic",
  "company": {
    "id": 1,
    "trading_name": "Soft Client Inc.",
    "cnpj": "00500497000107"
  }
}
```

#### GET One user by name

Rota referente a pesquisa de um usuário, passando o nome dele.

|      **url**      | **method** | **status**  |
| :---------------: | :--------: | :---------: |
| `/user/user_name` |   `GET`    | `200 - 404` |

**RESPONSE**

```json
{
  "id": 6,
  "name": "Marcelo",
  "email": "marcelo@gmail.com.br",
  "active": true,
  "birthdate": "22/11/1996",
  "role": "tech",
  "company": {
    "id": 1,
    "trading_name": "Soft Client Inc.",
    "cnpj": "00500497000107"
  }
}
```

#### PATCH User

Rota referente a atualização de um usuário, passando o id desse usuário.

|     **url**     | **method** | **status**  |
| :-------------: | :--------: | :---------: |
| `/user/user_id` |  `PATCH`   | `200 - 404` |

**BODY**

```json
{
  "name": "Marcelo Moraes"
}
```

**RESPONSE**

```json
{
  "id": 6,
  "name": "Marcelo Moraes",
  "email": "marcelo@gmail.com.br",
  "active": true,
  "birthdate": "22/11/1996",
  "role": "tech",
  "company_name": "Softclient"
}
```

#### DELETE User

Rota responsável pela remoção do usuário, passando o id dele.

|     **url**     | **method** | **status**  |
| :-------------: | :--------: | :---------: |
| `/user/user_id` |  `DELETE`  | `200 - 404` |

**RESPONSE**

```json
{
  "id": 1,
  "name": "Marcelo",
  "email": "marcelo@gmail.com.br",
  "birthdate": "Fri, 22 Nov 1996 00:00:00 GMT",
  "active": true,
  "role": "tech"
}
```

#### GET Company by user id

Rota responsável pela pesquisa de uma empresa utilizando o id do usuário.

|         **url**         | **method** | **status**  |
| :---------------------: | :--------: | :---------: |
| `/user/user_id/company` |   `GET`    | `200 - 404` |

**RESPONSE**

```json
{
  "company": {
    "id": 1,
    "cnpj": "00500497000107",
    "trading_name": "Soft Client Inc.",
    "company_name": "Softclient"
  }
}
```

#### GET Order by user id

Rota responsável pela pesquisa de um chamado feito pelo usuário.

|        **url**        | **method** | **status**  |
| :-------------------: | :--------: | :---------: |
| `/user/user_id/order` |   `GET`    | `200 - 404` |

**RESPONSE**

```json
{
  "user": {
    "id": 3,
    "name": "Guilherme",
    "email": "guilherme@gmail.com",
    "birthdate": "22/11/1996",
    "role": "admin"
  }
}
```

### Order

Endpoint referente a criação de um chamado, alteração de usuários, obtenção de todos os chamados, remoção de um chamado, pesquisa do usuário que fez um chamado e pesquisa de um técnico de pelo chamado.

#### POST Order

Rota referente à criação de um chamado.

|  **url**  | **method** | **status** |
| :-------: | :--------: | :--------: |
| `/orders` |   `POST`   |   `200`    |

**BODY**

```json
{
  "status": "aberto",
  "type": "computador",
  "description": "Realizar uma averiguação do computador, pois está travando muito.",
  "release_date": "13/12/2021",
  "update_date": "13/12/2021",
  "user_id": 3,
  "technician_id": 1
}
```

**RESPONSE**

```json
{
  "type": "computador",
  "status": "aberto",
  "description": "Realizar uma averiguação do computador, pois está travando muito.",
  "release_date": "13/12/2021",
  "update_date": "13/12/2021",
  "solution": "",
  "user_id": 3,
  "technician_id": 1
}
```

#### GET Order

Rota responsável por obter todos os chamados.
| **url** | **method** | **status** |
|:---------:|:----------:|:----------:|
| `/orders` | `GET` | `200` |

**RESPONSE**

```json
[
  {
    "id": 3,
    "type": "computador",
    "status": "aberto",
    "description": "Realizar uma averiguação do computador, pois está travando muito.",
    "release_date": "13/12/2021",
    "update_date": "13/12/2021",
    "solution": "",
    "user_id": 3
  }
]
```

#### GET Order by id

Rota responsável pela pesquisa do chamado, passando o id dele na requisição.

|      **url**       | **method** | **status**  |
| :----------------: | :--------: | :---------: |
| `/orders/order_id` |   `GET`    | `200 - 404` |

**RESPONSE**

```json
{
  "type": "notebook",
  "status": "aberto",
  "description": "Notebook esquentando muito e desligando as vezes.",
  "release_date": "13/12/2021, 18:55",
  "update_date": "13/12/2021, 18:55",
  "solution": "",
  "user_id": 2,
  "technician_id": 1
}
```

#### GET User by order id

Rota responsável pela pesquisa do usuário que solicitou o chamado, passando o id do chamado na rota.

|         **url**         | **method** | **status**  |
| :---------------------: | :--------: | :---------: |
| `/orders/order_id/user` |   `GET`    | `200 - 404` |

**RESPONSE**

```json
{
  "user": {
    "id": 3,
    "name": "Guilherme",
    "email": "guilherme@gmail.com",
    "birthdate": "22/11/1996",
    "role": "admin"
  }
}
```

#### GET Technician by order id

Rota responsável pela pesquisa do técnico que realizará a manutenção, passando o id do chamado na rota.

|            **url**            | **method** | **status**  |
| :---------------------------: | :--------: | :---------: |
| `/orders/order_id/technician` |   `GET`    | `200 - 404` |

**RESPONSE**

```json
{
  "technician": {
    "id": 1,
    "name": "Gustavo Martins",
    "email": "gustavomartins@gmail.com",
    "birthdate": "22/11/1996"
  }
}
```

#### DELETE ORDER

Rota responsável por fazer a remoção de um chamado, passando o id do chamado pra ela.

|      **url**       | **method** | **status**  |
| :----------------: | :--------: | :---------: |
| `/orders/order_id` |  `DELETE`  | `200 - 404` |

**RESPONSE - status**

`204`

### Technician

Endpoint referente ao login do técnico, inserção de um técnico, alteração de dados do técnico, obtenção de todos os técnicos, obtenção de um técnico apenas, obtenção dos chamados que estão relacionados à um técnico e exclusão de um técnico.

#### LOGIN Technician

Rota responsável pelo login do técnico. Retorna um token de acesso para que os outros métodos sejam liberados.

|       **url**        | **method** | **status**  |
| :------------------: | :--------: | :---------: |
| `/technicians/login` |   `POST`   | `200 - 404` |

**BODY**

```json
{
  "email": "gustavomartins@gmail.com",
  "password": "123456"
}
```

**RESPONSE**

```json
{
  "token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTYzOTQyNzYxMywianRpIjoiMGUzZmRhY2UtNzM4Yi00MzkwLWEwMWEtZDMzZjZjMDU2M2VlIiwidHlwZSI6ImFjY2VzcyIsInN1YiI6eyJpZCI6NCwibmFtZSI6Ikd1c3Rhdm8gTWFydGlucyIsImVtYWlsIjoiZ3VzdGF2b21hcnRpbnNAZ21haWwuY29tIiwiYmlydGhkYXRlIjoiRnJpLCAyNyBEZWMgMTk4NSAwMDowMDowMCBHTVQifSwibmJmIjoxNjM5NDI3NjEzLCJleHAiOjE2Mzk0Mjg1MTN9.RPw18icuvjCrtpqhY1dEWPGWVYCK1yG4PxMz7lzy4EQ"
}
```

#### POST Technician

|    **url**     | **method** | **status** |
| :------------: | :--------: | :--------: |
| `/technicians` |   `POST`   |   `200`    |

```json
{
  "name": "Gustavo Martins",
  "email": "gustavomartins@gmail.com",
  "password": "123456",
  "birthdate": "15/10/1991"
}
```

**RESPONSE**

```json
{
  "id": 1,
  "name": "Gustavo Martins",
  "email": "gustavomartins@gmail.com",
  "password": "123456",
  "birthdate": "15/10/1991"
}
```

#### GET Technician

Rota responsável pela pesquisa de todos os técnicos registrados na API.

|    **url**     | **method** | **status** |
| :------------: | :--------: | :--------: |
| `/technicians` |   `GET`    |   `200`    |

```json
[
  {
    "id": 1,
    "name": "Gustavo Martins",
    "email": "gustavomartins@gmail.com",
    "birthdate": "15/10/1991"
  }
]
```

#### GET Technician by id

Rota responsável por trazer os dados de um técnico, passando o id dele na rota.

|           **url**            | **method** | **status**  |
| :--------------------------: | :--------: | :---------: |
| `/technicians/technician_id` |   `GET`    | `200 - 404` |

```json
{
  "id": 1,
  "name": "Gustavo Martins",
  "email": "gustavomartins@gmail.com",
  "birthdate": "15/10/1991"
}
```

#### GET Order by technician id

Rota responsável por obter à qua(is)l chamado(s) aquele técnico foi relacionado, passando o id do técnico na rota.

|               **url**               | **method** | **status**  |
| :---------------------------------: | :--------: | :---------: |
| `/technicians/technician_id/orders` |   `GET`    | `200 - 404` |

```json
[
  {
    "id": 5,
    "type": "computador",
    "status": "aberto",
    "description": "Realizar uma averiguação do computador, pois está travando muito.",
    "release_date": "Mon, 13 Dec 2021 18:32:43 GMT",
    "update_date": "Mon, 13 Dec 2021 18:32:43 GMT",
    "solution": "",
    "user": {
      "id": 3,
      "name": "Guilherme",
      "email": "guilherme@gmail.com",
      "role": "admin",
      "company": {
        "id": 1,
        "cnpj": "00.500.497/0001-07",
        "trading_name": "Soft Client Inc"
      }
    }
  }
]
```

#### PATCH Technician

Rota responsável pela atualização dos dados do técnico, passando o id do técnico na rota. Para poder fazer as alterações, é necessário estar logado na aplicação.

|           **url**            | **method** |       **status**        |
| :--------------------------: | :--------: | :---------------------: |
| `/technicians/technician_id` |  `PATCH`   | `200 - 400 - 404 - 409` |

**BODY**

```json
{
  "name": "Gustavo Martins Ferreira"
}
```

**RESPONSE**

```json
{
  "id": 4,
  "name": "Gustavo Martins Ferreira",
  "email": "gustavomartins@gmail.com",
  "birthdate": "27/12/1985"
}
```

#### DELETE Technician

Rota responsável pela remoção de um técnico da API.

**RESPONSE**

```json
{
  "id": 1,
  "name": "Gustavo Martins",
  "email": "gustavomartins@gmail.com",
  "birthdate": "15/10/1991"
}
```
