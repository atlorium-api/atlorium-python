"""
Приём изображений для OCR и модерации: путь, байты или поток.

API ждёт картинку строкой Base64 внутри JSON. SDK кодирует её сам, пользователю остаётся
передать то, что у него есть под рукой.
"""

from __future__ import annotations

import base64
import os
import re
from pathlib import Path
from typing import IO, Union

__all__ = ["FileInput", "encode_image"]

FileInput = Union[str, bytes, bytearray, memoryview, "os.PathLike[str]", IO[bytes]]
"""Изображение: путь (``str`` или ``Path``), байты или открытый бинарный поток.

Строка, которая не является путём к существующему файлу, считается уже готовым Base64
(допускается и data-URL вида ``data:image/png;base64,...``) и уходит на сервер как есть.
Строка, похожая на путь к файлу, которого нет, — ошибка ``FileNotFoundError``.
"""

# Строка длиннее этого предела — точно не путь, а содержимое; проверять файловую систему незачем.
_MAX_PATH_LENGTH = 4096

# В Base64 не бывает ни точки, ни обратной косой черты, поэтому строка с точкой и разделителем
# пути или с расширением файла — это опечатка в пути, а не содержимое картинки.
_PATH_LIKE = re.compile(r"\.(png|jpe?g|gif|webp|bmp|tiff?|heic|pdf)$|/.*\.|\\", re.IGNORECASE)


def encode_image(image: FileInput) -> str:
    """Превращает изображение из любого поддерживаемого вида в строку Base64."""
    if isinstance(image, (bytes, bytearray, memoryview)):
        return base64.b64encode(bytes(image)).decode("ascii")
    if isinstance(image, os.PathLike):
        return base64.b64encode(Path(image).read_bytes()).decode("ascii")
    if isinstance(image, str):
        if image.startswith("data:") or len(image) > _MAX_PATH_LENGTH:
            return image
        try:
            if os.path.isfile(image):
                return base64.b64encode(Path(image).read_bytes()).decode("ascii")
        except (OSError, ValueError):
            pass
        if image.startswith(("http://", "https://")):
            raise ValueError("API не принимает ссылку на изображение: скачайте его и передайте байты")
        if "\n" not in image and _PATH_LIKE.search(image.strip()):
            raise FileNotFoundError(f"Файл изображения не найден: {image}")
        return image
    if hasattr(image, "read"):
        content: object = image.read()
        if not isinstance(content, (bytes, bytearray, memoryview)):
            raise TypeError("Поток изображения нужно открывать в бинарном режиме: open(path, 'rb')")
        return base64.b64encode(bytes(content)).decode("ascii")
    raise TypeError(f"Неподдерживаемый тип изображения: {type(image).__name__}")
