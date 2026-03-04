# Importar bibliotecas
import json
from openai import OpenAI

_client = OpenAI()

# Função para retornar os prompts que serão enviados para o llm
def retornar_llm_prompts(class_name, components_list_json, json_file):

    # Prompt do system
    system_prompt = """
    Você é um Especialista em Modelagem de Ameaças e recebeu o nome de uma classe que representa um conjunto de componentes de nuvem. 
    Sua tarefa é gerar um relatório para essa classe, detalhando as vulnerabilidades e as contramedidas para mitigar ou até mesmo prevenir essas ameaças, com base na metodologia STRIDE.
    
    Você receberá um arquivo RAG e deve usá-lo como referência técnica e contextual; no entanto, não copie e cole as frases deste arquivo em sua resposta final, pois este arquivo é apenas para seu aprendizado.
    
    Você deve retornar um JSON válido (apenas o JSON, sem markdown, sem texto adicional) e mantendo o 'stride_analysis' como lista igual no arquivo RAG.
    
    O JSON final deve conter apenas os campos: 'class_name', 'components', 'stride_analysis' e dentro do 'stride_analysis' os campos 'type', 'threat', 'countermeasures'.
    
    O campo stride_analysis deve conter exatamente 6 itens e exatamente nessa mesma ordem, um para cada tipo STRIDE: Spoofing, Tampering, Repudiation, Information Disclosure, Denial of Service, Elevation of Privilege.
    
    Se algum tipo não estiver explícito no RAG, use o tipo mesmo assim, mas baseie a ameaça apenas em padrões compatíveis com a classe e nos controles do RAG (sem criar vulnerabilidades ou contramedidas fora do escopo).

    Antes de responder, revise internamente se alguma ameaça pressupõe detalhes não garantidos pelo RAG/diagrama e reescreva para forma condicional sem perder especificidade.
    
    Não coloque uma 'threat' muito genérica, é esperado no relatório o mesmo nível de especificidade que existe no arquivo RAG. 
    
    Cada 'threat' deve ser descrita em uma frase.
    
    Para o campo 'countermeasures', liste no mínimo 1 até no máximo 3 contramedidas para a ameaça selecionada no campo 'threat'.
    
    Qualidade é melhor que quantidade então não liste 'countermeasures' que você não tem certeza que irão funcionar contra a ameaça.
    
    O relatório deve ser obrigatóriamente gerado em linguagem PT-BR.

    Revise a ortografia antes de enviar a resposta.
    """
    
    # Prompt do user
    user_prompt = f"""
    Gere o relatório STRIDE para:
    
    Nome classe (use exatamente estes valores para preencher o campo 'class_name'):
    {class_name}
    
    Componentes (use exatamente estes valores para preencher o campo 'components'):
    {components_list_json}
    
    Arquivo RAG para referência:
    <documento_rag>
    {json_file}
    </documento_rag>
    """
    return system_prompt, user_prompt

# Função para enviar a pergunta ao llm
def enviar_pergunta_llm(system_prompt, user_prompt, model, temperature, max_tokens):
    response = _client.responses.create(
        model=model,
        input=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ],
        temperature=temperature,
        max_output_tokens=max_tokens,
    )

    # Verificar se o llm retornou um resposta e se essa resposta não esta vazia
    msg = next(o for o in response.output if o.type == "message")
    json_text = msg.content[0].text

    if len(json_text.strip()) > 0:
      print(f"Resposta da llm para esta classe retornada com sucesso.\n")

    return json_text