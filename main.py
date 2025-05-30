# Paso 1: Importar librerías necesarias
from google.colab import files
import ipywidgets as widgets
from IPython.display import display, clear_output
import pandas as pd
import os

def main()

  # Paso 2: Widget para subir archivo
  upload_button = widgets.FileUpload(
      accept='.lis',  # solo acepta archivos .lis
      multiple=False
  )
  
  # Paso 3: Botón para convertir a Excel
  convert_button = widgets.Button(
      description='Convertir a Excel',
      button_style='success'
  )
  
  # Paso 4: Zona para mostrar mensajes
  output = widgets.Output()
  
  # Paso 5: Función para convertir .lis a .xlsx
  def convertir_lis_a_excel(change):
      with output:
          clear_output()
          if not upload_button.value:
              print("Por favor, sube un archivo .lis primero.")
              return
  
          # Obtener el archivo subido
          uploaded_file = list(upload_button.value.values())[0]
          filename = uploaded_file['metadata']['name']
          content = uploaded_file['content']
  
          # Guardar archivo temporalmente
          with open(filename, 'wb') as f:
              f.write(content)
  
          # Leer el archivo .lis como texto plano
          try:
              df = pd.read_csv(filename, sep='|', engine='python', encoding='latin1')  # ajusta según formato del .lis
              nombre_excel = filename.replace('.lis', '.xlsx')
              for i in df.columns:
                  if 'fecha' in i:
                      df[i]=pd.to_datetime(df[i],format='%b %d %Y %I:%M:%S:%f%p')
              df.to_excel(nombre_excel, index=False)
              files.download(nombre_excel)
              print(f"✅ Archivo convertido exitosamente: {nombre_excel}")
          except Exception as e:
              print(f"❌ Error al convertir el archivo: {e}")
  
  # Paso 6: Conectar botón a la función
  convert_button.on_click(convertir_lis_a_excel)
  
  # Paso 7: Mostrar widgets
  display(widgets.HTML("<h2>Convertidor de archivos .lis a .xlsx</h2>"))
  display(widgets.HTML("1. Sube el archivo .lis"))
  display(upload_button)
  display(widgets.HTML("2. Haz clic para convertir y descargar"))
  display(convert_button)
  display(output)
