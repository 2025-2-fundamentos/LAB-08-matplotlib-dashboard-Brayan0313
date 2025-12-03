# pylint: disable=line-too-long
"""
Escriba el codigo que ejecute la accion solicitada.
"""

import pandas as pd
import matplotlib.pyplot as plt
import os

def pregunta_01():
    """
    El archivo `files//shipping-data.csv` contiene información sobre los envios
    de productos de una empresa. Cree un dashboard estático en HTML que
    permita visualizar los siguientes campos:

    * `Warehouse_block`

    * `Mode_of_Shipment`

    * `Customer_rating`

    * `Weight_in_gms`

    El dashboard generado debe ser similar a este:

    https://github.com/jdvelasq/LAB_matplotlib_dashboard/blob/main/shipping-dashboard-example.png

    Para ello, siga las instrucciones dadas en el siguiente video:

    https://youtu.be/AgbWALiAGVo

    Tenga en cuenta los siguientes cambios respecto al video:

    * El archivo de datos se encuentra en la carpeta `data`.

    * Todos los archivos debe ser creados en la carpeta `docs`.

    * Su código debe crear la carpeta `docs` si no existe.

    """
    
    # [CORRECCIÓN 1: Solución robusta al FileExistsError]
    # En lugar de intentar borrar la carpeta y volver a crearla, 
    # usamos 'exist_ok=True'. Esto crea la carpeta si no existe, 
    # y si ya existe, no hace nada, evitando el error [WinError 183].
    os.makedirs('docs', exist_ok=True)

    # Nota: El archivo de datos debe estar presente en 'files/input/shipping-data.csv' 
    # para que la lectura de pandas funcione.
    df = pd.read_csv('files/input/shipping-data.csv')
    
    # --- GRÁFICO 1: Shipping per warehouse (Barra) ---
    df2 = df.copy()
    plt.figure()
    counts = df2['Warehouse_block'].value_counts()
    counts.plot.bar(
        title="Shipping per warehouse",
        xlabel="Warehouse block",
        ylabel="Record count",
        color="tab:blue",
        fontsize=8
    )
    
    plt.gca().spines["top"].set_visible(False)
    plt.gca().spines["right"].set_visible(False)
    # Guardamos en la carpeta corregida 'docs'
    plt.savefig('docs/shipping_per_warehouse.png')

    # --- GRÁFICO 2: Mode of shipment (Torta/Donut) ---
    df3 = df.copy()
    plt.figure()
    counts = df3['Mode_of_Shipment'].value_counts()
    counts.plot.pie(
        title="Mode of shipment",
        wedgeprops=dict(width=0.35),
        ylabel="",
        colors=["tab:blue", "tab:orange", "tab:green"],
        autopct='%1.1f%%',
        startangle=90
    )
    # Guardamos en la carpeta corregida 'docs'
    plt.savefig('docs/mode_of_shipment.png')

    # --- GRÁFICO 3: Average Customer Rating (Barras de rango) ---
    df4 = df.copy()
    plt.figure()
    df4 = (
        df4[["Mode_of_Shipment", "Customer_rating"]]
        .groupby("Mode_of_Shipment")
        .describe()
    )
    df4.columns = df4.columns.droplevel()
    df4 = df4[["mean", "min", "max"]]
    
    # Barras de rango (Min a Max)
    plt.barh(
        y=df4.index.values,
        width=df4["max"].values - df4["min"].values,
        left=df4["min"].values,
        height=0.9,
        color="lightgray",
        alpha=0.8,
    )

    # Barras de media (Min a Mean), coloreadas según el valor de la media
    colors = [
        "tab:green" if value >= 3.0 else "tab:orange" for value in df4["mean"].values
    ]

    plt.barh(
        y=df4.index.values,
        width=df4["mean"].values - df4["min"].values,
        left=df4["min"].values,
        color=colors,
        height=0.5,
        alpha=1.0,
    )
    
    plt.title("Average Customer Rating")
    plt.xlim(0, 5) # Establecer límite de rating
    plt.gca().spines["left"].set_color("gray")
    plt.gca().spines["bottom"].set_color("gray")
    plt.gca().spines["top"].set_visible(False)
    plt.gca().spines["right"].set_visible(False)
    
    # Guardamos en la carpeta corregida 'docs'
    plt.savefig("docs/average_customer_rating.png")
    
    # --- GRÁFICO 4: Shipped Weight Distribution (Histograma) ---
    df5 = df.copy()
    plt.figure()
    df5.Weight_in_gms.plot.hist(
        title="Shipped Weight Distribution",
        color="tab:orange",
        edgecolor="white",
        bins=15
    )
    plt.gca().spines["top"].set_visible(False)
    plt.gca().spines["right"].set_visible(False)
    # Guardamos en la carpeta corregida 'docs'
    plt.savefig("docs/weight_distribution.png")

    # --- Generación del Archivo HTML ---
    html = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Shipping Dashboard Example</title>
</head>
<body>
    <h1>Shipping Dashboard Example</h1>
    <!-- Se recomienda usar estilos CSS para un mejor diseño responsive. 
         Estos estilos básicos replican el layout de 2x2. -->
    <div style="max-width: 1200px; margin: 0 auto;">
        <div style="display: flex; flex-wrap: wrap; justify-content: space-around;">
            <div style="width: 45%; min-width: 300px; margin-bottom: 20px;">
                <img src="shipping_per_warehouse.png" alt="Fig 1" style="width: 100%; height: auto; border-radius: 8px;" />
            </div>
            <div style="width: 45%; min-width: 300px; margin-bottom: 20px;">
                <img src="average_customer_rating.png" alt="Fig 3" style="width: 100%; height: auto; border-radius: 8px;" />
            </div>
            <div style="width: 45%; min-width: 300px; margin-bottom: 20px;">
                <img src="mode_of_shipment.png" alt="Fig 2" style="width: 100%; height: auto; border-radius: 8px;" />
            </div>
            <div style="width: 45%; min-width: 300px; margin-bottom: 20px;">
                <img src="weight_distribution.png" alt="Fig 4" style="width: 100%; height: auto; border-radius: 8px;" />
            </div>
        </div>
    </div>
</body>
</html>
    """
    
    # Creación y escritura del archivo index.html en la carpeta 'docs'
    with open("docs/index.html", "w") as file:
        file.write(html)
    

# [CORRECCIÓN 2: Uso de if __name__ == "__main__"]
# Esta cláusula asegura que la función pregunta_01() solo se ejecute 
# cuando el script se inicie directamente (ej. python tu_archivo.py), 
# y NO cuando sea importado por un script de pruebas.
if __name__ == "__main__":
    pregunta_01()