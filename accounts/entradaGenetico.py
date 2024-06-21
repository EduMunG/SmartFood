#### ALGORTIMOP PARA OBTENER EL VECTOR DESAYUNO, COMIDA COLACION Y CENA

def calculaCalorias(objetivo, caloriasQuemadas):
    if objetivo == "subir":
        superAvit = caloriasQuemadas*0.1
        calorias = caloriasQuemadas+superAvit
    else:
        deficit = caloriasQuemadas*0.1
        calorias = caloriasQuemadas-deficit
    return calorias


def caloriasQuemadas(Kg, FA):
    return Kg*FA*22

def get_vectores_Desayuno_Comida_Colacion_Cena(kg, fa, objetivo):
    caloriasDia = calculaCalorias(objetivo, caloriasQuemadas(kg, fa))
    
    ### Macros ###
    if objetivo == 'subir':
        proteina = 2 * kg
        grasa = 1.5 * kg
        carbos = (caloriasDia - proteina * 4 - grasa * 9) / 4
    else:  # Asumimos que cualquier otro objetivo es bajar de peso
        proteina = 2.5 * kg
        grasa = 0.6 * kg
        carbos = (caloriasDia - proteina * 4 - grasa * 9) / 4
    
    vectorDia = [caloriasDia, grasa, carbos, proteina]
    
    # Usamos una comprensión de listas para multiplicar cada elemento de vectorDia y redondear a dos decimales
    desayuno = [round(0.25 * x, 2) for x in vectorDia]
    colacion = [round(0.15 * x, 2) for x in vectorDia]
    comida = [round(0.40 * x, 2) for x in vectorDia]
    cena = [round(0.20 * x, 2) for x in vectorDia]
    
    return desayuno, colacion, comida, cena


### EJEMPLO SOLAMENTE ##
print(get_vectores_Desayuno_Comida_Colacion_Cena(75, 1.6, 'subir'))

