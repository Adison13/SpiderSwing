from __future__ import annotations
from dataclasses import dataclass
from typing import Optional, List, Tuple


@dataclass(frozen=True)
class ScoreRecord:
    score: int
    name: str
    uid: int  # desempate (ordem de inserção)


class _NoAVL:
    def __init__(self, key: Tuple[int, int], value: ScoreRecord):
        self.key = key  # (score, uid)
        self.value = value
        self.left: Optional[_NoAVL] = None
        self.right: Optional[_NoAVL] = None
        self.height: int = 1


class AVLRanking:
    """
    AVL para Ranking:
    - chave = (score, uid) para manter tudo único
    - suporta inserir, remover, buscar mínimo/máximo, e obter Top N (maiores scores)
    """

    def __init__(self):
        self._root: Optional[_NoAVL] = None
        self._size: int = 0

    # -------- utilitários --------
    def size(self) -> int:
        return self._size

    def _h(self, n: Optional[_NoAVL]) -> int:
        return n.height if n else 0

    def _update_h(self, n: _NoAVL):
        n.height = 1 + max(self._h(n.left), self._h(n.right))

    def _bf(self, n: _NoAVL) -> int:
        return self._h(n.left) - self._h(n.right)

    def _rot_right(self, y: _NoAVL) -> _NoAVL:
        x = y.left
        t2 = x.right  # type: ignore

        x.right = y  # type: ignore
        y.left = t2

        self._update_h(y)
        self._update_h(x)  # type: ignore
        return x  # type: ignore

    def _rot_left(self, x: _NoAVL) -> _NoAVL:
        y = x.right
        t2 = y.left  # type: ignore

        y.left = x  # type: ignore
        x.right = t2

        self._update_h(x)
        self._update_h(y)  # type: ignore
        return y  # type: ignore

    def _balance(self, n: _NoAVL) -> _NoAVL:
        self._update_h(n)
        bf = self._bf(n)

        # Esquerda pesada
        if bf > 1:
            if self._bf(n.left) < 0:  # type: ignore
                n.left = self._rot_left(n.left)  # type: ignore
            return self._rot_right(n)

        # Direita pesada
        if bf < -1:
            if self._bf(n.right) > 0:  # type: ignore
                n.right = self._rot_right(n.right)  # type: ignore
            return self._rot_left(n)

        return n

    # -------- inserir --------
    def insert(self, record: ScoreRecord):
        self._root = self._insert(self._root, (record.score, record.uid), record)

    def _insert(self, node: Optional[_NoAVL], key: Tuple[int, int], value: ScoreRecord) -> _NoAVL:
        if node is None:
            self._size += 1
            return _NoAVL(key, value)

        if key < node.key:
            node.left = self._insert(node.left, key, value)
        elif key > node.key:
            node.right = self._insert(node.right, key, value)
        else:
            # chave repetida (não deve acontecer por causa do uid), mas ignoramos
            return node

        return self._balance(node)

    # -------- remover --------
    def remove(self, key: Tuple[int, int]):
        self._root = self._remove(self._root, key)

    def _remove(self, node: Optional[_NoAVL], key: Tuple[int, int]) -> Optional[_NoAVL]:
        if node is None:
            return None

        if key < node.key:
            node.left = self._remove(node.left, key)
        elif key > node.key:
            node.right = self._remove(node.right, key)
        else:
            # achou o nó
            self._size -= 1

            # 0 ou 1 filho
            if node.left is None:
                return node.right
            if node.right is None:
                return node.left

            # 2 filhos: pega sucessor (menor da direita)
            succ = self._min_node(node.right)
            node.key = succ.key
            node.value = succ.value
            # remove o sucessor na subárvore direita (sem decrementar size novamente)
            self._size += 1
            node.right = self._remove(node.right, succ.key)

        if node is None:
            return None

        return self._balance(node)

    # -------- buscas --------
    def min_key(self) -> Optional[Tuple[int, int]]:
        if self._root is None:
            return None
        return self._min_node(self._root).key

    def max_key(self) -> Optional[Tuple[int, int]]:
        if self._root is None:
            return None
        return self._max_node(self._root).key

    def _min_node(self, node: _NoAVL) -> _NoAVL:
        atual = node
        while atual.left is not None:
            atual = atual.left
        return atual

    def _max_node(self, node: _NoAVL) -> _NoAVL:
        atual = node
        while atual.right is not None:
            atual = atual.right
        return atual

    # -------- listar top N --------
    def top_n(self, n: int) -> List[ScoreRecord]:
        """
        Retorna os N maiores (score alto primeiro).
        Faz percurso reverso (direita -> raiz -> esquerda).
        """
        resultado: List[ScoreRecord] = []
        self._inorder_reverso(self._root, resultado, n)
        return resultado

    def _inorder_reverso(self, node: Optional[_NoAVL], out: List[ScoreRecord], limit: int):
        if node is None or len(out) >= limit:
            return
        self._inorder_reverso(node.right, out, limit)
        if len(out) < limit:
            out.append(node.value)
        self._inorder_reverso(node.left, out, limit)
