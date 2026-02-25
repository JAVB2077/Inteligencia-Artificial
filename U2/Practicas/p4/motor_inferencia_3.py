import json

def cargar_base_conocimiento(ruta):
    with open(ruta, 'r',encoding='utf-8') as archivo:
        return json.load(archivo)

def aplicar_reglas_inferencia(kb):
    print("Iniciando motor de inferencia avanzado/...")
    individuos = kb["individuos"]

    inferencias = {nombre: {"hermanos": [], "abuelos": [], "tios": [], "colegas": []} for nombre in individuos}

    for sujeto, datos_sujeto in individuos.items():
        padres_sujeto = set(datos_sujeto.get("padres", []))
        profesion_sujeto = datos_sujeto.get("profesion")

        for otro, datos_otro in individuos.items():
            if sujeto == otro:
                continue

            padres_otro = set(datos_otro.get("padres", []))
            profesion_otro = datos_otro.get("profesion")

            # Inferencia de hermanos
            if padres_sujeto and padres_otro == padres_otro:
                if otro not in inferencias[sujeto]["hermanos"]:
                    inferencias[sujeto]["hermanos"].append(otro)

            if profesion_sujeto and profesion_sujeto == profesion_otro:
                if otro not in inferencias[sujeto]["colegas"]:
                    inferencias[sujeto]["colegas"].append(otro)

        for padre in padres_sujeto:
            datos_del_padre = individuos.get(padre, {})
            abuelos = datos_del_padre.get("padres", [])
            for abuelo in abuelos:
                if abuelo not in inferencias[sujeto]["abuelos"]:
                    inferencias[sujeto]["abuelos"].append(abuelo)
        
    for sujeto, datos_sujeto in individuos.items():
        padres_sujeto = datos_sujeto.get("padres", [])
        for padre in padres_sujeto:
            hermanos_del_padre = inferencias[padre]["hermanos"]
            for tio in hermanos_del_padre:
                if tio not in inferencias[sujeto]["tios"]:
                    inferencias[sujeto]["tios"].append(tio)

    inferencias_limpias = {}
    for persona, deducciones in inferencias.items():
        deducciones_filtradas = {k: v for k, v in deducciones.items() if len(v) > 0}
        if deducciones_filtradas:
            inferencias_limpias[persona] = deducciones_filtradas

    kb["conocimiento_inferido"] = inferencias_limpias
    return kb
    
def main():
    archivo_json = 'ontologia3.json'

    base_conocimiento = cargar_base_conocimiento(archivo_json)
    kb_actualizada = aplicar_reglas_inferencia(base_conocimiento)

    print("======================================================")
    print("Conocimiento Inferido: (Nuevos hechos descubierto)")
    print("======================================================")
    print(json.dumps(kb_actualizada["conocimiento_inferido"], indent=4, ensure_ascii=False))

    with open('ontologia_inferida.json', 'w', encoding='utf-8') as f:
        json.dump(kb_actualizada, f, indent=4, ensure_ascii=False)
    print("Conocimiento inferido guardado en 'ontologia_inferida.json'")
    
if __name__ == "__main__":
    main()