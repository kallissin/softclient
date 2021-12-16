<div style="text-align:center">
  <img src="assets/logo_img.png" alt="SoftClient Logo"/>
</div>

<br />

Plataforma que registra um técnico em um equipamento de informática, para que ele possa atender chamados das empresas dando manutenção no equipamento no qual ele domina.

### Rodando a aplicação:

Após clonar do Git, digite no terminal:

- `python -m venv venv`
- `source venv/bin/activate`
- `pip install -r requirements.txt`
- `flask run`

Para criar um usuário do tipo "super", digite o seguinte comando no terminal:

`heroku run --app softclient flask super create name username password`

**Exemplo:**

`heroku run --app softclient flask super create kelvin kallissin 123456`

Para ativar a empresa que irá cadastrar, digite o seguinte comando no terminal:

`heroku run --app softclient flask super active cnpj`

**Exemplo:**

`heroku run --app softclient flask super active 20232212232343`

## Deploy da aplicação:

`https://softclient.herokuapp.com/api`

## Endpoints

1. Owners
2. Company
   - Login Company
3. User
   - Login User
4. Orders
5. Technicians

### Owners

Endpoint referente aos donos da empresa, onde podemos fazer fazer login e listar todos os donos.

#### Login Owner

Rota responsável pelo login do usuário "owner". Retorna um token de acesso, para que o método GET seja liberado.

|    **url**     | **method** | **status**  |
| :------------: | :--------: | :---------: |
| `/owner/login` |   `POST`   | `200 - 404` |

**BODY**

```json
{
  "username": "odaairlopes",
  "password": "123456"
}
```

**RESPONSE**

```json
{
  "token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTYzOTU5MTA2MywianRpIjoiNTU3MTczNDktOGRkZS00ZmM5LWI1NzktYzE3OGQ5NTI4ZTE1IiwidHlwZSI6ImFjY2VzcyIsInN1YiI6eyJpZCI6MSwibmFtZSI6Ik9kYWlyIiwidXNlcm5hbWUiOiJvZGFhaXJsb3BlcyIsInJvbGUiOiJzdXBlciIsImFjdGl2ZSI6dHJ1ZX0sIm5iZiI6MTYzOTU5MTA2MywiZXhwIjoxNjM5NTkxOTYzfQ.q7nCO3NVPcSOdIZalcQNKOLtVw7u-JdbeJAoUqa5dcQ"
}
```

#### GET Owner

Rota responsável por mostrar todos os usuários "owner" cadastrados.

| **url**  | **method** | **status** |
| :------: | :--------: | :--------: |
| `/owner` |   `GET`    |   `200`    |

**RESPONSE**

```json
[
  {
    "id": 1,
    "name": "Odair",
    "username": "odaairlopes",
    "role": "super",
    "active": true
  }
]
```

### Company

Endpoint referente à própria empresa. Aqui, podemos fazer o login, criação de novas empresas, obtenção de todas empresas cadastradas, obtenção de apenas uma empresa (pelo id), obtenção de todos os usuários de determinada empresa e remoção de uma empresa cadastrada. Para a empresa cadastrar uma empresa, é necessário de um super usuário.

#### Login Company

Rota responsável pelo login da empresa. Retorna um token de acesso para que os outros métodos sejam liberados. Essa empresa precisa estar ativada (ativação feita pelo super usuário).

|     **url**      | **method** | **status**  |
| :--------------: | :--------: | :---------: |
| `/company/login` |   `POST`   | `200 - 404` |

**BODY**

```json
{
  "username": "sofclient",
  "password": "softclient1234"
}
```

**RESPONSE**

```json
{
  "token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTYzOTU5MTg1NywianRpIjoiZmJkNWYzMDEtZjJlMS00MDhkLWE5YjUtNzg3M2U4YmFiZjE4IiwidHlwZSI6ImFjY2VzcyIsInN1YiI6eyJpZCI6MSwiYWN0aXZlIjpmYWxzZSwiY25waiI6IjIwMjMyMjEyMjMyMzQyIiwidHJhZGluZ19uYW1lIjoiU29mdCBDbGllbnQgSW5jLiIsImNvbXBhbnlfbmFtZSI6IlNvZnRjbGllbnQiLCJ1c2VybmFtZSI6InNvZmNsaWVudCIsInJvbGUiOiJhZG1pbiJ9LCJuYmYiOjE2Mzk1OTE4NTcsImV4cCI6MTYzOTU5Mjc1N30.TyrNl7sgcVeeI4RjJehpUU_Ln-zD2BLD3M7tAuXCPP4"
}
```

