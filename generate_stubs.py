"""Gera os stubs Python a partir do contrato Protocol Buffers."""

from pathlib import Path

from grpc_tools import protoc

ROOT = Path(__file__).resolve().parent
PROTO_DIR = ROOT / "protos"
OUT_DIR = ROOT / "generated"


def main() -> None:
    OUT_DIR.mkdir(exist_ok=True)
    (OUT_DIR / "__init__.py").touch(exist_ok=True)

    result = protoc.main(
        [
            "grpc_tools.protoc",
            f"-I{PROTO_DIR}",
            f"--python_out={OUT_DIR}",
            f"--grpc_python_out={OUT_DIR}",
            str(PROTO_DIR / "gacha.proto"),
        ]
    )

    if result != 0:
        raise SystemExit(f"Falha ao gerar stubs (código {result}).")

    # Ajusta o import gerado para funcionar como pacote local.
    grpc_file = OUT_DIR / "gacha_pb2_grpc.py"
    content = grpc_file.read_text(encoding="utf-8")
    grpc_file.write_text(
        content.replace("import gacha_pb2 as gacha__pb2", "from generated import gacha_pb2 as gacha__pb2"),
        encoding="utf-8",
    )

    print(f"Stubs gerados em: {OUT_DIR}")
    print("  - gacha_pb2.py")
    print("  - gacha_pb2_grpc.py")


if __name__ == "__main__":
    main()
