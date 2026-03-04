# Importar bibliotecas
import pandas as pd

# Função para gerar um relatório com as classes correspondentes aos componentes detectados no relatório 'yolo_detections.csv'
def gerar_relatorio_classes(report_detections_path, report_classes_path, csv_output_path):

    # Extrair os relatórios
    df_detections = pd.read_csv(report_detections_path)
    df_classes = pd.read_excel(report_classes_path)

    # Gerar um novo relatório com a coluna 'classe_componente'
    df_final = df_detections.merge(
        df_classes[["id_componente", "classe_componente"]],
        on="id_componente",
        how="left"
    )

    # Ordernar as colunas no relatório
    df_final = df_final[
        [
            "nome_imagem",
            "id_componente",
            "nome_componente",
            "classe_componente",
            "quantidade"
        ]
    ]

    # Salvar o relatório final
    df_final.to_csv(csv_output_path, index=False)

    print(f"Relatório csv com as classes dos componentes gerado com sucesso.")

    return df_final