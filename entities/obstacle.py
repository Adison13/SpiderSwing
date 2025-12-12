import os
import random
import pygame


class ObstaclePair:
    _loaded = False
    _cap_top = None
    _cap_bot = None
    _tile = None

    @classmethod
    def _load_sprites(cls):
        if cls._loaded:
            return

        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))  # raiz do projeto
        path_top = os.path.join(base_dir, "assets", "images", "obstacles", "stalactite_cap.png")
        path_bot = os.path.join(base_dir, "assets", "images", "obstacles", "stalagmite_cap.png")
        path_tile = os.path.join(base_dir, "assets", "images", "obstacles", "rock_tile.png")

        if not os.path.exists(path_top) or not os.path.exists(path_bot) or not os.path.exists(path_tile):
            raise FileNotFoundError(
                "Sprites de obstáculo não encontrados. Verifique:\n"
                f"- {path_top}\n- {path_bot}\n- {path_tile}"
            )

        cls._cap_top = pygame.image.load(path_top).convert_alpha()
        cls._cap_bot = pygame.image.load(path_bot).convert_alpha()
        cls._tile = pygame.image.load(path_tile).convert_alpha()

        cls._loaded = True

    def __init__(self, x: int, largura: int, altura_tela: int, gap: int):
        self.x = x
        self.largura = largura
        self.altura_tela = altura_tela
        self.gap = gap

        min_h = 80
        max_h = max(min_h + 20, altura_tela - gap - 80)
        self.altura_topo = random.randint(min_h, max_h)
        self.altura_baixo = altura_tela - self.altura_topo - gap

        self.rect_topo = pygame.Rect(self.x, 0, self.largura, self.altura_topo)
        self.rect_baixo = pygame.Rect(self.x, self.altura_topo + self.gap, self.largura, self.altura_baixo)

        self.vel = 3
        self.passou = False

    def atualizar(self):
        self.x -= self.vel
        self.rect_topo.x = self.x
        self.rect_baixo.x = self.x

    def fora_da_tela(self) -> bool:
        return self.rect_topo.right < 0

    def colide_com(self, rect_player: pygame.Rect) -> bool:
        return self.rect_topo.colliderect(rect_player) or self.rect_baixo.colliderect(rect_player)

    def _blit_tile_vertical_clip(self, tela: pygame.Surface, tile: pygame.Surface, rect: pygame.Rect):
        """
        Preenche rect com tile repetindo verticalmente, SEM VAZAR (usa clip).
        """
        if rect.width <= 0 or rect.height <= 0:
            return

        prev_clip = tela.get_clip()
        tela.set_clip(rect)

        # Ajusta tile para a largura do obstáculo
        tile_scaled = pygame.transform.scale(tile, (rect.width, tile.get_height()))
        y = rect.y

        # desenha em loop; o CLIP garante que não invade o gap
        while y < rect.bottom:
            tela.blit(tile_scaled, (rect.x, y))
            y += tile_scaled.get_height()

        tela.set_clip(prev_clip)

    def _blit_cap_clip(self, tela: pygame.Surface, cap: pygame.Surface, rect: pygame.Rect, is_top: bool):
        """
        Desenha o 'cap' respeitando o limite do rect (usa clip).
        is_top=True => cap fica no fim do rect_topo (embaixo)
        is_top=False => cap fica no começo do rect_baixo (em cima)
        """
        if rect.width <= 0 or rect.height <= 0:
            return

        prev_clip = tela.get_clip()
        tela.set_clip(rect)

        cap_h = min(rect.height, cap.get_height())
        cap_scaled = pygame.transform.scale(cap, (rect.width, cap_h))

        if is_top:
            tela.blit(cap_scaled, (rect.x, rect.bottom - cap_h))
        else:
            tela.blit(cap_scaled, (rect.x, rect.y))

        tela.set_clip(prev_clip)

    def desenhar(self, tela: pygame.Surface):
        self._load_sprites()

        # TOP (estalactite)
        self._blit_tile_vertical_clip(tela, self._tile, self.rect_topo)
        self._blit_cap_clip(tela, self._cap_top, self.rect_topo, is_top=True)

        # BOTTOM (estalagmite)
        self._blit_tile_vertical_clip(tela, self._tile, self.rect_baixo)
        self._blit_cap_clip(tela, self._cap_bot, self.rect_baixo, is_top=False)
