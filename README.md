# Gacha Game — Projeto gRPC

Sistema distribuído em **Python** que demonstra comunicação remota com **gRPC** e contrato definido em **Protocol Buffers** (`.proto`).

O tema é um mini **Gacha Game**: o jogador invoca personagens, lista a coleção e evolui personagens obtidos. Os dados ficam em memória no servidor (sem banco de dados). A interação do cliente é por linha de comando.

## Requisitos

- Python 3.10+ (testado com 3.12)
- Dependências listadas em `requirements.txt`

## Estrutura do projeto

```
Projeto-gRPC/
├── protos/
│   └── gacha.proto              # Contrato do serviço (fonte da verdade)
├── generated/
│   ├── gacha_pb2.py             # Mensagens geradas pelo Protocol Buffers
│   └── gacha_pb2_grpc.py        # Stubs gRPC gerados automaticamente
├── server.py                    # Servidor gRPC
├── client.py                    # Cliente gRPC (CLI)
├── generate_stubs.py            # Regenera o código a partir do .proto
├── requirements.txt
├── apresentacao.html            # Slides no navegador
├── apresentacao.pptx            # Slides em PowerPoint
├── gerar_apresentacao_pptx.py   # Script que gera o .pptx
└── README.md
```

## Entidade e operações

### Entidade: `Personagem`

| Campo      | Tipo   | Descrição                             |
|------------|--------|---------------------------------------|
| `id`       | int32  | Identificador único na coleção        |
| `nome`     | string | Nome do personagem                    |
| `raridade` | string | Comum, Raro, Épico ou Lendário        |
| `elemento` | string | Fogo, Água, Terra, Ar, Luz ou Trevas  |
| `nivel`    | int32  | Nível atual (inicia em 1, máximo 100) |

### Operações remotas (RPCs)

| RPC                  | Descrição                                           |
|----------------------|-----------------------------------------------------|
| `InvocarPersonagem`  | Sorteia um personagem e adiciona à coleção          |
| `ListarPersonagens`  | Retorna todos os personagens obtidos                |
| `EvoluirPersonagem`  | Aumenta em 1 o nível de um personagem pelo `id`     |

## Como executar

### 1. Instalar dependências

Na pasta do projeto:

```bash
pip install -r requirements.txt
```

### 2. Gerar os stubs (se necessário)

Os arquivos em `generated/` já podem estar versionados. Para regenerá-los após alterar o `.proto`:

```bash
python generate_stubs.py
```

Arquivos gerados automaticamente pelo compilador Protocol Buffers:

- `generated/gacha_pb2.py` — classes das mensagens (`Personagem`, requests e responses)
- `generated/gacha_pb2_grpc.py` — stubs do serviço (`GachaServiceStub`, `GachaServiceServicer`)

### 3. Subir o servidor

Em um terminal:

```bash
python server.py
```

O servidor escuta em `127.0.0.1:50051`.

### 4. Rodar o cliente

Em **outro** terminal:

```bash
python client.py
```

Menu do cliente:

1. Invocar personagem  
2. Listar personagens  
3. Evoluir personagem  
0. Sair  

## Como funciona a comunicação

1. O cliente abre um canal gRPC para `localhost:50051`.
2. Usa o **stub** gerado (`GachaServiceStub`) para chamar os métodos remotos.
3. As mensagens são serializadas em **Protobuf** e enviadas ao servidor.
4. O servidor processa a requisição (coleção em memória) e devolve uma resposta tipada.

```
Cliente  →  Canal gRPC  →  Servidor  →  Resposta Protobuf
```

## Decisões arquiteturais

- **Contrato único em `.proto`**: cliente e servidor compartilham a mesma definição de mensagens e RPCs.
- **Dados em memória**: suficiente para demonstrar a comunicação remota sem banco de dados. Ao encerrar o servidor, a coleção é perdida.
- **Canal local sem TLS** (`insecure_channel`): adequado para ambiente acadêmico; em produção usaria TLS.
- **CLI no cliente**: o foco da atividade é a comunicação remota, não a interface gráfica.
- **Bind em `127.0.0.1`**: mais estável no Windows do que `[::]` (IPv6).

## gRPC × REST neste cenário

Para um serviço interno entre processos (cliente ↔ servidor do gacha):

| Aspecto        | REST típico              | gRPC neste projeto                          |
|----------------|--------------------------|----------------------------------------------|
| Contrato       | Rotas HTTP + JSON        | Tipado no `.proto`                           |
| Código         | Serialização manual      | Stubs gerados automaticamente                |
| Chamadas       | `POST /personagens` etc. | RPCs com nomes claros (`InvocarPersonagem`)  |
| Serialização   | Texto (JSON)             | Binária (Protobuf), mais eficiente           |

## Apresentação

Os quatro pontos pedidos na atividade estão nos slides:

| Arquivo              | Como usar                                      |
|----------------------|------------------------------------------------|
| `apresentacao.html`  | Abrir no navegador · `F` tela cheia · setas    |
| `apresentacao.pptx`  | Abrir no PowerPoint ou Google Slides           |

Para regenerar o PowerPoint:

```bash
pip install python-pptx
python gerar_apresentacao_pptx.py
```

### Pontos da apresentação

1. **Por que o contrato foi assim** — entidade composta `Personagem`, RPCs com nomes do domínio, request/response separados.
2. **Como ocorre a comunicação** — canal gRPC, stub, serialização Protobuf, servidor em memória.
3. **Arquivos gerados** — `gacha_pb2.py` e `gacha_pb2_grpc.py`.
4. **Vantagens do gRPC vs REST** — tipagem, geração de código, eficiência e chamadas RPC explícitas.

## Problemas comuns

**Erro: `Failed to bind to address ...:50051`**

A porta já está em uso (outro `server.py` aberto). Feche o processo antigo ou o terminal correspondente e tente de novo.

**Cliente não conecta**

Confirme que o servidor está rodando antes de iniciar o cliente.

## Autores

Projeto acadêmico — disciplina de sistemas distribuídos / gRPC.
