#!/usr/bin/env python3
"""Utilitário para consultar a knowledge base do chat."""

import json
from pathlib import Path

KB_DIR = Path(__file__).parent / "knowledge_base"
KB_FILE = KB_DIR / "knowledge_base.json"


def carregar_kb() -> dict:
    """Carrega a knowledge base do arquivo JSON."""
    with open(KB_FILE, "r", encoding="utf-8") as f:
        return json.load(f)


def buscar(documento_id: int = None, termo: str = None) -> list[dict]:
    """Busca na knowledge base por documento ou termo."""
    kb = carregar_kb()
    resultados = []
    
    for doc in kb["documentos"]:
        if documento_id and doc["id"] != documento_id:
            continue
        
        if termo:
            chunks_encontrados = []
            for chunk in doc["chunks"]:
                if termo.lower() in chunk.lower():
                    chunks_encontrados.append(chunk)
            if chunks_encontrados:
                resultados.append({
                    "documento": doc["titulo"],
                    "arquivo": doc["arquivo"],
                    "chunks": chunks_encontrados,
                })
        else:
            resultados.append({
                "documento": doc["titulo"],
                "arquivo": doc["arquivo"],
                "total_chunks": doc["total_chunks"],
                "paginas": doc["paginas"],
            })
    
    return resultados


def listar_documentos():
    """Lista todos os documentos da knowledge base."""
    kb = carregar_kb()
    print(f"\nKnowledge Base - {len(kb['documentos'])} documentos\n")
    for doc in kb["documentos"]:
        print(f"  [{doc['id']}] {doc['titulo']}")
        print(f"      Arquivo: {doc['arquivo']}")
        print(f"      Paginas: {doc['paginas']} | Chunks: {doc['total_chunks']}")
        print()


def contexto_para_chat(documento_id: int = None, max_tokens: int = 4000) -> str:
    """Gera contexto formatado para incluir no chat."""
    kb = carregar_kb()
    partes = []
    total_chars = 0
    max_chars = max_tokens * 4  # aproximacao: 1 token ~ 4 chars
    
    for doc in kb["documentos"]:
        if documento_id and doc["id"] != documento_id:
            continue
        
        for chunk in doc["chunks"]:
            if total_chars + len(chunk) > max_chars:
                break
            partes.append(f"[{doc['titulo']}]\n{chunk}")
            total_chars += len(chunk)
        
        if total_chars >= max_chars:
            break
    
    return "\n\n---\n\n".join(partes)


if __name__ == "__main__":
    import sys
    
    if len(sys.argv) < 2:
        print("Uso:")
        print("  python consultar_kb.py list              # Listar documentos")
        print("  python consultar_kb.py search <termo>    # Buscar termo")
        print("  python consultar_kb.py context [id]      # Gerar contexto")
        sys.exit(0)
    
    cmd = sys.argv[1]
    
    if cmd == "list":
        listar_documentos()
    
    elif cmd == "search" and len(sys.argv) > 2:
        termo = " ".join(sys.argv[2:])
        resultados = buscar(termo=termo)
        if resultados:
            print(f"\nResultados para '{termo}':\n")
            for r in resultados:
                print(f"  {r['documento']} ({len(r['chunks'])} chunks)")
                for chunk in r["chunks"][:2]:
                    print(f"    > {chunk[:100]}...")
                print()
        else:
            print(f"Nenhum resultado para '{termo}'")
    
    elif cmd == "context":
        doc_id = int(sys.argv[2]) if len(sys.argv) > 2 else None
        ctx = contexto_para_chat(doc_id)
        print(ctx[:2000] + "..." if len(ctx) > 2000 else ctx)
    
    else:
        print("Comando invalido. Use: list, search, ou context")
