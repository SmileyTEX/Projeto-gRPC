# Gacha Game — Projeto gRPC

Sistema distribuído simples em Python que demonstra comunicação remota com **gRPC** e contrato definido em **Protocol Buffers**.

Tema: um mini **Gacha Game** em que o jogador invoca personagens, lista a coleção e evolui personagens obtidos. Os dados ficam em memória no servidor.

## Estrutura

```
Projeto-gRPC/
├── protos/
│   └── gacha.proto          # Contrato do serviço
├── generated/
│   ├── gacha_pb2.py         # Mensagens geradas automaticamente
│   └── gacha_pb2_grpc.py    # Stubs gRPC gerados automaticamente
├── server.py                # Servidor gRPC
├── client.py                # Cliente gRPC (CLI)
├── generate_stubs.py        # Script para regenerar o código a partir do .proto
├── requirements.txt
└── README.md
```

## Entidade e operações

### Entidade: `Personagem`

| Campo     | Tipo   | Descrição                                      |
|-----------|--------|------------------------------------------------|
| id        | int32  | Identificador único na coleção                 |
| nome      | string | Nome do personagem                             |
| raridade  | string | Comum, Raro, Épico ou Lendário                 |
| elemento  | string | Fogo, Água, Terra, Ar, Luz ou Trevas           |
| nivel     | int32  | Nível atual (inicia em 1, máximo 100)          |

### Operações remotas

| RPC                  | Descrição                                              |
|----------------------|--------------------------------------------------------|
| `InvocarPersonagem`  | Sorteia um personagem e adiciona à coleção             |
| `ListarPersonagens`  | Retorna todos os personagens obtidos                   |
| `EvoluirPersonagem`  | Aumenta em 1 o nível de um personagem pelo `id`        |

## Como executar

### 1. Instalar dependências

```bash
pip install -r requirements.txt
```

### 2. Gerar os stubs (já podem estar gerados)

```bash
python generate_stubs.py
```

Arquivos gerados automaticamente pelo compilador Protocol Buffers:

- `generated/gacha_pb2.py` — classes das mensagens (`Personagem`, requests/responses)
- `generated/gacha_pb2_grpc.py` — stubs do serviço (`GachaServiceStub`, `GachaServiceServicer`)

### 3. Subir o servidor

Em um terminal:

```bash
python server.py
```

O servidor escuta em `localhost:50051`.

### 4. Rodar o cliente

Em outro terminal:

```bash
python client.py
```

Use o menu para invocar, listar e evoluir personagens.

## Decisões arquiteturais

- **Contrato único em `.proto`**: cliente e servidor compartilham a mesma definição de mensagens e RPCs, reduzindo inconsistências.
- **Dados em memória**: suficiente para demonstrar a comunicação remota sem depender de banco de dados.
- **Canal inseguro local (`insecure_channel`)**: adequado para ambiente acadêmico/local; em produção usaria TLS.
- **CLI no cliente**: foco na comunicação remota, sem interface gráfica.

## Por que gRPC neste cenário?

Em relação a uma API REST típica:

- contrato tipado e gerado automaticamente a partir do `.proto`;
- serialização binária eficiente (Protobuf);
- chamadas RPC com nomes e tipos explícitos (`InvocarPersonagem`, etc.);
- menos boilerplate de rotas HTTP/JSON para um serviço interno entre processos.