#### POST Company

Rota para cadastrar uma empresa.

|  **url**   | **method** | **status**  |
| :--------: | :--------: | :---------: |
| `/company` |   `POST`   | `201 - 400` |

Formato dos campos:

- **"cnpj"**: deve ser colocado todos os 14 dígitos, sem pontuação;

**BODY**

```json
{
  "cnpj": "20232212232342",
  "trading_name": "Soft Client Inc.",
  "company_name": "SoftClient",
  "username": "sofclient",
  "password": "softclient1234"
}
```

**RESPONSE**

```json
{
  "id": 1,
  "active": false,
  "cnpj": "20.232.212/2323-42",
  "trading_name": "Soft Client Inc.",
  "company_name": "Softclient"
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
    "cnpj": "20.232.212/2323-42",
    "trading_name": "Soft Client Inc.",
    "company_name": "Softclient",
    "users": []
  },
  {
    "id": 2,
    "cnpj": "10.123.286/0001-56",
    "trading_name": "Wal-Mart Inc.",
    "company_name": "Walmart",
    "users": []
  },
  {
    "id": 3,
    "cnpj": "08.522.687/0001-37",
    "trading_name": "Microsoft Inc.",
    "company_name": "Microsoft",
    "users": []
  }
]
```

#### GET One Company

Rota que pega uma única empresa, pelo seu id.

|       **url**        | **method** | **status**  |
| :------------------: | :--------: | :---------: |
| `company/company_id` |   `GET`    | `200 - 404` |

**RESPONSE**

```json
{
  "id": 1,
  "cnpj": "20.232.212/2323-42",
  "trading_name": "Soft Client Inc.",
  "company_name": "Softclient",
  "users": []
}
```

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

#### PATCH Company

Rota responsável pela atualização de uma empresa.

|        **url**        | **method** | **status**  |
| :-------------------: | :--------: | :---------: |
| `/company/company_id` |  `PATCH`   | `200 - 400` |

**BODY**

```json
{
  "trading_name": "Soft Client Enterprise"
}
```

**RESPONSE**

```json
{
  "id": 1,
  "cnpj": "20.232.212/2323-42",
  "trading_name": "Soft Client Enterprise",
  "company_name": "Softclient"
}
```

#### PATCH Company active

Rota responsável por desativar uma empresa.

|        **url**        | **method** | **status**  |
| :-------------------: | :--------: | :---------: |
| `/company/company_id` |  `PATCH`   | `200 - 400` |

**BODY**

```json
{
  "active": False
}
```

**RESPONSE - status**

```json
{
  "id": 1,
  "cnpj": "20.232.212/2323-42",
  "trading_name": "Soft Client Enterprise",
  "company_name": "Softclient",
  "active": false
}
```

### User

Endpoint referente aos usuários que fazem parte da empresa. Aqui podemos fazer a criação de usuário, alteração de usuários, obtenção de todos os usuários, obtenção de usuário por filtragem (email e nome), remoção de um usuário, pesquisa de usuários que solicitaram um serviço e pesquisa de um usuário de certa empresa.

#### Login User

Rota responsável pelo login do usuário. Retorna um token de acesso para que os outros métodos sejam liberados.

**BODY**

```json
{
  "email": "kelvin@gmail.com",
  "password": "kelvin1234"
}
```

**RESPONSE**

```json
{
  "token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTYzOTU5MzI0NywianRpIjoiYzUwMThhNmEtYWI2Mi00NWI2LTkyM2UtNTA5MzZlNWU0NTBjIiwidHlwZSI6ImFjY2VzcyIsInN1YiI6eyJpZCI6MSwibmFtZSI6IktlbHZpbiIsImVtYWlsIjoia2VsdmluQGdtYWlsLmNvbSIsInBvc2l0aW9uIjoiQ1RPIiwiYWN0aXZlIjp0cnVlLCJiaXJ0aGRhdGUiOiIyMi8wNS8xOTkzIiwicm9sZSI6ImFkbWluIiwiY29tcGFueV9uYW1lIjoiU29mdGNsaWVudCJ9LCJuYmYiOjE2Mzk1OTMyNDcsImV4cCI6MTYzOTU5NDE0N30.UpfscEuF4p-BpO1NJtJb4RkKII-GvDxA-pfJyu4OjC4"
}
```

