import pygame
from typing import List, Dict
from structures.avl import ScoreRecord


def desenhar_texto_central(tela, fonte, texto, y, cor=(240, 240, 240)):
    surf = fonte.render(texto, True, cor)
    x = (tela.get_width() - surf.get_width()) // 2
    tela.blit(surf, (x, y))


def _scale_rect(base_rect: pygame.Rect, base_size, target_size) -> pygame.Rect:
    base_w, base_h = base_size
    target_w, target_h = target_size
    sx = target_w / base_w
    sy = target_h / base_h
    return pygame.Rect(
        int(base_rect.x * sx),
        int(base_rect.y * sy),
        int(base_rect.width * sx),
        int(base_rect.height * sy),
    )


def tela_menu(tela: pygame.Surface, menu_bg: pygame.Surface, mouse_pos) -> Dict[str, pygame.Rect]:
    tela.blit(menu_bg, (0, 0))

    BASE_W, BASE_H = 1024, 1536

    play_base = pygame.Rect(259, 816, 506, 127)
    rank_base = pygame.Rect(259, 1011, 506, 117)
    quit_base = pygame.Rect(259, 1206, 506, 117)

    btn_play = _scale_rect(play_base, (BASE_W, BASE_H), (tela.get_width(), tela.get_height()))
    btn_rank = _scale_rect(rank_base, (BASE_W, BASE_H), (tela.get_width(), tela.get_height()))
    btn_quit = _scale_rect(quit_base, (BASE_W, BASE_H), (tela.get_width(), tela.get_height()))

    if btn_play.collidepoint(mouse_pos):
        pygame.draw.rect(tela, (255, 255, 255), btn_play, 2, border_radius=12)
    if btn_rank.collidepoint(mouse_pos):
        pygame.draw.rect(tela, (255, 255, 255), btn_rank, 2, border_radius=12)
    if btn_quit.collidepoint(mouse_pos):
        pygame.draw.rect(tela, (255, 255, 255), btn_quit, 2, border_radius=12)

    return {"PLAY": btn_play, "RANKING": btn_rank, "QUIT": btn_quit}


def tela_gameover(
    tela: pygame.Surface,
    gameover_bg: pygame.Surface,
    fonte_score,
    fonte_nome,
    score: int,
    nome_player: str,
    mouse_pos
) -> Dict[str, pygame.Rect]:
    tela.blit(gameover_bg, (0, 0))

    BASE_W, BASE_H = 1024, 1536

    score_val_base = pygame.Rect(620, 569, 158, 76)
    name_box_base  = pygame.Rect(201, 744, 613, 113)

    retry_base = pygame.Rect(204, 1028, 616, 107)
    menu_base  = pygame.Rect(204, 1160, 616, 118)
    rank_base  = pygame.Rect(203, 1303, 617, 117)

    score_rect = _scale_rect(score_val_base, (BASE_W, BASE_H), (tela.get_width(), tela.get_height()))
    name_rect  = _scale_rect(name_box_base,  (BASE_W, BASE_H), (tela.get_width(), tela.get_height()))
    btn_retry  = _scale_rect(retry_base,     (BASE_W, BASE_H), (tela.get_width(), tela.get_height()))
    btn_menu   = _scale_rect(menu_base,      (BASE_W, BASE_H), (tela.get_width(), tela.get_height()))
    btn_rank   = _scale_rect(rank_base,      (BASE_W, BASE_H), (tela.get_width(), tela.get_height()))

    # limpa placeholders
    COR_FUNDO_CARD = (10, 10, 25)

    limpar_score = score_rect.inflate(60, 10)
    limpar_score.y += 6
    limpar_score.height -= 8

    limpar_nome = name_rect.inflate(-10, -10)

    pygame.draw.rect(tela, COR_FUNDO_CARD, limpar_score)
    pygame.draw.rect(tela, COR_FUNDO_CARD, limpar_nome)

    prev_clip = tela.get_clip()

    tela.set_clip(limpar_score)
    score_surf = fonte_score.render(str(score), True, (255, 255, 255))
    tela.blit(score_surf, (score_rect.centerx - score_surf.get_width() // 2,
                           score_rect.centery - score_surf.get_height() // 2))

    tela.set_clip(limpar_nome)
    nome_surf = fonte_nome.render(nome_player, True, (255, 255, 255))
    tela.blit(nome_surf, (name_rect.centerx - nome_surf.get_width() // 2,
                          name_rect.centery - nome_surf.get_height() // 2))

    tela.set_clip(prev_clip)

    for rect in (btn_retry, btn_menu, btn_rank):
        if rect.collidepoint(mouse_pos):
            pygame.draw.rect(tela, (255, 255, 255), rect, 2, border_radius=12)

    return {"RETRY": btn_retry, "MENU": btn_menu, "RANKING": btn_rank, "NAME_BOX": name_rect}


def tela_ranking(
    tela: pygame.Surface,
    ranking_bg: pygame.Surface,
    fonte_itens,
    top: List[ScoreRecord]
):
    """
    Ranking com imagem de fundo (pixel) e texto real por cima.
    """
    tela.blit(ranking_bg, (0, 0))

    # Área “grande” interna (onde vão os 10 itens) — base 1024x1536
    # (retângulo do painel grande na sua arte)
    BASE_W, BASE_H = 1024, 1536
    lista_base = pygame.Rect(120, 520, 784, 860)
    lista_rect = _scale_rect(lista_base, (BASE_W, BASE_H), (tela.get_width(), tela.get_height()))

    # Desenhar TOP 10 dentro do painel
    x = lista_rect.x + int(lista_rect.width * 0.10)
    y = lista_rect.y + int(lista_rect.height * 0.12)
    linha_h = int(lista_rect.height * 0.075)

    if not top:
        surf = fonte_itens.render("Sem scores ainda.", True, (240, 240, 240))
        tela.blit(surf, (lista_rect.centerx - surf.get_width() // 2, y))
        return

    for i, r in enumerate(top[:10], start=1):
        texto = f"{i:02d}. {r.name}  -  {r.score}"
        surf = fonte_itens.render(texto, True, (245, 245, 245))
        tela.blit(surf, (x, y))
        y += linha_h


