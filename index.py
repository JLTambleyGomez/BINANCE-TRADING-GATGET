import ctypes
import sys
import tkinter as tk
import requests
import threading
from binance.client import Client
from PIL import Image, ImageTk

if sys.platform == 'win32':
    ctypes.windll.user32.ShowWindow(ctypes.windll.kernel32.GetConsoleWindow(), 0)


# Crea una ventana principal
window = tk.Tk()
window.title("Binance Mica Bot by JorgeTambley")

background_image = Image.open("12111.png")
background_photo = ImageTk.PhotoImage(background_image)
# Crea el widget para la imagen de fondo
background_label = tk.Label(window, image=background_photo)
background_label.place(x=0, y=0, relwidth=1, relheight=1)
# Agrega campos de entrada de texto para el usuario

usdt_amount_label = tk.Label(window, text='Bienvenido Binance Spot Gatget By JL:')
usdt_amount_label.pack()
usdt_amount_label = tk.Label(window, text='Completa los Datos')
usdt_amount_label.pack()

usdt_amount_label = tk.Label(window, text='Monto USDT Por Compra:')
usdt_amount_label.pack()

usdt_amount_entry = tk.Entry(window)
usdt_amount_entry.pack()

api_key_label = tk.Label(window, text='API key:')
api_key_label.pack()

api_key_entry = tk.Entry(window)
api_key_entry.pack()

api_secret_label = tk.Label(window, text='API secret:')
api_secret_label.pack()

api_secret_entry = tk.Entry(window, show='*')
api_secret_entry.pack()

testnet_var = tk.BooleanVar()
testnet_checkbox = tk.Checkbutton(window, text='Usar modo de prueba', variable=testnet_var)
testnet_checkbox.pack()

def confirm_and_close_window():
    # Obtén los valores ingresados por el usuario
    global usdt_amount, api_key, api_secret
    usdt_amount = float(usdt_amount_entry.get())
    api_key = api_key_entry.get()
    api_secret = api_secret_entry.get()
    window.destroy()

# Crea botones para que el usuario pueda confirmar las entradas
confirm_button = tk.Button(window, text='Confirmar', command=confirm_and_close_window)
confirm_button.pack()

cancel_button = tk.Button(window, text='Cancelar', command=window.destroy)
cancel_button.pack()

# Ejecuta la ventana principal y espera a que el usuario la cierre
window.mainloop()

client = Client(api_key, api_secret, testnet=testnet_var.get())

def trade(pair, quantity, trade_type):
    if trade_type == 'buy':
        order = client.order_market_buy(
            symbol=pair,
            quantity=quantity
        )
    elif trade_type == 'sell':
        order = client.order_market_sell(
            symbol=pair,
            quantity=quantity
        )
    else:
        return 'Invalid trade type'

    return order

def get_price(pair):
    url = f'https://api.binance.com/api/v3/ticker/price?symbol={pair}'
    response = requests.get(url)
    data = response.json()
    return float(data['price'])

def get_balance(asset):
    balance = client.get_asset_balance(asset=asset)
    return float(balance['free'])

usdt_balance = get_balance('USDT')
btc_balance = get_balance('BTC')

initial_balance = usdt_balance + (btc_balance * get_price("BTCUSDT"))

usdt_amount_label_text = f'USDT balance: {usdt_balance:.2f}'
btc_amount_label_text = f'BTC balance: {btc_balance:.8f}'

window = tk.Tk()
window.title("Binance Mica Bot")
# Obtiene las dimensiones de la ventana

background_image = Image.open("12111.png")
background_photo = ImageTk.PhotoImage(background_image)
# Crea el widget para la imagen de fondo
background_label = tk.Label(window, image=background_photo)
background_label.place(x=0, y=0, relwidth=1, relheight=1)

usdt_amount_label = tk.Label(window, text=usdt_amount_label_text)
usdt_amount_label.pack()

btc_amount_label = tk.Label(window, text=btc_amount_label_text)
btc_amount_label.pack()

pair_label_text = f'Valor: {get_price("BTCUSDT"):.2f}'
pair_label = tk.Label(window, text=pair_label_text)
pair_label.pack()

