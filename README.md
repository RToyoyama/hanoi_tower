# 🗼 Torre de Hanói

Implementação do problema clássico da **Torre de Hanói** em Python, com foco em boas práticas de engenharia de software: orientação a objetos, separação de responsabilidades, configuração externalizada e interface de linha de comando.

---

## 📐 Arquitetura

```
torre_hanoi/
 ┣ 📂config/
 ┃  ┣ 📜config.py          # Lê o YAML e expõe dataclasses tipadas (singleton CONFIG)
 ┃  ┗ 📜config.yml         # Única fonte de verdade — sem valores hardcoded no código
 ┣ 📂src/
 ┃  ┗ 📂torre_hanoi/
 ┃     ┣ 📜disco.py         # Classe Disco — encapsulamento + dunder methods
 ┃     ┣ 📜torre.py         # Classe Torre — pilha com regras de domínio
 ┃     ┣ 📜jogo.py          # Classe Jogo — orquestra a recursão e o estado
 ┃     ┣ 📜visualizador.py  # Classe Visualizador — renderização no terminal (SRP)
 ┃     ┣ 📜cli.py           # Interface CLI com argparse
 ┃     ┗ 📜__init__.py      # API pública do pacote
 ┣ 📜main.py                # Entrypoint
 ┗ 📜pyproject.toml         # Configuração uv / hatchling
```

### Diagrama de dependências

```
main.py
  └── cli.py
        ├── config/config.py  ←─── config/config.yml
        └── jogo.py
              ├── disco.py
              ├── torre.py
              └── visualizador.py
                    └── config/config.py
```

---

## ⚙️ Pré-requisitos

| Ferramenta | Versão mínima |
|---|---|
| Python | 3.11 |
| uv | qualquer |

---

## 🚀 Instalação

```bash
# Clone o repositório
git clone https://github.com/seu-usuario/torre_hanoi.git
cd torre_hanoi

# Instala dependências (PyYAML) e cria o virtualenv
uv sync
```

---

## ▶️ Como usar

```bash
# Resolve com o número de discos padrão (definido em config/config.yml)
uv run main.py

# Resolve com N discos
uv run main.py 5

# Exibe o estado das torres após cada movimento
uv run main.py 5 --passo-a-passo
uv run main.py 5 -p

# Adiciona pausa entre os passos (útil para acompanhar visualmente)
uv run main.py 4 --passo-a-passo --delay 0.3

# Desativa cores ANSI (para terminais que não suportam)
uv run main.py 6 --sem-cor

# Exibe apenas a lista de movimentos, sem o desenho
uv run main.py 3 --so-movimentos

# Ajuda completa
uv run main.py --help
```

### Exemplo de saída

```
══════════════════════════════════════════════════
  🗼  TORRE DE HANÓI  —  3 disco(s)
  Movimentos necessários: 7
══════════════════════════════════════════════════

📐 Estado inicial:

   [─]          |          |
  [───]         |          |
 [─────]        |          |
────────────────────────────
    A            B          C

✅  Estado final:

    |            |         [─]
    |            |        [───]
    |            |       [─────]
────────────────────────────
    A            B          C

  Total de movimentos : 7
  Tempo de cálculo    : 0.0001s
  ════════════════════════════════════════
```

---

## 🔧 Configuração

Toda a configuração fica em **`config/config.yml`**. Nenhum valor está hardcoded no código.

```yaml
jogo:
  discos_padrao: 3      # discos usados quando nenhum argumento é passado
  discos_maximo: 25     # limite máximo aceito pela CLI
  torre_origem:  "A"
  torre_destino: "C"
  torre_auxiliar: "B"

cli:
  passo_a_passo:  false
  delay_segundos: 0.0
  colorido:       true
  so_movimentos:  false

visual:
  char_disco:    "─"
  char_poste:    "|"
  cores_discos:  ["91m", "93m", "92m", "96m", "94m", "95m", "97m"]

log:
  mostrar_cabecalho:      true
  mostrar_estado_inicial: true
  mostrar_estado_final:   true
  mostrar_estatisticas:   true
  precisao_tempo:         4
```

**Prioridade de configuração:**
```
argumento CLI  >  config.yml  >  código
```

---

## 🧠 O algoritmo

A Torre de Hanói é resolvida com **recursão** usando a estratégia dividir para conquistar:

```
Para mover N discos de ORIGEM → DESTINO usando AUXILIAR:

  1. Mova N-1 discos:  ORIGEM  → AUXILIAR   (recursão)
  2. Mova disco N:     ORIGEM  → DESTINO    (caso base)
  3. Mova N-1 discos:  AUXILIAR → DESTINO  (recursão)
```

O número mínimo de movimentos é sempre **2ⁿ − 1**:

| Discos | Movimentos |
|--------|-----------|
| 1 | 1 |
| 3 | 7 |
| 5 | 31 |
| 10 | 1.023 |
| 20 | 1.048.575 |
| 64 | ~1,8 × 10¹⁹ 😱 |

---

## 🏗️ Conceitos OOP aplicados

| Classe | Princípio / Padrão |
|---|---|
| `Disco` | Encapsulamento, dunder methods (`__eq__`, `__lt__`, `__str__`, `__repr__`) |
| `Torre` | Composição, exceções de domínio (`TorreVaziaError`, `MovimentoInvalidoError`), protocolo container (`__len__`, `__iter__`) |
| `Jogo` | Orquestração, `@dataclass`, `@property`, método privado `_resolver()` |
| `Visualizador` | Single Responsibility Principle — só renderiza, nunca decide |
| `ConfigJogo` | `@dataclass(frozen=True)` — imutável por design |
| `config.py` | Singleton via módulo, fail-fast, `yaml.safe_load` |

---

## 📦 Dependências

| Pacote | Uso |
|---|---|
| `PyYAML` | Leitura do `config/config.yml` |

**Dev:**

| Pacote | Uso |
|---|---|
| `pytest` | Testes unitários |
| `ruff` | Linter e formatter |

---

## 🤝 Contribuindo

```bash
# Instala dependências de dev
uv sync

# Roda o linter
uv run ruff check src/

# Formata o código
uv run ruff format src/

# Roda os testes
uv run pytest
```

---

## 📄 Licença

MIT