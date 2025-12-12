import os
import pygame


class Spider:
    def __init__(self, x: int, y: int):
        self.x = float(x)
        self.y = float(y)

        self.vy = 0.0
        self.grav = 900.0
        self.impulso = -340.0
        self.damping = 0.995

        self.altura_tela = 640
        self.margem_chao = 30

        # --- Sprite do player (pixel) ---
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))  # raiz do projeto
        sprite_path = os.path.join(base_dir, "assets", "images", "spider_player.png")

        if not os.path.exists(sprite_path):
            raise FileNotFoundError(
                "Não encontrei o sprite do player. Coloque em:\n"
                f"{sprite_path}\n"
                "=> assets/images/spider_player.png"
            )

        self.sprite = pygame.image.load(sprite_path).convert_alpha()

        # Ajuste fino do tamanho do player (se quiser maior, aumente aqui)
        # (mantém pixel-art: sem smoothscale)
        alvo_w = 64
        alvo_h = 64
        self.sprite = pygame.transform.scale(self.sprite, (alvo_w, alvo_h))

        self.w = self.sprite.get_width()
        self.h = self.sprite.get_height()

        # hitbox (um pouco menor que o sprite pra ficar justo e “justo” no gameplay)
        hit_w = int(self.w * 0.70)
        hit_h = int(self.h * 0.70)
        self.rect = pygame.Rect(int(self.x), int(self.y), hit_w, hit_h)

    def configurar_limites(self, altura_tela: int, margem_chao: int = 30):
        self.altura_tela = altura_tela
        self.margem_chao = margem_chao

    def pular(self):
        self.vy = self.impulso

    def atualizar(self, dt: float = 1 / 60):
        self.vy += self.grav * dt
        self.vy *= self.damping

        self.y += self.vy * dt

        # Limites (considerando a hitbox)
        chao = self.altura_tela - self.margem_chao - self.rect.height
        if self.y > chao:
            self.y = chao
            self.vy = 0.0

        if self.y < 0:
            self.y = 0
            self.vy = 0.0

        self.rect.x = int(self.x)
        self.rect.y = int(self.y)

    def desenhar(self, tela: pygame.Surface):
        # centraliza o sprite em relação à hitbox
        sprite_x = self.rect.centerx - self.w // 2
        sprite_y = self.rect.centery - self.h // 2
        tela.blit(self.sprite, (sprite_x, sprite_y))
