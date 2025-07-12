import requests
import urllib.parse

def geocodificar(ubicacion, clave):
    while ubicacion == "":
        ubicacion = input("Ingrese la ubicación nuevamente: ")
    url_base = "https://graphhopper.com/api/1/geocode?"
    url = url_base + urllib.parse.urlencode({
        "q": ubicacion,
        "limit": "1",
        "key": clave
    })

    respuesta = requests.get(url)
    datos = respuesta.json()
    estado = respuesta.status_code

    if estado == 200 and len(datos["hits"]) != 0:
        lat = datos["hits"][0]["point"]["lat"]
        lng = datos["hits"][0]["point"]["lng"]
        nombre = datos["hits"][0]["name"]
        tipo = datos["hits"][0]["osm_value"]
        pais = datos["hits"][0].get("country", "")
        estado_region = datos["hits"][0].get("state", "")

        if estado_region and pais:
            nueva_ubicacion = f"{nombre}, {estado_region}, {pais}"
        elif pais:
            nueva_ubicacion = f"{nombre}, {pais}"
        else:
            nueva_ubicacion = nombre

        print(f"\nAPI Geocoding → {nueva_ubicacion} (Tipo: {tipo})\n{url}")
    else:
        lat = "null"
        lng = "null"
        nueva_ubicacion = ubicacion
        if estado != 200:
            print(f"Error {estado}: {datos.get('message','Sin mensaje')}")
    return estado, lat, lng, nueva_ubicacion

def main():
    url_ruta = "https://graphhopper.com/api/1/route?"
    clave = "860d5ce8-b860-469f-8325-815d9e9b83ee"  # Tu API Key de GraphHopper

    while True:
        print("\n========= MENÚ DE OPCIONES =========")
        print("Perfiles disponibles: car, bike, foot")
        print("Escriba 'q' o 'quit' para salir")
        print("====================================")
        perfil = input("Seleccione un perfil de vehículo: ").strip().lower()
        if perfil in ["q", "quit"]:
            print("Saliendo del programa. ¡Hasta luego!")
            break
        if perfil not in ["car", "bike", "foot"]:
            print("Perfil no válido. Se usará 'car' por defecto.")
            perfil = "car"

        origen = input("Ingrese la ubicación de origen: ")
        if origen.lower() in ["q", "quit"]:
            break
        datos_origen = geocodificar(origen, clave)

        destino = input("Ingrese la ubicación de destino: ")
        if destino.lower() in ["q", "quit"]:
            break
        datos_destino = geocodificar(destino, clave)

        print("====================================")
        if datos_origen[0] == 200 and datos_destino[0] == 200:
            punto_origen  = f"&point={datos_origen[1]}%2C{datos_origen[2]}"
            punto_destino = f"&point={datos_destino[1]}%2C{datos_destino[2]}"
            params       = {"key": clave, "vehicle": perfil}
            url_completa = url_ruta + urllib.parse.urlencode(params) + punto_origen + punto_destino

            respuesta = requests.get(url_completa)
            estado    = respuesta.status_code
            datos_ruta = respuesta.json()

            print(f"\nEstado API Rutas: {estado}")
            print(f"URL solicitud: {url_completa}\n")
            print(f"Ruta: {datos_origen[3]} → {datos_destino[3]} (vehículo: {perfil})")
            print("====================================")

            if estado == 200:
                distancia_km = datos_ruta["paths"][0]["distance"] / 1000
                tiempo_ms    = datos_ruta["paths"][0]["time"]
                seg = int(tiempo_ms / 1000 % 60)
                min = int(tiempo_ms / 1000 / 60 % 60)
                hr  = int(tiempo_ms / 1000 / 60 / 60)
                combustible_l = distancia_km / 8.0

                print(f"Distancia: {distancia_km:.2f} km")
                print(f"Duración: {hr:02d}:{min:02d}:{seg:02d}")
                print(f"Combustible aproximado: {combustible_l:.2f} L")
                print("------ Instrucciones ------")
                for paso in datos_ruta["paths"][0]["instructions"]:
                    texto = paso["text"]
                    dist = paso["distance"] / 1000
                    print(f"{texto} ({dist:.2f} km)")
                print("====================================\n")
            else:
                print(f"Error en la ruta: {datos_ruta.get('message','Desconocido')}")
        else:
            print("No fue posible obtener geocodificación para origen o destino.")

if __name__ == "__main__":
    main()