#### POST User

Rota referente a criação de um usuário. Necessário utilizar o token da empresa, para fazer a criação do seu usuário.

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
  "name": "Kelvin",
  "email": "kelvin@gmail.com",
  "password": "kelvin1234",
  "birthdate": "22/05/1993",
  "position": "CTO",
  "role": "admin",
  "company_id": 1
}
```

**RESPONSE**

```json
{
  "id": 1,
  "name": "Kelvin",
  "email": "kelvin@gmail.com",
  "position": "CTO",
  "birthdate": "22/05/1993",
  "active": true,
  "role": "admin",
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
    "name": "Kelvin",
    "email": "kelvin@gmail.com",
    "position": "CTO",
    "active": true,
    "birthdate": "22/05/1993",
    "role": "admin",
    "company": {
      "id": 1,
      "trading_name": "Soft Client Inc.",
      "cnpj": "20232212232342"
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
  "name": "Kelvin",
  "email": "kelvin@gmail.com",
  "position": "CTO",
  "active": true,
  "birthdate": "22/05/1993",
  "role": "admin",
  "company": {
    "id": 1,
    "trading_name": "Soft Client Inc.",
    "cnpj": "20232212232342"
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
  "id": 1,
  "name": "Kelvin",
  "email": "kelvin@gmail.com",
  "position": "CTO",
  "active": true,
  "birthdate": "22/05/1993",
  "role": "admin",
  "company": {
    "id": 1,
    "trading_name": "Soft Client Inc.",
    "cnpj": "20232212232342"
  }
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
    "cnpj": "20232212232342",
    "trading_name": "Soft Client Inc.",
    "company_name": "Softclient"
  }
}
```

#### GET Order by user id

Rota responsável pela pesquisa de um chamado utilizando o id do usuário. Para essa pesquisa, é necessário passar o token do usuário com a role 'user'.

|        **url**        | **method** | **status**  |
| :-------------------: | :--------: | :---------: |
| `/user/user_id/order` |   `GET`    | `200 - 404` |

**RESPONSE**

```json
[
  {
    "id": 1,
    "type": "computador",
    "status": "fechado",
    "description": "O computador apresenta falhas contínuas",
    "release_date": "Wed, 15 Dec 2021 18:45:47 GMT",
    "update_date": "Wed, 15 Dec 2021 19:02:15 GMT",
    "solution": "Troca de algumas peças do computador, que estavam falhando. Todas elas foram verificadas."
  }
]
```

#### PATCH User

Rota referente a atualização de um usuário, passando o id desse usuário.

|     **url**     | **method** | **status**  |
| :-------------: | :--------: | :---------: |
| `/user/user_id` |  `PATCH`   | `200 - 404` |

**BODY**

```json
{
  "name": "Kelvin Alisson"
}
```

**RESPONSE**

```json
{
  "id": 1,
  "name": "Kelvin",
  "email": "kelvin@gmail.com",
  "position": "CTO",
  "active": true,
  "birthdate": "22/05/1993",
  "role": "admin",
  "company_name": "Softclient"
}
```

### Order

Endpoint referente a criação de um chamado, alteração de usuários, obtenção de todos os chamados, remoção de um chamado, pesquisa do usuário que fez um chamado e pesquisa de um técnico de pelo chamado. O chamado só pode ser criado por um usuário que tenha a role de 'user', sendo necessário o token desse usuário.

#### POST Order

Rota referente à criação de um chamado.

|  **url**  | **method** | **status** |
| :-------: | :--------: | :--------: |
| `/orders` |   `POST`   |   `200`    |

**BODY**

```json
{
  "type": "nobreak",
  "description": "No break apitando todo momento",
  "release_date": "22/10/2021",
  "update_date": "16/12/2021",
  "user_id": 1
}
```

**RESPONSE**

```json
{
  "id": 1,
  "type": "nobreak",
  "status": "aberto",
  "description": "No break apitando todo momento",
  "release_date": "Thu, 16 Dec 2021 17:05:31 GMT",
  "update_date": "Thu, 16 Dec 2021 17:05:31 GMT",
  "solution": "",
  "user": {
    "id": 1,
    "name": "Kelvin",
    "email": "kelvin@gmail.com",
    "position": "CTO",
    "role": "admin"
  },
  "technician": null
}
```

#### GET Order

Rota responsável por obter todos os chamados.

|  **url**  | **method** | **status** |
| :-------: | :--------: | :--------: |
| `/orders` |   `GET`    |   `200`    |

**RESPONSE**

```json
[
  {
    "id": 1,
    "type": "nobreak",
    "status": "aberto",
    "description": "No break apitando todo momento",
    "release_date": "Thu, 16 Dec 2021 17:05:31 GMT",
    "update_date": "Thu, 16 Dec 2021 17:05:31 GMT",
    "solution": "",
    "user": {
      "id": 1,
      "name": "Kelvin",
      "email": "kelvin@gmail.com",
      "position": "CTO",
      "role": "admin"
    },
    "technician": null
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
  "id": 1,
  "type": "Nobreak",
  "status": "aberto",
  "description": "No break apitando todo momento",
  "release_date": "Thu, 16 Dec 2021 17:05:31 GMT",
  "update_date": "Thu, 16 Dec 2021 17:05:31 GMT",
  "solution": "",
  "user": {
    "id": 1,
    "name": "Kelvin",
    "email": "kelvin@gmail.com",
    "position": "CTO",
    "role": "admin"
  },
  "technician": null
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
    "id": 2,
    "name": "João Guilherme Filho",
    "email": "joaoguilherme@gmail.com",
    "birthdate": "22/05/1993",
    "role": "user"
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

#### GET Order by status

Rota responsável por obter os chamados, passando na rota os status disponíveis (aberto, em_atendimento, fechado) e o token do usuário que criou esse chamado.

|        **url**         | **method** | **status**  |
| :--------------------: | :--------: | :---------: |
| `/orders/order_status` |   `GET`    | `200 - 404` |

**RESPONSE**

```json
[
  {
    "id": 1,
    "type": "Nobreak",
    "status": "aberto",
    "description": "No break apitando todo momento",
    "release_date": "Thu, 16 Dec 2021 17:05:31 GMT",
    "update_date": "Thu, 16 Dec 2021 17:05:31 GMT",
    "solution": "",
    "user": {
      "id": 1,
      "name": "Kelvin",
      "email": "kelvin@gmail.com",
      "position": "CTO",
      "role": "admin"
    },
    "technician": null
  }
]
```

#### PATCH Order by id

Rota responsável pela atualização de um chamado, passando o id dele na rota.

|      **url**       | **method** |       **status**        |
| :----------------: | :--------: | :---------------------: |
| `/orders/order_id` |  `PATCH`   | `200 - 400 - 401 - 404` |

**BODY**

```json
{
  "description": "Apresenta falhas contínuas."
}
```

**RESPONSE**

```json
{
  "id": 1,
  "type": "Nobreak",
  "status": "aberto",
  "description": "Apresenta falhas contínuas.",
  "release_date": "Thu, 16 Dec 2021 17:05:31 GMT",
  "update_date": "Thu, 16 Dec 2021 17:05:31 GMT",
  "solution": "",
  "user": {
    "id": 1,
    "name": "João",
    "email": "joaoguilherme@gmail.com",
    "position": "CTO",
    "role": "admin"
  },
  "technician": null
}
```

#### DELETE Order

Rota responsável por fazer a remoção de um chamado, passando o id dele na rota.

|      **url**       | **method** | **status**  |
| :----------------: | :--------: | :---------: |
| `/orders/order_id` |  `DELETE`  | `200 - 404` |

**RESPONSE - status**

`204`

### Technician

Endpoint referente ao técnicos responsáveis por responderem aos chamados. Aqui podemso fazer o login do técnico, inserção de um técnico, alteração de dados do técnico, obtenção de todos os técnicos, obtenção de um técnico apenas, obtenção dos chamados que estão relacionados à um técnico e exclusão de um técnico. Para a criação de um técnico, é necessário o token da empresa. Para as outras rotas, necessário o token do próprio técnico, obtido no login.

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
  "token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTYzOTU5NDQzMywianRpIjoiYjJiNDMyZWUtMzlhMC00MTNmLTlhOWYtYTQ5Y2QwYjM4NWQzIiwidHlwZSI6ImFjY2VzcyIsInN1YiI6eyJpZCI6MSwibmFtZSI6Ikd1c3Rhdm8gTWFydGlucyIsImVtYWlsIjoiZ3VzdGF2b21hcnRpbnNAZ21haWwuY29tIiwiYmlydGhkYXRlIjoiRnJpLCAyNyBEZWMgMTk4NSAwMDowMDowMCBHTVQifSwibmJmIjoxNjM5NTk0NDMzLCJleHAiOjE2Mzk1OTUzMzN9.snEqX5nCWlItBDEcOEVXFZHOKYgwrgrFdPgeNGyEwAs"
}
```

#### POST Technician

|    **url**     | **method** | **status** |
| :------------: | :--------: | :--------: |
| `/technicians` |   `POST`   |   `200`    |

```json
{
  "name": "Erick Lander",
  "email": "ericklander@gmail.com",
  "password": "123456",
  "birthdate": "03/05/1989"
}
```

**RESPONSE**

```json
{
  "id": 1,
  "name": "Erick Lander",
  "email": "ericklander@gmail.com",
  "birthdate": "03/05/1989",
  "role": "tech"
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
    "name": "Erick Lander",
    "email": "ericklander@gmail.com",
    "birthdate": "03/05/1989",
    "role": "tech"
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
  "name": "Erick Lander",
  "email": "ericklander@gmail.com",
  "birthdate": "03/05/1989",
  "role": "tech"
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
    "id": 1,
    "type": "nobreak",
    "status": "em_atendimento",
    "description": "Apresenta falhas contínuas.",
    "release_date": "Thu, 16 Dec 2021 17:05:31 GMT",
    "update_date": "Thu, 16 Dec 2021 17:32:12 GMT",
    "solution": "",
    "user": {
      "id": 1,
      "name": "João",
      "email": "joaoguilherme@gmail.com",
      "position": "CTO",
      "company": {
        "id": 1,
        "cnpj": "52.468.355/0001-03",
        "trading_name": "Microsoft Enterprise"
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
  "name": "Erick"
}
```

**RESPONSE**

```json
{
  "id": 1,
  "name": "Erick",
  "email": "ericklander@gmail.com",
  "birthdate": "03/05/1989",
  "role": "tech"
}
```

#### PATCH Take order

Rota responsável pelo técnico assumir um chamado em aberto. Para isso, é necessário apenas passar o id do chamado na rota e o token do técnico que ficará com aquele chamado.

|              **url**               | **method** |    **status**     |
| :--------------------------------: | :--------: | :---------------: |
| `/technicians/take_order/order_id` |  `PATCH`   | `200 - 400 - 404` |

**RESPONSE**

```json
{
  "order": {
    "id": 1,
    "status": "em_atendimento",
    "type": "nobreak",
    "description": "Apresenta falhas contínuas.",
    "release_date": "Thu, 16 Dec 2021 17:05:31 GMT",
    "update_date": "Thu, 16 Dec 2021 17:32:12 GMT",
    "user": {
      "id": 1,
      "name": "João",
      "email": "joaoguilherme@gmail.com",
      "position": "CTO",
      "birthdate": "01/01/2001"
    }
  }
}
```

#### PATCH Finalize order

Rota responsável pelo técnico finalizar aquele chamado. Para isso, é necessário apenas passar id do chamado na rota e o token do técnico que havia assumido aquele chamado.

|                **url**                 | **method** |       **status**        |
| :------------------------------------: | :--------: | :---------------------: |
| `/technicians/finalize_order/order_id` |  `PATCH`   | `200 - 400 - 401 - 404` |

**BODY**

```json
{
  "solution": "COMPRA DE UM NOVO NOBREAK."
}
```

**RESPONSE**

```json
{
  "order": {
    "id": 1,
    "status": "fechado",
    "type": "nobreak",
    "description": "Apresenta falhas contínuas.",
    "release_date": "Thu, 16 Dec 2021 17:05:31 GMT",
    "update_date": "Thu, 16 Dec 2021 17:34:30 GMT",
    "solution": "COMPRA DE UM NOVO NOBREAK.",
    "user": {
      "id": 1,
      "name": "João",
      "email": "joaoguilherme@gmail.com",
      "position": "CTO",
      "birthdate": "01/01/2001"
    }
  }
}
```
