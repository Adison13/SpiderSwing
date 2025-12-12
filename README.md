# 🕷️ SpiderSwing

SpiderSwing é um jogo 2D desenvolvido em **Python com Pygame**, inspirado em jogos de desvio de obstáculos como *Flappy Bird*.  
O jogador controla uma aranha que deve desviar dos obstáculos e alcançar a maior pontuação possível.

---

## 🎯 Objetivo do Jogo
- Controlar a aranha
- Desviar dos obstáculos da caverna
- Acumular pontos
- Salvar o nome e a pontuação no ranking ao perder

---

## 🎮 Controles
- **ESPAÇO** → Pular / mover a aranha
- **Mouse** → Navegar pelos botões do menu
- **ENTER** → Salvar nome no ranking
- **BACKSPACE** → Apagar letras no nome
- **ESC** → Voltar ao menu (na tela de ranking)

---

## 🧱 Estrutura do Projeto
O projeto foi organizado utilizando **Programação Orientada a Objetos (POO)** e separação de responsabilidades:

SpiderSwing/
│
├── assets/ → Imagens do jogo (menu, player, obstáculos, fundo)
│
├── entities/ → Entidades do jogo
│ ├── spider.py → Lógica da aranha (player)
│ └── obstacle.py → Lógica dos obstáculos
│
├── ui/ → Telas do jogo
│ └── screens.py → Menu, Game Over e Ranking
│
├── structures/ → Estruturas de dados
│ └── avl.py → Árvore AVL usada no ranking
│
├── data/ → Armazenamento de dados
│ ├── scores.json → Ranking salvo localmente
│ └── storage.py → Manipulação dos dados
│
├── main.py → Arquivo principal do jogo
├── requirements.txt → Dependências do projeto
└── README.md → Documentação

yaml
Copiar código

---

## 🧠 Conceitos Utilizados
- Programação Orientada a Objetos (POO)
- Estrutura de dados (Árvore AVL)
- Manipulação de arquivos JSON
- Loop de jogo com Pygame
- Interface gráfica em pixel art

---

## ⚙️ Requisitos
- Python **3.10 ou superior**
- Biblioteca **Pygame**

---

## ▶️ Como Executar o Jogo

### 1️⃣ Clonar o repositório
```bash
git clone https://github.com/Adison13/SpiderSwing.git
cd SpiderSwing
2️⃣ Criar e ativar o ambiente virtual
bash
Copiar código
python -m venv .venv
.\.venv\Scripts\Activate.ps1
Se o PowerShell bloquear:

powershell
Copiar código
Set-ExecutionPolicy -Scope CurrentUser RemoteSigned
3️⃣ Instalar dependências
bash
Copiar código
pip install -r requirements.txt
4️⃣ Executar o jogo
bash
Copiar código
python main.py
💾 Ranking
As pontuações são salvas automaticamente no arquivo:

bash
Copiar código
data/scores.json
O ranking exibe os Top 10 jogadores, ordenados pela maior pontuação.

👨‍💻 Autores
Adison de Oliveira, Matteo Souza, Matheus Borges
Curso: Análise e Desenvolvimento de Sistemas
Projeto acadêmico desenvolvido em Python.