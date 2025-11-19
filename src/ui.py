# Codemagus: Interface Rich para barra de progresso elegante
from typing import Sequence, Callable
from .types import ChunkInfo
from rich.progress import (
    Progress,
    BarColumn,
    TextColumn,
    TaskProgressColumn,
    TimeRemainingColumn,
)


def process_with_progress(
    chunks: Sequence[ChunkInfo], process_fn: Callable[[ChunkInfo], None]
) -> None:
    """
    Processa a conversão de chunks com barra de progresso Rich e títulos dinâmicos.
    """
    with Progress(
        TextColumn("[bold blue]Conversão PDF → Markdown:"),
        BarColumn(),
        TaskProgressColumn(),
        TimeRemainingColumn(),
        transient=True,
        expand=True,
    ) as progress:
        task = progress.add_task("Convertendo chunks...", total=len(chunks))
        for chunk in chunks:
            progress.update(task, description=f"Convertendo chunk {chunk.index}...")
            process_fn(chunk)
            progress.update(task, advance=1)
