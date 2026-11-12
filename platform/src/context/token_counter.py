"""Contador e estimador de tokens para gerenciamento de orçamentos de atenção."""

import re
from typing import Callable, Optional


class TokenCounter:
    """Calculador de tokens parametrizável com suporte a tokenizadores reais ou calibrados."""

    def __init__(self, custom_tokenizer: Optional[Callable[[str], int]] = None):
        """
        Inicializa o contador.
        :param custom_tokenizer: Função opcional que recebe uma string e retorna a contagem exata de tokens.
        """
        self._custom_tokenizer = custom_tokenizer
        # Regex calibrada para segmentação aproximada de BPE (palavras, números, pontuação e espaços múltiplos)
        self._token_pattern = re.compile(r"\w+|[^\w\s]|\s+", re.UNICODE)

    def count(self, text: str) -> int:
        """
        Calcula a contagem de tokens para o texto fornecido.
        :param text: Conteúdo a ser avaliado.
        :return: Número estimado ou exato de tokens.
        """
        if not text:
            return 0

        if self._custom_tokenizer is not None:
            return self._custom_tokenizer(text)

        # Heurística BPE-calibrada:
        # 1. Segmenta palavras, símbolos individuais e blocos de espaços.
        # 2. Palavras muito longas (> 4 chars) ou caracteres especiais/acentuados consomem tokens fracionados adicionais.
        matches = self._token_pattern.findall(text)
        token_count = 0
        for match in matches:
            length = len(match)
            if match.isspace():
                # Espaços consecutivos agregam tokens
                token_count += max(1, length // 4)
            elif length <= 4:
                token_count += 1
            else:
                # Palavras longas ou palavras de código em camelCase/snake_case
                token_count += max(1, (length + 2) // 3)

        return token_count

    def truncate_to_tokens(self, text: str, max_tokens: int) -> str:
        """
        Trunca um texto para que não ultrapasse max_tokens, preservando integridade de linhas.
        :param text: Texto original.
        :param max_tokens: Teto de tokens permitido.
        :return: Texto truncado acompanhado de marcador explicativo.
        """
        if max_tokens <= 0:
            return ""

        current_tokens = self.count(text)
        if current_tokens <= max_tokens:
            return text

        lines = text.splitlines(keepends=True)
        accumulated: list[str] = []
        accumulated_tokens = 0
        marker = "\n[... CONTEÚDO TRUNCADO PELO CONTEXT MANAGER DEVIDO AO LIMITE DE TOKENS ...]\n"
        marker_tokens = self.count(marker)
        effective_max = max(1, max_tokens - marker_tokens)

        for line in lines:
            line_tokens = self.count(line)
            if accumulated_tokens + line_tokens > effective_max:
                break
            accumulated.append(line)
            accumulated_tokens += line_tokens

        return "".join(accumulated).rstrip() + marker
