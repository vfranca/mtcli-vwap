# mtcli-vwap

Plugin **VWAP (Volume Weighted Average Price)** para o ecossistema **mtcli**, desenvolvido para análise intraday, automação e integração entre plugins.

Compatível com **MetaTrader 5**, com foco em **VWAP ancorada**, **bandas estatísticas** e **saída acessível em terminal**.

---

## Principais recursos

- VWAP intraday tradicional
- VWAP ancorada por:
  - abertura do dia
  - ajuste
  - horário específico
  - máxima do período
  - mínima do período
- Bandas de VWAP configuráveis
  - desvio padrão
  - desvio ponderado por volume
- Saída textual acessível (NVDA / JAWS)
- Saída em **JSON estruturado** para automação
- Arquitetura clara em MVC

---

## Instalação

```bash
pip install mtcli-vwap
```

### Requisitos

- Python >= 3.10
- MetaTrader 5 instalado
- mtcli configurado corretamente

---

## Uso rápido

```bash
mt vwp
```

Exemplo completo:

```bash
mt vwp \
  --symbol WIN$N \
  --minutes 1 \
  --limit 600 \
  --anchor abertura \
  --bands 2
```

---

## ⚓ VWAP ancorada

### Abertura do dia

```bash
mt vwp --anchor abertura
```

### Ajuste

```bash
mt vwp --anchor ajuste
```

### Horário específico

```bash
mt vwp --anchor hora --anchor-time "2026-01-29 09:00"
```

### Máxima / mínima do período

```bash
mt vwp --anchor maxima
mt vwp --anchor minima
```

---

## Bandas de VWAP

```bash
mt vwp --bands 2
```

Saída vertical (compatível com leitores de tela):

```
banda_sup_2
banda_sup_1
VWAP
banda_inf_1
banda_inf_2
```

---

## Saída em JSON

Indicada para automações e integração com outros plugins do mtcli:

```bash
mt vwp --bands 2 --json
```

Exemplo de saída:

```json
{
  "vwap": 123456.0,
  "anchor_type": "abertura",
  "anchor_time": null,
  "banda_sup_1": 123600.0,
  "banda_inf_1": 123300.0
}
```

---

## Configuração

O plugin aceita configuração por:

1. Variáveis de ambiente
2. Arquivo de configuração do mtcli
3. Valores padrão

Parâmetros suportados:

- `SYMBOL`
- `MINUTES`
- `LIMIT`
- `ANCHOR`
- `BANDS`
- `DIGITOS`

---

## 🧱 Estrutura do projeto

```
mtcli_vwap/
├── cli.py        # Interface de linha de comando
├── controller.py # Orquestração
├── model.py      # Cálculo da VWAP
├── view.py       # Saída acessível
├── conf.py       # Configurações
└── plugin.py     # Registro no mtcli
```

---

## Acessibilidade

- Saída exclusivamente textual
- Ordem previsível e estável
- Compatível com NVDA, JAWS e leitores de tela similares

---

## Licença

GPL

---

## Autor

**Valmir França**  
Desenvolvedor de ferramentas quantitativas, automação de trading e CLIs acessíveis.

---

## Contribuições

Contribuições são bem-vindas via issues ou pull requests.

---

> Projeto pensado para traders discricionários, automação quantitativa e leitura de contexto de fluxo.

