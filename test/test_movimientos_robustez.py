import pytest

from core import movimientos


def test_error_inesperado_no_se_oculta(
    tmp_path,
    monkeypatch,
):
    # ARRANGE
    archivo = tmp_path / "foto.jpg"
    archivo.write_bytes(b"contenido")

    clasificacion = [
        ("foto.jpg", "Fotos"),
    ]

    def mover_falso(*args, **kwargs):
        raise RuntimeError(
            "Fallo inesperado simulado"
        )

    monkeypatch.setattr(
        movimientos.shutil,
        "move",
        mover_falso,
    )

    # ACT + ASSERT
    with pytest.raises(
        RuntimeError,
        match="Fallo inesperado simulado",
    ):
        movimientos.mover_archivos(
            clasificacion,
            tmp_path,
        )
