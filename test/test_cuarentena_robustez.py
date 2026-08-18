from core import cuarentena


def configurar_cuarentena_temporal(tmp_path, monkeypatch):
    """
    Redirige la cuarentena y su registro a un
    directorio temporal controlado por pytest.
    """

    carpeta = tmp_path / "quarantine"
    registro = carpeta / "alertas.log"

    monkeypatch.setattr(
        cuarentena,
        "CUARENTENA",
        carpeta,
    )

    monkeypatch.setattr(
        cuarentena,
        "REGISTRO_CUARENTENA",
        registro,
    )

    return carpeta, registro


def test_colisiones_multiples(tmp_path, monkeypatch):
    # ARRANGE
    carpeta, _ = configurar_cuarentena_temporal(
        tmp_path,
        monkeypatch,
    )

    carpeta.mkdir()

    (carpeta / "programa.jpg").write_bytes(b"original")
    (carpeta / "programa_1.jpg").write_bytes(b"colision")

    origen = tmp_path / "programa.jpg"
    origen.write_bytes(b"MZ")

    # ACT
    destino = cuarentena.poner_en_cuarentena(
        origen,
        "PE/Windows executable",
        ".jpg",
    )

    # ASSERT
    assert destino == carpeta / "programa_2.jpg"
    assert destino.read_bytes() == b"MZ"
    assert not origen.exists()

    assert (carpeta / "programa.jpg").read_bytes() == b"original"
    assert (carpeta / "programa_1.jpg").read_bytes() == b"colision"


def test_nombre_unicode_y_espacios(tmp_path, monkeypatch):
    # ARRANGE
    carpeta, _ = configurar_cuarentena_temporal(
        tmp_path,
        monkeypatch,
    )

    origen = tmp_path / "fíchéró sospechoso 日本.jpg"
    origen.write_bytes(b"MZ")

    # ACT
    destino = cuarentena.poner_en_cuarentena(
        origen,
        "PE/Windows executable",
        ".jpg",
    )

    # ASSERT
    assert destino == carpeta / "fíchéró sospechoso 日本.jpg"
    assert destino.exists()
    assert not origen.exists()


def test_archivo_sin_extension(tmp_path, monkeypatch):
    # ARRANGE
    carpeta, _ = configurar_cuarentena_temporal(
        tmp_path,
        monkeypatch,
    )

    origen = tmp_path / "sospechoso"
    origen.write_bytes(b"MZ")

    # ACT
    destino = cuarentena.poner_en_cuarentena(
        origen,
        "PE/Windows executable",
        "",
    )

    # ASSERT
    assert destino == carpeta / "sospechoso"
    assert destino.exists()
    assert not origen.exists()


def test_no_sobrescribe_archivo_existente(tmp_path, monkeypatch):
    # ARRANGE
    carpeta, _ = configurar_cuarentena_temporal(
        tmp_path,
        monkeypatch,
    )

    carpeta.mkdir()

    existente = carpeta / "documento.pdf"
    existente.write_bytes(b"%PDF-original")

    origen = tmp_path / "documento.pdf"
    origen.write_bytes(b"MZ-malicioso")

    # ACT
    destino = cuarentena.poner_en_cuarentena(
        origen,
        "PE/Windows executable",
        ".pdf",
    )

    # ASSERT
    assert existente.read_bytes() == b"%PDF-original"

    assert destino == carpeta / "documento_1.pdf"
    assert destino.read_bytes() == b"MZ-malicioso"


def test_registro_varias_entradas(tmp_path, monkeypatch):
    # ARRANGE
    _, registro = configurar_cuarentena_temporal(
        tmp_path,
        monkeypatch,
    )

    archivo_1 = tmp_path / "uno.jpg"
    archivo_2 = tmp_path / "dos.pdf"

    archivo_1.write_bytes(b"MZ")
    archivo_2.write_bytes(b"MZ")

    # ACT
    cuarentena.poner_en_cuarentena(
        archivo_1,
        "PE/Windows executable",
        ".jpg",
    )

    cuarentena.poner_en_cuarentena(
        archivo_2,
        "PE/Windows executable",
        ".pdf",
    )

    contenido = registro.read_text(
        encoding="utf-8"
    )

    # ASSERT
    lineas = contenido.splitlines()

    assert len(lineas) == 2

    assert "uno.jpg" in lineas[0]
    assert "dos.pdf" in lineas[1]

    assert "PE/Windows executable" in lineas[0]
    assert "PE/Windows executable" in lineas[1]
