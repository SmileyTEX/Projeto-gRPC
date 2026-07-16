"""Servidor gRPC do Gacha Game."""

from __future__ import annotations

import random
import sys
from concurrent import futures

import grpc

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

from generated import gacha_pb2, gacha_pb2_grpc

# Pool de personagens possíveis nas invocações.
POOL_PERSONAGENS = [
    ("Goblin", "Comum", "Terra"),
    ("Slime", "Comum", "Água"),
    ("Lobo Flamejante", "Comum", "Fogo"),
    ("Arqueira Élfica", "Raro", "Ar"),
    ("Mago de Gelo", "Raro", "Água"),
    ("Guerreiro Sombrio", "Raro", "Trevas"),
    ("Dragão de Fogo", "Épico", "Fogo"),
    ("Sacerdotisa da Luz", "Épico", "Luz"),
    ("Titã da Terra", "Épico", "Terra"),
    ("Fênix Eterna", "Lendário", "Fogo"),
    ("Leviatã Abissal", "Lendário", "Água"),
    ("Arquianjo Celestial", "Lendário", "Luz"),
]

PESOS_RARIDADE = {
    "Comum": 50,
    "Raro": 30,
    "Épico": 15,
    "Lendário": 5,
}

HOST = "127.0.0.1"
PORTA = 50051


class GachaService(gacha_pb2_grpc.GachaServiceServicer):
    """Implementação do serviço remoto em memória."""

    def __init__(self) -> None:
        self._proximo_id = 1
        self._colecao: dict[int, gacha_pb2.Personagem] = {}

    def InvocarPersonagem(self, request, context):
        nome, raridade, elemento = self._sortear_personagem()
        personagem = gacha_pb2.Personagem(
            id=self._proximo_id,
            nome=nome,
            raridade=raridade,
            elemento=elemento,
            nivel=1,
        )
        self._colecao[personagem.id] = personagem
        self._proximo_id += 1

        return gacha_pb2.InvocarResponse(
            personagem=personagem,
            mensagem=f"Você invocou {personagem.nome} ({personagem.raridade})!",
        )

    def ListarPersonagens(self, request, context):
        personagens = list(self._colecao.values())
        return gacha_pb2.ListarResponse(
            personagens=personagens,
            total=len(personagens),
        )

    def EvoluirPersonagem(self, request, context):
        personagem = self._colecao.get(request.id)
        if personagem is None:
            return gacha_pb2.EvoluirResponse(
                sucesso=False,
                mensagem=f"Personagem com id {request.id} não encontrado.",
            )

        if personagem.nivel >= 100:
            return gacha_pb2.EvoluirResponse(
                personagem=personagem,
                sucesso=False,
                mensagem=f"{personagem.nome} já está no nível máximo (100).",
            )

        personagem.nivel += 1
        return gacha_pb2.EvoluirResponse(
            personagem=personagem,
            sucesso=True,
            mensagem=f"{personagem.nome} evoluiu para o nível {personagem.nivel}!",
        )

    def _sortear_personagem(self) -> tuple[str, str, str]:
        pesos = [PESOS_RARIDADE[p[1]] for p in POOL_PERSONAGENS]
        return random.choices(POOL_PERSONAGENS, weights=pesos, k=1)[0]


def servir() -> None:
    servidor = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    gacha_pb2_grpc.add_GachaServiceServicer_to_server(GachaService(), servidor)
    endereco = f"{HOST}:{PORTA}"
    servidor.add_insecure_port(endereco)
    servidor.start()
    print(f"Servidor Gacha gRPC ouvindo em {endereco}")
    print("Pressione Ctrl+C para encerrar.")
    servidor.wait_for_termination()


if __name__ == "__main__":
    servir()
