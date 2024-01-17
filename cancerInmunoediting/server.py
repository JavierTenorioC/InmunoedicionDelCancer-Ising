import mesa
from cancerInmunoediting.model import CancerInmunoediting

# Diccionario de parametros configurables por el usuario: estos se asignan a los parametros de inicializacion del modelo
model_params = {
    "meanIS": mesa.visualization.Slider(
        "meanIS", 0.9, 0.01, 1, 0.01, description="Media de la distribucion del Sistema Inmunologico"
    ),
    "stdIS": mesa.visualization.Slider(
        "stdIS", 0.05, 0.01, 1, 0.01, description="Desviacion estandar de la distribucion del Sistema Inmunologico",
    ),
    "meanCancer": mesa.visualization.Slider(
        "meanCancer", 0.9, 0.01, 1, 0.01, description="Media de la distribucion del Cancer",
    ),
    "stdCancer": mesa.visualization.Slider(
        "stdCancer", 0.05, 0.01, 1, 0.01, description="Desviacion estandar de la distribucion del Cancer",
    ),
}

# Elemento de grafico 1
chart_element1 = mesa.visualization.ChartModule(
    [
        {"Label": "CancerCells", "Color": "#2596be"},
        {"Label": "CellsM1",     "Color": "#9925be"},
        {"Label": "CellsM2",     "Color": "#be4d25"},
        {"Label": "CellsN1",     "Color": "#49be25"},
        {"Label": "CellsN2",     "Color": "#bea925"},
        {"Label": "CellsNK",     "Color": "#041014"},
    ]
)

# Elemento de grafico 2
chart_element2 = mesa.visualization.ChartModule(
    [
        {"Label": "ProCancer",  "Color": "#2596be"},
        {"Label": "AntiCancer", "Color": "#041014"}
    ]
)

# Elemento de grafico 3
chart_element3 = mesa.visualization.ChartModule(
    [
        {"Label": "HAntiCancer",  "Color": "#2596be"},
        {"Label": "HProCancer", "Color": "#041014"},
        {"Label": "HTME", "Color": "#be4d25"},
    ]
)

# Elemento de grafico 4
chart_element4 = mesa.visualization.ChartModule(
    [
        {"Label": "TumorGrowthRate",  "Color": "#2596be"},
    ]
)

# Crear instancia del servidor modular de Mesa
server = mesa.visualization.ModularServer(
    CancerInmunoediting,  # Clase del modelo
    [chart_element1, chart_element2, chart_element3, chart_element4],  # Elementos de graficos para visualizar
    "Cancer Inmunoediting Model",  # Titulo del servidor
    model_params=model_params,  # Parametros del modelo
)
