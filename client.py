"""Cliente gRPC do Gacha Game (interação por linha de comando)."""

from __future__ import annotations

import sys

import grpc

from generated import gacha_pb2, gacha_pb2_grpc

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

ENDERECO_SERVIDOR = "localhost:50051"


def formatar_personagem(p: gacha_pb2.Personagem) -> str:
    return (
        f"[ID {p.id}] {p.nome} | "
        f"Raridade: {p.raridade} | "
        f"Elemento: {p.elemento} | "
        f"Nível: {p.nivel}"
    )


def invocar(stub: gacha_pb2_grpc.GachaServiceStub) -> None:
    resposta = stub.InvocarPersonagem(gacha_pb2.InvocarRequest())
    print(f"\n{resposta.mensagem}")
    print(formatar_personagem(resposta.personagem))


def listar(stub: gacha_pb2_grpc.GachaServiceStub) -> None:
    resposta = stub.ListarPersonagens(gacha_pb2.ListarRequest())
    print(f"\nColeção ({resposta.total} personagem(ns)):")
    if resposta.total == 0:
        print("  Nenhum personagem ainda. Use a opção 1 para invocar!")
        return
    for personagem in resposta.personagens:
        print(f"  {formatar_personagem(personagem)}")


def evoluir(stub: gacha_pb2_grpc.GachaServiceStub) -> None:
    try:
        id_personagem = int(input("Digite o ID do personagem: ").strip())
    except ValueError:
        print("ID inválido. Informe um número inteiro.")
        return

    resposta = stub.EvoluirPersonagem(gacha_pb2.EvoluirRequest(id=id_personagem))
    print(f"\n{resposta.mensagem}")
    if resposta.sucesso and resposta.HasField("personagem"):
        print(formatar_personagem(resposta.personagem))


def menu() -> None:
    print(
        """
=== Gacha Game (cliente gRPC) ===
1 - Invocar personagem
2 - Listar personagens
3 - Evoluir personagem
0 - Sair
"""
    )


def main() -> None:
    with grpc.insecure_channel(ENDERECO_SERVIDOR) as canal:
        stub = gacha_pb2_grpc.GachaServiceStub(canal)
        print(f"Conectado ao servidor em {ENDERECO_SERVIDOR}")

        while True:
            menu()
            opcao = input("Escolha uma opção: ").strip()

            try:
                if opcao == "1":
                    invocar(stub)
                elif opcao == "2":
                    listar(stub)
                elif opcao == "3":
                    evoluir(stub)
                elif opcao == "0":
                    print("Encerrando cliente.")
                    break
                else:
                    print("Opção inválida.")
            except grpc.RpcError as erro:
                print(f"\nErro na chamada remota: {erro.code().name} - {erro.details()}")


if __name__ == "__main__":
    main()