profit_label_text = f'Ganancias: {0:.2f}'
profit_label = tk.Label(window, text=profit_label_text)
profit_label.pack()

def update_pair_value():
    def get_price(pair):
        url = f'https://api.binance.com/api/v3/ticker/price?symbol={pair}'
        response = requests.get(url)
        data = response.json()
        return float(data['price'])

    pair_label_text = f'Valor: {get_price("BTCUSDT"):.2f}'
    pair_label.configure(text=pair_label_text)
    window.after(1000, update_pair_value) 
update_pair_value()

def update_profit():
    global usdt_balance, btc_balance, initial_balance
    current_balance = usdt_balance + (btc_balance * get_price("BTCUSDT"))
    profit = current_balance - initial_balance
    profit_label_text = f'Ganancias: {profit:.2f}'
    profit_label.configure(text=profit_label_text)
    window.after(3000, update_profit)

update_profit()


def buy():
    global usdt_balance, btc_balance, usdt_amount_label_text, btc_amount_label_text, initial_balance
    value = get_price("BTCUSDT")
    quantity = usdt_amount/value
    quantity = round(quantity, 4)
    trade('BTCUSDT', quantity, 'buy')
    usdt_balance = get_balance('USDT')
    btc_balance = get_balance('BTC')
    current_balance = usdt_balance + (btc_balance * get_price("BTCUSDT"))
    profit = current_balance - initial_balance
    profit_label_text = f'Ganancias: {profit:.2f}'
    profit_label.configure(text=profit_label_text)
    usdt_amount_label_text = f'USDT balance: {usdt_balance:.2f}'
    usdt_amount_label.configure(text=usdt_amount_label_text)
    btc_amount_label_text = f'BTC balance: {btc_balance:.8f}'
    btc_amount_label.configure(text=btc_amount_label_text)

def sell():
    global usdt_balance, btc_balance, usdt_amount_label_text, btc_amount_label_text, initial_balance
    quantity = usdt_amount/ get_price("BTCUSDT")
    quantity = round(quantity, 4)
    trade('BTCUSDT', quantity, 'sell')
    usdt_balance = get_balance('USDT')
    btc_balance = get_balance('BTC')
    current_balance = usdt_balance + (btc_balance * get_price("BTCUSDT"))
    profit = current_balance - initial_balance
    profit_label_text = f'Ganancias: {profit:.2f}'
    profit_label.configure(text=profit_label_text)
    usdt_amount_label_text = f'USDT balance: {usdt_balance:.2f}'
    usdt_amount_label.configure(text=usdt_amount_label_text)
    btc_amount_label_text = f'BTC balance: {btc_balance:.8f}'
    btc_amount_label.configure(text=btc_amount_label_text)
    
def sell_all():
    global usdt_balance, btc_balance, usdt_amount_label_text, btc_amount_label_text, initial_balance
    quantity = btc_balance
    trade('BTCUSDT', quantity, 'sell')
    usdt_balance = get_balance('USDT')
    btc_balance = get_balance('BTC')
    current_balance = usdt_balance + (btc_balance * get_price("BTCUSDT"))
    profit = current_balance - initial_balance
    profit_label_text = f'Ganancias: {profit:.2f}'
    profit_label.configure(text=profit_label_text)
    usdt_amount_label_text = f'USDT balance: {usdt_balance:.2f}'
    usdt_amount_label.configure(text=usdt_amount_label_text)
    btc_amount_label_text = f'BTC balance: {btc_balance:.8f}'
    btc_amount_label.configure(text=btc_amount_label_text)

    
def buy_wrapper():
    threading.Thread(target=buy).start()

def sell_wrapper():
    threading.Thread(target=sell).start()

def sell_all_wrapper():
    threading.Thread(target=sell_all).start()


buy_button = tk.Button(window, text="Comprar", command=buy_wrapper)
buy_button.pack()

sell_button = tk.Button(window, text="Vender", command=sell_wrapper)
sell_button.pack()

sell_all_button = tk.Button(window, text="Vender todo", command=sell_all_wrapper)
sell_all_button.pack()

window.mainloop()
