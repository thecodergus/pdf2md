# Codemagus: Entry point do pipeline PDF→Markdown modular e funcional
from pathlib import Path
from src.types import PipelineConfig
from src.validation import is_valid_pdf
from src.chunking import split_pdf_chunks
from src.cache_manager import CacheManager
from src.conversion import configure_docling_converter, convert_chunk_to_markdown
from src.merge import merge_markdown_chunks
from src.ui import process_with_progress
import logging, sys
from dotenv import load_dotenv


def main() -> None:
    # Configuração de caminhos e parâmetros
    input_pdf = Path("inputs/Manual de publicações da SBC.pdf").resolve()
    # input_pdf = Path(
    #     "inputs/PISA 2015 - Assessment Analytical Framework Science Reading Math Financial Collaborative.pdf"
    # ).resolve()
    # input_pdf = Path(input("Digite o caminho do PDF: ")).resolve()
    config = PipelineConfig(
        chunk_size=1, cache_dir=Path("cache"), output_dir=Path("outputs")
    )

    if not input_pdf.exists() or not input_pdf.is_file():
        print("Arquivo não encontrado.")
        return
    if not is_valid_pdf(input_pdf):
        print("PDF inválido ou corrompido.")
        return

    config.cache_dir.mkdir(exist_ok=True)
    config.output_dir.mkdir(exist_ok=True)

    # Chunking
    chunks = split_pdf_chunks(input_pdf, config.chunk_size, config.cache_dir)

    # Cache e conversão
    cache = CacheManager(config.cache_dir)
    converter = configure_docling_converter()

    def process_chunk(chunk):
        if not cache.is_chunk_processed(chunk):
            convert_chunk_to_markdown(chunk, converter)
            cache.mark_chunk_processed(chunk)

    process_with_progress(chunks, process_chunk)
    cache.close()

    # Merge final
    output_md = config.output_dir / f"{input_pdf.stem}.md"
    merge_markdown_chunks(chunks, output_md)
    print(f"Conversão concluída. Markdown salvo em: {output_md}")

    # Limpar
    cache.clear_cache_parallel(chunks)


if __name__ == "__main__":
    logging.disable(sys.maxsize)
    load_dotenv()
    main()
