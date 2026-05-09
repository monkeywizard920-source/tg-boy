from __future__ import annotations

import logging
import tempfile
from pathlib import Path
from typing import Any

logger = logging.getLogger(__name__)


class ImageService:
    def __init__(self, *, width: int = 900, padding: int = 48, font_size: int = 38) -> None:
        self._width = width
        self._padding = padding
        self._font_size = font_size

    def create_text_image(self, text: str) -> Path:
        try:
            from PIL import Image, ImageDraw
        except ModuleNotFoundError as error:
            raise RuntimeError("Pillow is required for fun image generation") from error

        font = self._load_font()
        wrapped_lines = self._wrap_text(text=text, font=font, max_width=self._width - self._padding * 2)
        line_height = self._line_height(font)
        height = max(240, self._padding * 2 + line_height * len(wrapped_lines))

        image = Image.new("RGB", (self._width, height), color="white")
        draw = ImageDraw.Draw(image)
        y = self._padding
        for line in wrapped_lines:
            draw.text((self._padding, y), line, fill="black", font=font)
            y += line_height

        temp = tempfile.NamedTemporaryFile(prefix="fun_mode_", suffix=".png", delete=False)
        temp_path = Path(temp.name)
        temp.close()
        image.save(temp_path, format="PNG")
        return temp_path

    def cleanup(self, path: Path) -> None:
        try:
            path.unlink(missing_ok=True)
        except OSError as error:
            logger.warning("Failed to cleanup fun image %s: %s", path, error)

    def _load_font(self) -> Any:
        from PIL import ImageFont

        candidates = (
            "arial.ttf",
            "segoeui.ttf",
            "DejaVuSans.ttf",
            "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
        )
        for candidate in candidates:
            try:
                return ImageFont.truetype(candidate, self._font_size)
            except OSError:
                continue
        logger.warning("No TrueType font found for fun image; using Pillow default font")
        return ImageFont.load_default()

    @staticmethod
    def _line_height(font: Any) -> int:
        bbox = font.getbbox("Ag")
        return max(24, bbox[3] - bbox[1] + 14)

    @staticmethod
    def _text_width(text: str, font: Any) -> int:
        bbox = font.getbbox(text)
        return bbox[2] - bbox[0]

    def _wrap_text(
        self,
        *,
        text: str,
        font: Any,
        max_width: int,
    ) -> list[str]:
        lines: list[str] = []
        for raw_line in text.splitlines() or [text]:
            words = raw_line.split()
            if not words:
                lines.append("")
                continue

            current = words[0]
            for word in words[1:]:
                candidate = f"{current} {word}"
                if self._text_width(candidate, font) <= max_width:
                    current = candidate
                else:
                    lines.extend(self._split_long_line(current, font, max_width))
                    current = word
            lines.extend(self._split_long_line(current, font, max_width))
        return lines

    def _split_long_line(
        self,
        text: str,
        font: Any,
        max_width: int,
    ) -> list[str]:
        if self._text_width(text, font) <= max_width:
            return [text]

        chunks: list[str] = []
        current = ""
        for char in text:
            candidate = current + char
            if current and self._text_width(candidate, font) > max_width:
                chunks.append(current)
                current = char
            else:
                current = candidate
        if current:
            chunks.append(current)
        return chunks
