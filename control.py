import serial
import serial.tools.list_ports
import pyautogui
import time

CODIGO_SIGUIENTE = 'BF40FF00' # <-- PON TU CODIGO DE AVANZAR AQUI
CODIGO_ANTERIOR = 'BB44FF00' # <-- PON TU CODIGO DE RETROCEDER AQUI

def conectar_arduino():
    puertos = list(serial.tools.list_ports.comports())
    
    # 1. Intento automático
    for p in puertos:
        if any(palabra in p.description for palabra in ['Arduino', 'CH340', 'USB Serial', 'Serie USB']):
            return p.device
            
    # 2. Si no lo reconoció por nombre, muestra todos los disponibles
    if len(puertos) > 0:
        print("\nNo se detecto el nombre automatico, pero encontre estos puertos:")
        for i, p in enumerate(puertos):
            print(f" [{i}] {p.device} - {p.description}")
        opcion = input("\nEscribe el numero de puerto (ej. 0) y presiona Enter: ")
        return puertos[int(opcion)].device
        
    return None

print("Buscando Arduino...")
puerto = None
while puerto is None:
    puerto = conectar_arduino()
    if puerto is None:
        print("Ningun puerto detectado. Revisa el cable o el driver...")
        time.sleep(3)

print(f"Conectado a {puerto}...")
arduino = serial.Serial(puerto, 9600)
time.sleep(2)
print("¡LISTO! Abre Canva en pantalla completa.")

while True:
    if arduino.in_waiting > 0:
        linea = arduino.readline().decode('utf-8').strip().upper()
        if linea == CODIGO_SIGUIENTE:
            pyautogui.press('pagedown')
            print("-> Siguiente")
        elif linea == CODIGO_ANTERIOR:
            pyautogui.press('pageup')
            print("<- Anterior")
