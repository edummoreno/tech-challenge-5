# Importar bibliotecas
from ultralytics import YOLO
from pathlib import Path
from collections import Counter
import pandas as pd

# Função que retorna uma lista com os nomes de cada imagem
def gerar_lista_imagens(dir_path):
  dir_path = Path(dir_path)
  images_list = []

  for item in dir_path.iterdir():
    if item.is_file():
      images_list.append(item.name)

  print(images_list)

  return images_list

# Função que carrega o best.pt do modelo yolo fine tunado
def carregar_yolo(model_path):
  model = YOLO(model_path)
  print("Modelo yolo carregado.")

  return model

# Função que aplica yolo nas imagens listadas
def aplicar_yolo(yolo_model, images_list, source, imgsz, conf, iou, save, name, verbose):
  yolo_detections = []

  for i in images_list:
    print(f'\nDetectando os componentes da imagem {i}')
    folder_name = i.split('.', 1)[0]
    results = yolo_model.predict(
        source=f'{source}/{i}',
        imgsz=960,
        conf=0.25,
        iou=0.5,
        save=True,
        name=f'{name}/imagens_yolo_{folder_name}',
        verbose=verbose
        )

    img = results[0]
    cls_ids = img.boxes.cls.cpu().numpy().astype(int).tolist()
    counts = Counter(cls_ids)
    rows = [(i, cls_id, img.names[cls_id], qty) for cls_id, qty in counts.items()]
    yolo_detections.append(rows)

  print('\nImagens analisadas pelo yolo.')

  return yolo_detections

# Função que transforma os resultados em um DataFrame
def gerar_dataframe(detections_list):
  df = pd.DataFrame(
      [x for sub in detections_list for x in sub],
      columns=['nome_imagem', 'id_componente', 'nome_componente', 'quantidade']
      )
  print("\nDataFrame gerado.")

  return df

# Função para gerar relatório csv
def gerar_relatorio_csv(dataframe, report_path):
  dataframe.to_csv(f'{report_path}/yolo_detections.csv', index=False)
  print("\nRelatório csv gerado com sucesso.")

  return dataframe
