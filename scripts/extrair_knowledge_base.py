#!/usr/bin/env python3
"""Extrai texto dos PDFs e cria knowledge base para o chat."""

import json
import re
from pathlib import Path
from pypdf import PdfReader

DOWNLOADS_DIR = Path.home() / "Downloads"
PROJECT_DIR = Path(__file__).parent.parent
KB_DIR = PROJECT_DIR / "knowledge_base"

# PDFs da pasta ~/Downloads (livros e materiais de referencia)
PDFS_DOWNLOADS = [
    "foba lenguaje visual Valor y Claes Tonales teorico.pdf",
    "Introducao_aos_Estudos_das_Artes_Visuais.pdf",
    "LIVRO_UNICO.pdf",
    "tonalidade.pdf",
    "valor-tonal.pdf",
    "Valores_Tonais_101_Guia_Completo.pdf",
]

# PDFs da pasta pdf/ do projeto ( automatico - todos os .pdf da pasta )


def limpar_texto(texto: str) -> str:
    """Remove caracteres especiais e normaliza espaços."""
    texto = re.sub(r'\s+', ' ', texto)
    texto = re.sub(r'[^\w\s.,;:!?()\-\"\'áàâãéèêíìîóòôõúùûçñÁÀÂÃÉÈÊÍÌÎÓÒÔÕÚÙÛÇÑ]', '', texto)
    return texto.strip()


def extrair_texto_pdf(caminho: Path) -> dict:
    """Extrai texto e metadados de um PDF."""
    reader = PdfReader(str(caminho))
    texto_total = []
    for page in reader.pages:
        texto = page.extract_text()
        if texto:
            texto_total.append(limpar_texto(texto))
    
    return {
        "arquivo": caminho.name,
        "titulo": caminho.stem.replace("_", " ").replace("-", " ").title(),
        "paginas": len(reader.pages),
        "tamanho_kb": round(caminho.stat().st_size / 1024),
        "texto": "\n\n".join(texto_total),
    }


def chunk_texto(texto: str, tamanho: int = 1500) -> list[str]:
    """Divide texto em chunks menores para busca."""
    paragrafos = texto.split("\n\n")
    chunks = []
    chunk_atual = ""
    
    for p in paragrafos:
        if len(chunk_atual) + len(p) > tamanho:
            if chunk_atual:
                chunks.append(chunk_atual.strip())
            chunk_atual = p
        else:
            chunk_atual += "\n\n" + p if chunk_atual else p
    
    if chunk_atual.strip():
        chunks.append(chunk_atual.strip())
    
    return chunks


def main():
    KB_DIR.mkdir(exist_ok=True)
    
    knowledge_base = {
        "versao": "1.1",
        "fontes": [],
        "documentos": [],
    }
    
    print("Extraindo texto dos PDFs...\n")
    
    # PDFs do Downloads
    print("--- PDFs do Downloads ---")
    for pdf_nome in PDFS_DOWNLOADS:
        caminho = DOWNLOADS_DIR / pdf_nome
        if not caminho.exists():
            print(f"  ! Nao encontrado: {pdf_nome}")
            continue
        
        dados = extrair_texto_pdf(caminho)
        chunks = chunk_texto(dados["texto"])
        
        doc = {
            "id": len(knowledge_base["documentos"]) + 1,
            "arquivo": dados["arquivo"],
            "titulo": dados["titulo"],
            "origem": "downloads",
            "paginas": dados["paginas"],
            "tamanho_kb": dados["tamanho_kb"],
            "chunks": chunks,
            "total_chunks": len(chunks),
        }
        
        knowledge_base["documentos"].append(doc)
        knowledge_base["fontes"].append(dados["arquivo"])
        
        print(f"  OK {dados['arquivo']} ({dados['paginas']} pag, {len(chunks)} chunks)")
    
    # PDFs do projeto (automatico - todos os .pdf da pasta pdf/)
    print("\n--- PDFs do Projeto (pdf/) ---")
    pdf_dir = PROJECT_DIR / "pdf"
    pdfs_projeto = sorted(pdf_dir.glob("*.pdf"))
    for caminho in pdfs_projeto:
        
        dados = extrair_texto_pdf(caminho)
        chunks = chunk_texto(dados["texto"])
        
        doc = {
            "id": len(knowledge_base["documentos"]) + 1,
            "arquivo": dados["arquivo"],
            "titulo": dados["titulo"],
            "origem": "projeto",
            "paginas": dados["paginas"],
            "tamanho_kb": dados["tamanho_kb"],
            "chunks": chunks,
            "total_chunks": len(chunks),
        }
        
        knowledge_base["documentos"].append(doc)
        knowledge_base["fontes"].append(dados["arquivo"])
        
        print(f"  OK {dados['arquivo']} ({dados['paginas']} pag, {len(chunks)} chunks)")
    
    # Salvar JSON completo
    kb_path = KB_DIR / "knowledge_base.json"
    with open(kb_path, "w", encoding="utf-8") as f:
        json.dump(knowledge_base, f, ensure_ascii=False, indent=2)
    
    # Salvar texto consolidado (para referência rápida)
    txt_path = KB_DIR / "knowledge_base.txt"
    with open(txt_path, "w", encoding="utf-8") as f:
        f.write(f"# Knowledge Base - Tono Art\n")
        f.write(f"# Total de documentos: {len(knowledge_base['documentos'])}\n\n")
        for doc in knowledge_base["documentos"]:
            f.write(f"\n{'='*60}\n")
            f.write(f"## {doc['titulo']}\n")
            f.write(f"Arquivo: {doc['arquivo']}\n")
            f.write(f"Paginas: {doc['paginas']}\n")
            f.write(f"{'='*60}\n\n")
            for chunk in doc["chunks"]:
                f.write(chunk + "\n\n")
    
    print(f"\nPronto! Knowledge base salva em:")
    print(f"  JSON: {kb_path}")
    print(f"  TXT:  {txt_path}")
    print(f"  Documentos: {len(knowledge_base['documentos'])}")
    print(f"  Total chunks: {sum(d['total_chunks'] for d in knowledge_base['documentos'])}")


if __name__ == "__main__":
    main()
