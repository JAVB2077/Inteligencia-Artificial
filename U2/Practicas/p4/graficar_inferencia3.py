import matplotlib
import networkx as nx
import matplotlib.pyplot as plt
import json

def cargar_json(ruta):
    with open (ruta, 'r', encoding='utf-8') as f:
        return json.load(f)

def generar_grafo():
    kb = cargar_json('ontologia_inferida.json')
    G = nx.DiGraph()

    individuos = kb.get("individuoa",{})
    inferidos = kb.get("conocimiento_inferido", {})

    #Nodos (personas)
    for nombre in individuos.keys():
        G.add_node(nombre)

    #Relaciones Implicitas
    for sujeto, datos in individuos.items():
        #Padres
        for padre in datos.get("padres",[]):
            G.add_edge(sujeto, padre, relation = "padre_de", tipo = "explicito")
        #Eaposos/Esposas
        if "esposa" in datos:
            G.add_edge(sujeto, datos["esposa"], relation = "esposo_de", tipo ="explicito")
        if "esposo" in datos:
            G.add_edge(sujeto, datos["esposo"], relation = "esposa_de", tipo ="explicito")

    #Relaciones inferidas
    for sujeto, deducciones in inferidos.items():
        for tipo_relaciones, lista_nombres in deducciones.items():
            for nombre_inferido in lista_nombres:
                #tipo_relaciones puede ser "hermanos", "abuelos", "tios", "colegas"
                G.add_edge(sujeto,nombre_inferido, relation = "tipo_relacion", tipo = "inferido")

    #-----GRAFO-------
    print("Generando imagen...")
    plt.figure(figsize = (16,12))

    pos = nx.spring_layout(G, k=1.5,iterations=60,seed=42)
    
    #Nodos
    nx.draw_networkx_nodes(G, pos, node_size=3000, node_color='lightblue', edgecolors='black')
    nx.draw_networkx_labels(G, pos, font_size=10, font_weight='bold')

    aristas_explicitas = [(u, v) for u, v, d in G.edges(data=True) if d['tipo'] == 'explicito']
    aristas_inferidas = [(u, v) for u, v, d in G.edges(data=True) if d['tipo'] == 'inferido']

    #flechas explicitas
    nx.draw_networkx_edges(G, pos, edgelist=aristas_explicitas,edge_color='gray',
                           arrows=True, arrowsize=15, connectionstyle='arc3, rad=0.2')
    
    #flechas inferidas rojas
    nx.draw_networkx_edges(G, pos, edgelist=aristas_inferidas, edge_color='red', style='dashed',
                           arrows=True, arrowsize=15, connectionstyle='arc3, rad=0.2')
    
    #etiquetas de relaciones
    edge_labels = nx.get_edge_attributes(G, 'relation')
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_size=7)

    # leyenda
    plt.plot([], [], color='gray', label='Relación Explícito(JSON Original)')
    plt.plot([], [], color='red', linestyle='dashed', label='Relación Inferida(Motor de Inferencia)')
    plt.legend(loc='upper left')

    plt.title("Red semántica: Conocimiento Explícito vs Inferido", fontsize=16)
    plt.axis('off')

    nombre_archivo = "grafo_inferencia3.png"
    plt.savefig(nombre_archivo, bbox_inches='tight', dpi=150)
    print(f"la imagen ha sido guardada como: {nombre_archivo}")

if __name__ == "__main__":
    generar_grafo()