import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
from gi.repository import GdkPixbuf

import requests
import os
import subprocess

caminho = ''
nomeArq = ''
url = ''
# usando os dois separados pra poder juntar os dois e formar um diretorio valido 

listaTipos = ['png', 'jpeg', 'jpg', 'svg', 'gif', 'bmp']
suportados = ['kde', 'cinnamon', 'gnome', 'mate']

def limpa():
    
    if caminho != '' and len(os.listdir(caminho)) > 0:
        for arq in os.listdir(caminho):
            os.remove(os.path.join(caminho, arq))


def notificaSucesso(caminho):

    os.system(f"notify-send -i info 'Concluído' 'Salvo em '{os.path.abspath(caminho)}'.'")
    os.system("paplay ./assets/audios/downloadConcluido.ogg")

def notificaFalha(falha):

    os.system(f"notify-send -i error 'Erro' '{falha}'")
    os.system("paplay ./assets/audios/falha.ogg")

def notificaTroca():
    os.system(f"notify-send -i info 'Sucesso' 'Seu wallpaper novo já está pronto.'")
    os.system("paplay ./assets/audios/wallpaperModificado.ogg")

def on_b_baixar_clicked(button):

    global caminho
    global listaTipos
    global nomeArq
    global url
    
    limpa()

    entrada = builder.get_object("texto_url")
    url = entrada.get_text()
    if url != '':
        if not url.startswith("http://") and not url.startswith("https://"):

            url = f'http://{url}' 
        

        for tipo in listaTipos:
            if ('.' + tipo) in url:
                try:
                    response = requests.get(url)
                except:
                    notificaFalha('A URL não corresponde a uma imagem')
                    return None
                
                if response.status_code == 200:
                    pathOriginal = 'images'
                    if not os.path.exists(pathOriginal):
                        os.makedirs(pathOriginal)
                    
                    nomeArq = f"wallpaper.{tipo}"
                    with open(os.path.join(pathOriginal, nomeArq), "wb") as file:
                        file.write(response.content)
                        
                    caminho = pathOriginal
                    img = builder.get_object("img")
                    pixbuf = GdkPixbuf.Pixbuf.new_from_file(os.path.join(pathOriginal, nomeArq))
                    
                    largura = (int(pixbuf.get_width() * 360) / pixbuf.get_height())
                    pixbuf = pixbuf.scale_simple(largura, 360, GdkPixbuf.InterpType.BILINEAR)
                    
                    img.set_from_pixbuf(pixbuf)

                    
                    notificaSucesso(os.path.join(pathOriginal, nomeArq))
                    botao_wall = builder.get_object("b_wall")
                    botao_wall.set_sensitive(True) # deixa ele clicavel novamente
                    return
        notificaFalha('Não é uma imagem.')

    else:
        notificaFalha('URL vazia.')

def on_b_wall_clicked(button):
    
    entrada = builder.get_object("texto_url").get_text()
    
    if entrada != url:
        botao_wall = builder.get_object("b_wall")
        botao_wall.set_sensitive(False)
        return
    
    path = os.path.abspath(os.path.join(caminho, nomeArq))
    if os.path.exists(path):
        output = subprocess.check_output('echo $DESKTOP_SESSION', shell=True)
        output = output.decode().replace('\n', '')
        if output in suportados:
            if output == suportados[0]:
                os.system(f'reg add "HKEY_CURRENT_USER\Control Panel\Desktop" /v Wallpaper /t REG_SZ /d "{path}" /f')
            elif output == suportados[1]:
               os.system(f'qdbus org.kde.plasmashell /PlasmaShell org.kde.PlasmaShell.evaluateScript "var Desktops = desktops(); \
                    for (i=0;i<Desktops.length;i++) \
                    Desktops[i].wallpaperPlugin = \"org.kde.image\"; \
                    for (i=0;i<Desktops.length;i++) \
                    Desktops[i].currentConfigGroup = Array(\"Wallpaper\", \"org.kde.image\", \"General\"); \
                    for (i=0;i<Desktops.length;i++) \
                    Desktops[i].writeConfig(\"Image\", \"file://{path}\")"')
            elif output == suportados[2]:
                os.system(f'gsettings set org.cinnamon.desktop.background picture-uri "file://{path}"')
            elif output == suportados[3]:
                os.system(f'gsettings set org.gnome.desktop.background picture-uri "file://{path}"')
            else:
                os.system(f'gsettings set org.mate.background picture-filename "{path}"')

            notificaTroca()
    else:
        notificaFalha('Wallpaper não encontrado!')
    

def on_b_sobre_clicked(button):
    janela_sobre = Gtk.Window()
    janela_sobre.set_title("Sobre")
    janela_sobre.set_default_size(300, 400)
    janela_sobre.set_resizable(False) 

    box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10)
    
    imagem = Gtk.Image()
    imagem.set_from_file(os.path.join('assets', 'triforce.svg'))
    pixbuf = imagem.get_pixbuf().scale_simple(50, 50, GdkPixbuf.InterpType.BILINEAR)
    imagem.set_from_pixbuf(pixbuf)    
    
    # Calcula as coordenadas para centralizar a imagem
    x = (300 - 50) / 2
    y = (200 - 50) / 2
    
    box.pack_start(imagem, True, True, 0)
    
    label = Gtk.Label()
    label.set_text("Criado pelos Sábios da Triforce\n   <b>(<b>sant</b>, <b>neosant</b> e <b>sant!ago</b>)</b>")
    label.set_use_markup(True)
    box.pack_start(label, True, True, 0)
    
    janela_sobre.add(box)
    janela_sobre.set_position(Gtk.WindowPosition.CENTER)
    

    janela_sobre.show_all()


def on_janela_destroy(widget):
    Gtk.main_quit()


limpa()

builder = Gtk.Builder()
builder.add_from_file("./modelo.glade")

handlers = {
    "on_b_baixar_clicked": on_b_baixar_clicked,
    "on_b_wall_clicked": on_b_wall_clicked,
    "on_janela_destroy": on_janela_destroy,
    "on_b_sobre_clicked":on_b_sobre_clicked
}

builder.connect_signals(handlers)

window = builder.get_object("janela")
window.set_position(Gtk.WindowPosition.CENTER)
window.set_title("Deskwall: uma aplicação para S.O")
window.show_all()

botao_wall = builder.get_object("b_wall")
botao_wall.set_sensitive(False)

Gtk.main()