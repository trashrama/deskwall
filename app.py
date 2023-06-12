import gi
from gi.repository import Gtk
gi.require_version('Gtk', '3.0')
import requests
import os

listaTipos = ['png', 'jpeg', 'jpg', 'svg', 'gif', 'bmp']

pathConcluido = ''

def notificaSucesso(caminho):

    os.system(f"notify-send -i info 'Concluído' 'Salvo em {caminho}'")
    os.system("paplay ./audio/downloadConcluido.ogg")

def notificaFalha(falha):

    os.system(f"notify-send -i error 'Erro' '{falha}'")
    os.system("paplay ./audio/falha.ogg")

def notificaTroca():
    os.system(f"notify-send -i info 'Erro' 'Seu wallpaper novo já está pronto'")
    os.system("paplay ./audio/wallpaperModificado.ogg")

def on_b_baixar_clicked(button):

    global pathConcluido  
    encontrouTipo = False

    entrada = builder.get_object("texto_url")
    url = entrada.get_text()
    if url != '':
        if not url.startswith("http://") and not url.startswith("https://"):

            url = f'http://{url}' 
        

        for tipo in listaTipos:
            if tipo in url:
                encontrouTipo = True
                response = requests.get(url)
                
                if response.status_code == 200:
                    path = "./images/"
                    if not os.path.exists(path):
                        os.makedirs(path)

                    with open(os.path.join(path, "wallpaper.png"), "wb") as file:
                        file.write(response.content)
            
                    pathConcluido = f'{path}wallpaper.png'
                    notificaSucesso(pathConcluido)

                    break
        if encontrouTipo == False:
            notificaFalha('Não é uma imagem')
        
        encontrouTipo = False

    else:
        notificaFalha('URL vazia')

def on_b_wall_clicked(button):
    notificaTroca()
    print(pathConcluido)


def on_janela_destroy(widget):
    Gtk.main_quit()




builder = Gtk.Builder()
builder.add_from_file("./modelo.glade")
#builder.connect_signals({"on_b_baixar_clicked": on_b_baixar_clicked})
#builder.connect_signals({"on_b_wall_clicked": on_b_wall_clicked})

builder.connect_signals({"on_janela_destroy": on_janela_destroy})

window = builder.get_object("janela")
window.show_all()

Gtk.main()