# Tech Challenge 5 — Modelagem de Ameaças Automática (STRIDE) com YOLO + LLM

Este projeto automatiza a modelagem de ameaças em diagramas de arquitetura:
1) Detecta componentes na imagem com **YOLO (Ultralytics)**  
2) Classifica os componentes detectados em **classes**  
3) Usa **LLM + RAG (JSONs por classe)** para gerar análise **STRIDE**  
4) Gera um **relatório PDF** por imagem

---

## ✅ Entregáveis
- Repositório (este GitHub)
- Vídeo (até 15 min) explicando solução e execução
- Relatórios gerados (PDF/CSV)

---

## 📂 Estrutura do projeto
- `scripts/` — pipeline e notebooks (entrada principal: `main.ipynb`)
- `rag_documents/` — base RAG em JSON (1 arquivo por classe)
- `imagens/imagens_source/` — imagens de entrada (diagramas)
- `imagens/imagens_yolo_*` — imagens de saída com bounding boxes (evidência)
- `reports/` — saídas finais e arquivos de apoio
  - `yolo_detections.csv` / `yolo_detections_classified.csv`
  - `component_classes.xlsx` (mapeamento id -> classe)
  - `relatorio_stride_<nome>.pdf`
- `models/` — (opcional) peso do YOLO `best.pt`

---

## ▶️ Como executar (modo oficial: Google Colab + Drive)
### Pré-requisitos
- Conta Google (Drive)
- Chave da OpenAI configurada como Secret no Colab: `OPENAI_API_KEY`

### Passo a passo
1) Faça upload da pasta do projeto para o seu Drive em:
   `MyDrive/Tech Challenge 5/`
2) Abra no Colab:
   `scripts/main.ipynb`
3) No Colab, adicione o Secret:
   - Name: `OPENAI_API_KEY`
   - Value: sua chave
4) Execute todas as células.

### Saídas esperadas
- `reports/yolo_detections.csv`
- `reports/yolo_detections_classified.csv`
- `reports/relatorio_stride_<imagem>.pdf`

---

## 🔐 Configuração da chave OpenAI (sem expor no GitHub)
No notebook `scripts/main.ipynb`, a chave é lida via Secret do Colab e setada em variável de ambiente:
- `OPENAI_API_KEY`

> Nunca commite a chave no repositório.

---

## 🧠 Como o relatório STRIDE é gerado
Para cada imagem:
1) YOLO detecta componentes e gera CSV de detecções
2) Um mapeamento (`component_classes.xlsx`) associa cada componente a uma classe
3) Para cada classe encontrada, o pipeline:
   - carrega o JSON RAG correspondente em `rag_documents/`
   - chama o LLM pedindo um JSON PT-BR com 6 itens STRIDE (ordem fixa)
4) O PDF final é montado via ReportLab

---

## 🗃️ Datasets / arquivos grandes (fora do GitHub)
Por limite de tamanho, estes itens NÃO ficam no GitHub:
- Dataset(s) de treino
- YOLO dataset (labels/imagens)
- Runs completos do treinamento

📌 Link do Drive (preencher):
- Dataset: [COLE_AQUI_O_LINK_DO_DRIVE]
- (Opcional) Artefatos de treino: [COLE_AQUI_O_LINK_DO_DRIVE]

---

## ✅ Modelos (YOLO)
O notebook espera um peso `best.pt`.

Opção A (recomendada): versionar só o peso final (≈52MB)
- Coloque em: `models/best.pt`
- Ajuste o caminho no notebook (1 linha)

Opção B: manter no Drive e referenciar no notebook
- Coloque em: `MyDrive/Tech Challenge 5/resultados_yolo/fine_tuning_train/weights/best.pt`

---

## 👥 Integrantes
- Nome 1
- Nome 2
- Nome 3