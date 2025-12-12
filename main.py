import sys
import os
import pygame

from entities.spider import Spider
from entities.obstacle import ObstaclePair

from structures.avl import AVLRanking, ScoreRecord
from ui.screens import tela_menu, tela_gameover, tela_ranking

from data.storage import carregar_scores, salvar_scores

LARGURA, ALTURA = 480, 640
FPS = 60
LIMITE_RANKING = 50


def carregar_imagem(path: str, largura: int, altura: int) -> pygame.Surface:
    img = pygame.image.load(path).convert()
    # Pixel art: usar scale (sem smooth)
    return pygame.transform.scale(img, (largura, altura))


def desenhar_parallax(tela: pygame.Surface,
                      layer_far: pygame.Surface, x_far: float,
                      layer_near: pygame.Surface, x_near: float):
    """
    Desenha 2 camadas em loop horizontal (tile), preenchendo a tela toda.
    """
    w = tela.get_width()

    # FAR
    x = x_far
    while x > 0:
        x -= w
    while x < w:
        tela.blit(layer_far, (x, 0))
        x += w

    # NEAR
    x = x_near
    while x > 0:
        x -= w
    while x < w:
        tela.blit(layer_near, (x, 0))
        x += w


def main():
    pygame.init()
    tela = pygame.display.set_mode((LARGURA, ALTURA))
    pygame.display.set_caption("SpiderSwing")
    relogio = pygame.time.Clock()

    fonte_score = pygame.font.SysFont(None, 48)
    fonte_nome = pygame.font.SysFont(None, 56)
    fonte_itens = pygame.font.SysFont(None, 30)

    BASE_DIR = os.path.dirname(os.path.abspath(__file__))

    # ----- MENU BG -----
    CAMINHO_MENU = os.path.join(BASE_DIR, "assets", "images", "menu.png")
    if not os.path.exists(CAMINHO_MENU):
        print("ERRO: Não encontrei a imagem do menu em:", CAMINHO_MENU)
        pygame.quit()
        return
    menu_bg = pygame.transform.scale(pygame.image.load(CAMINHO_MENU).convert(), (LARGURA, ALTURA))

    # ----- GAME OVER BG -----
    CAMINHO_GAMEOVER = os.path.join(BASE_DIR, "assets", "images", "gameover.png")
    if not os.path.exists(CAMINHO_GAMEOVER):
        print("ERRO: Não encontrei a imagem do game over em:", CAMINHO_GAMEOVER)
        print("Coloque como: assets/images/gameover.png")
        pygame.quit()
        return
    gameover_bg = pygame.transform.scale(pygame.image.load(CAMINHO_GAMEOVER).convert(), (LARGURA, ALTURA))

    # ----- RANKING BG -----
    CAMINHO_RANKING = os.path.join(BASE_DIR, "assets", "images", "ranking.png")
    if not os.path.exists(CAMINHO_RANKING):
        print("ERRO: Não encontrei a imagem do ranking em:", CAMINHO_RANKING)
        print("Coloque como: assets/images/ranking.png")
        pygame.quit()
        return
    ranking_bg = pygame.transform.scale(pygame.image.load(CAMINHO_RANKING).convert(), (LARGURA, ALTURA))

    # ----- PARALLAX (CAVERNA) -----
    CAMINHO_CAVE_FAR = os.path.join(BASE_DIR, "assets", "images", "cave_far.png")
    CAMINHO_CAVE_NEAR = os.path.join(BASE_DIR, "assets", "images", "cave_near.png")

    if not os.path.exists(CAMINHO_CAVE_FAR) or not os.path.exists(CAMINHO_CAVE_NEAR):
        print("ERRO: Não encontrei as camadas do fundo parallax:")
        print(" -", CAMINHO_CAVE_FAR)
        print(" -", CAMINHO_CAVE_NEAR)
        print("Coloque como: assets/images/cave_far.png e assets/images/cave_near.png")
        pygame.quit()
        return

    cave_far = carregar_imagem(CAMINHO_CAVE_FAR, LARGURA, ALTURA)
    cave_near = carregar_imagem(CAMINHO_CAVE_NEAR, LARGURA, ALTURA)

    # offsets do parallax
    x_far = 0.0
    x_near = 0.0
    # velocidades (px por segundo)
    vel_far = 18.0
    vel_near = 42.0

    # ----- Ranking (AVL) -----
    ranking = AVLRanking()
    carregados = carregar_scores()
    uid_counter = 1
    for item in carregados:
        try:
            s = int(item.get("score", 0))
            n = str(item.get("name", "Player"))
            u = int(item.get("uid", uid_counter))
            uid_counter = max(uid_counter, u + 1)
            ranking.insert(ScoreRecord(score=s, name=n, uid=u))
        except Exception:
            pass

    modo = "MENU"  # MENU, JOGO, RANKING, GAMEOVER
    nome_player = ""
    max_nome = 10

    def persistir_ranking():
        top = ranking.top_n(LIMITE_RANKING)
        lista = [{"score": r.score, "name": r.name, "uid": r.uid} for r in top]
        salvar_scores(lista)

    def resetar_partida():
        nonlocal spider, obstaculos, tempo_spawn, score, game_over, score_registrado, nome_player
        spider = Spider(120, ALTURA // 2)
        spider.configurar_limites(ALTURA, margem_chao=30)
        obstaculos = []
        tempo_spawn = 0
        score = 0
        game_over = False
        score_registrado = False
        nome_player = ""

    spider = Spider(120, ALTURA // 2)
    spider.configurar_limites(ALTURA, margem_chao=30)

    obstaculos = []
    tempo_spawn = 0
    intervalo_spawn = 1500

    score = 0
    game_over = False
    score_registrado = False

    rodando = True
    while rodando:
        delta_ms = relogio.tick(FPS)
        dt = delta_ms / 1000.0  # segundos
        mouse_pos = pygame.mouse.get_pos()

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                rodando = False

            if evento.type == pygame.KEYDOWN:
                # GAMEOVER: digitar nome
                if modo == "GAMEOVER":
                    if evento.key == pygame.K_RETURN:
                        if nome_player.strip():
                            u = uid_counter
                            uid_counter += 1
                            ranking.insert(ScoreRecord(score=score, name=nome_player.strip(), uid=u))

                            while ranking.size() > LIMITE_RANKING:
                                mk = ranking.min_key()
                                if mk is None:
                                    break
                                ranking.remove(mk)

                            persistir_ranking()
                            score_registrado = True
                            modo = "RANKING"

                    elif evento.key == pygame.K_BACKSPACE:
                        nome_player = nome_player[:-1]

                    elif evento.key == pygame.K_ESCAPE:
                        modo = "MENU"

                    else:
                        ch = evento.unicode
                        if ch and ch.isprintable() and len(nome_player) < max_nome:
                            if ch not in ["\r", "\n", "\t"]:
                                nome_player += ch
                    continue

                if evento.key == pygame.K_ESCAPE:
                    if modo in ("RANKING", "JOGO"):
                        modo = "MENU"
                    else:
                        rodando = False

                if evento.key == pygame.K_t:
                    modo = "RANKING"

                if modo == "JOGO":
                    if evento.key == pygame.K_SPACE and not game_over:
                        spider.pular()
                    if evento.key == pygame.K_r:
                        resetar_partida()

            if evento.type == pygame.MOUSEBUTTONDOWN:
                if modo == "MENU":
                    rects = tela_menu(tela, menu_bg, mouse_pos)
                    if rects["PLAY"].collidepoint(mouse_pos):
                        resetar_partida()
                        modo = "JOGO"
                    elif rects["RANKING"].collidepoint(mouse_pos):
                        modo = "RANKING"
                    elif rects["QUIT"].collidepoint(mouse_pos):
                        rodando = False

                elif modo == "JOGO" and not game_over:
                    spider.pular()

                elif modo == "GAMEOVER":
                    rects = tela_gameover(tela, gameover_bg, fonte_score, fonte_nome, score, nome_player, mouse_pos)
                    if rects["RETRY"].collidepoint(mouse_pos):
                        resetar_partida()
                        modo = "JOGO"
                    elif rects["MENU"].collidepoint(mouse_pos):
                        modo = "MENU"
                    elif rects["RANKING"].collidepoint(mouse_pos):
                        modo = "RANKING"

        # MENU
        if modo == "MENU":
            tela_menu(tela, menu_bg, mouse_pos)
            pygame.display.flip()
            continue

        # RANKING
        if modo == "RANKING":
            top10 = ranking.top_n(10)
            tela_ranking(tela, ranking_bg, fonte_itens, top10)
            pygame.display.flip()
            continue

        # GAMEOVER
        if modo == "GAMEOVER":
            tela_gameover(tela, gameover_bg, fonte_score, fonte_nome, score, nome_player, mouse_pos)
            pygame.display.flip()
            continue

        # ====== JOGO ======
        # Atualiza parallax APENAS no jogo (para dar sensação de movimento)
        x_far -= vel_far * dt
        x_near -= vel_near * dt

        if not game_over:
            tempo_spawn += delta_ms

            if tempo_spawn >= intervalo_spawn:
                tempo_spawn = 0
                obstaculos.append(
                    ObstaclePair(
                        x=LARGURA,
                        largura=60,
                        altura_tela=ALTURA - 30,
                        gap=160
                    )
                )

            spider.atualizar()

            for obs in obstaculos:
                obs.atualizar()

                if obs.colide_com(spider.rect):
                    game_over = True

                if not obs.passou and obs.rect_topo.right < spider.rect.left:
                    obs.passou = True
                    score += 1

            obstaculos = [o for o in obstaculos if not o.fora_da_tela()]

        if game_over and not score_registrado:
            modo = "GAMEOVER"

        # ====== DESENHO ======
        desenhar_parallax(tela, cave_far, x_far, cave_near, x_near)

        for obs in obstaculos:
            obs.desenhar(tela)

        spider.desenhar(tela)

        pygame.draw.line(tela, (60, 60, 80), (0, ALTURA - 30), (LARGURA, ALTURA - 30), 4)

        txt = pygame.font.SysFont(None, 36).render(f"Score: {score}", True, (240, 240, 240))
        tela.blit(txt, (10, 10))

        pygame.display.flip()

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()





