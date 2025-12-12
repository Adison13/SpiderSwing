# 🕷️ SpiderSwing

SpiderSwing é um jogo 2D desenvolvido em **Python com Pygame**, inspirado em mecânicas simples de sobrevivência e reflexo.
O jogador controla uma aranha que deve se movimentar e desviar de obstáculos em um cenário de caverna, acumulando pontuação.
Ao final da partida, o jogador pode salvar seu nome no **ranking Top 10**.

Projeto desenvolvido para fins **acadêmicos**, aplicando conceitos de:
- Estrutura de dados
- Organização de código
- Persistência de dados
- Interface gráfica com Pygame

---

## 🎮 Funcionalidades

- Menu inicial interativo (Play, Ranking, Quit)
- Jogabilidade com pontuação em tempo real
- Tela de Game Over com inserção de nome
- Ranking Top 10 persistente (salvo em arquivo JSON)
- Cenário em pixel art
- Sprites personalizados
- Estrutura modular do projeto

---

## 🗂️ Estrutura do Projeto

```text
SpiderSwing/
│
├── assets/
│   └── images/
│       ├── cave_far.png
│       ├── cave_near.png
│       ├── menu.png
│       ├── gameover.png
│       ├── ranking.png
│       ├── spider_player.png
│       └── obstacles/
│           ├── rock_tile.png
│           ├── stalactite_cap.png
│           └── stalagmite_cap.png
│
├── data/
│   ├── scores.json
│   └── storage.py
│
├── entities/
│   ├── spider.py
│   └── obstacle.py
│
├── structures/
│   └── avl.py
│
├── ui/
│   └── screens.py
│
├── main.py
├── .gitignore
└── README.md
▶️ Como Executar o Jogo
1️⃣ Clonar o repositório
bash
Copiar código
git clone https://github.com/Adison13/SpiderSwing.git
cd SpiderSwing
2️⃣ Criar e ativar o ambiente virtual
bash
Copiar código
python -m venv .venv
Ativar no Windows (PowerShell):

powershell
Copiar código
.\.venv\Scripts\Activate.ps1
Se o PowerShell bloquear a ativação:

powershell
Copiar código
Set-ExecutionPolicy -Scope CurrentUser RemoteSigned
3️⃣ Instalar dependências
bash
Copiar código
pip install pygame
Obs: o projeto utiliza apenas Pygame.

4️⃣ Executar o jogo
bash
Copiar código
python main.py
🏆 Ranking
O ranking salva automaticamente os Top 10 jogadores

As pontuações são armazenadas no arquivo:

text
Copiar código
data/scores.json
O ranking é ordenado da maior para a menor pontuação

👨‍💻 Autores
Adison de Oliveira

Matteo Souza

Matheus Borges

Curso: Análise e Desenvolvimento de Sistemas
Projeto acadêmico desenvolvido em Python.

📚 Tecnologias Utilizadas
Python 3.x

Pygame

Git & GitHub


