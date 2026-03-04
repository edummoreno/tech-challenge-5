# Importar bibliotecas
import glob, json

# Função para retornar o arquivo RAG de acordo com a classe selecionada
def retornar_documento_rag(document_path, classe_name):
  document_path = document_path

  # Normalizar o nome da classe para ficar igual ao nome que esta no arquivo RAG
  classe_name = classe_name.lower().replace(" ", "-")

  # Retornar o caminho + nome do arquivo RAG
  final_path = f'{document_path}*-{classe_name}.json'

  files = glob.glob(final_path)

  # Extrair o conteudo do arquivo RAG e salva-lo na variável de retorno em formato JSON
  if files:
    with open(files[0], 'r', encoding='utf-8') as f:
      doc = json.load(f)

    rag_content = json.dumps(doc, ensure_ascii=False, indent=2)

    print(f"Arquivo RAG '{classe_name}.json' retornado com sucesso.")
  else:
    print("Arquivo não encontrado")

  return rag_content