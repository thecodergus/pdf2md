# Codemagus: Tipos, enums e dataclasses para pipeline PDF→Markdown
from pathlib import Path
from typing import NamedTuple, TypeAlias, Sequence
from dataclasses import dataclass


class ChunkInfo(NamedTuple):
    pdf_path: Path
    md_path: Path
    index_: int


@dataclass(frozen=True, slots=True)
class PipelineConfig:
    chunk_size: int
    cache_dir: Path
    output_dir: Path


ChunkList: TypeAlias = Sequence[ChunkInfo]
