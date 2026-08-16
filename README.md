# 🧩 Tetris no Terminal (Python)

Uma implementação em **Python** do clássico jogo **Tetris**, projetada para ser executada diretamente no terminal de linha de comando.

---

## 📋 Índice

- [Características](#-características)
- [Pré-requisitos](#-pré-requisitos)
- [Como Executar](#-como-executar)
- [Como Jogar](#-como-jogar)
- [Arquitetura e Código](#-arquitetura-e-código)
- [Peças Disponíveis (Tetrominós)](#-peças-disponíveis-tetrominós)

---

## ✨ Características

- **Visualização em caracteres Unicode (`⣿⣿`)** no próprio terminal.
- **Entrada Assíncrona:** Movimentação e rotação em tempo real utilizando *threads* e *asyncio*, sem pausar a queda das peças.
- **Detecção de Colisão:** Limitações de bordas e peças empilhadas no tabuleiro.
- **Limpeza de Linhas:** Remoção automática de linhas completas com deslocamento dos blocos superiores.

---

## 🛑 Pré-requisitos

- **Python 3.10** ou superior (utiliza suporte nativo a `match / case`).
- **Sistema Operacional:** Linux ou macOS (utiliza o comando de sistema `clear` para atualização de tela).

---

## 🚀 Como Executar

1. Clone este repositório ou baixe os arquivos da aplicação.
2. Abra o terminal no diretório onde o arquivo `main.py` está localizado.
3. Execute o script com o comando:

```bash
python3 main.py
```

---

## 🎮 Como Jogar

Digite o comando desejado no terminal e pressione **`Enter`**:

| Tecla | Ação |
| :---: | :--- |
| **`A`** + `Enter` | Move a peça atual para a **esquerda** |
| **`D`** + `Enter` | Move a peça atual para a **direita** |
| **`W`** + `Enter` | **Rotaciona** a peça em 90° no sentido horário |

---

## 📐 Peças Disponíveis (Tetrominós)

O jogo conta com 6 formatos principais definidos na numeração `Schemas`:

- **L**: Tetrominó em forma de L
- **T**: Tetrominó em forma de T
- **N / NR**: Tetrominós no formato Z / S
- **Q**: Bloco Quadrado ($2 	imes 2$)
- **I**: Peça Reta ($1 	imes 4$)

---

## 🛠️ Arquitetura do Projeto

- **`Block`**: Representa um ponto coordenado $(x, y)$ na grade.
- **`Schemas`**: Contém o padrão inicial das coordenadas de cada tipo de peça.
- **`Piece`**: Controla o deslocamento, clonagem preventiva de colisão e cálculo matricial da rotação da peça ativa.
- **`Board`**:
  - Controla o tabuleiro de tamanho $10 	imes 20$.
  - Gerencia o loop de queda (`fall`) e checagem de colisão (`collide`).
  - Renderiza o tabuleiro no console (`draw`).
  - Processa a verificação e limpeza de linhas cheias (`verify`).
