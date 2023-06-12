import gi
from gi.repository import Gtk
gi.require_version('Gtk', '3.0')
import requests

def on_b_baixar_clicked(button):
    entrada = builder.get_object("texto_url")
    url = 'https://' + entrada.get_text()
    
    response = requests.get(url)

    # Verificar se a solicitação foi bem-sucedida (código de status 200 indica sucesso)
    if response.status_code == 200:
        # Caminho de destino onde a imagem será salva
        path = "./images/"

        # Salvar o conteúdo da resposta no arquivo
        with open(path, "wb") as file:
            file.write(response.content)

        print("Imagem baixada com sucesso.")
    else:
        print("Falha ao baixar a imagem.")

def on_janela_destroy(widget):
    Gtk.main_quit()




builder = Gtk.Builder()
builder.add_from_file("./modelo.glade")  # Substitua pelo caminho real para o seu arquivo Glade
builder.connect_signals({"on_b_baixar_clicked": on_b_baixar_clicked})
builder.connect_signals({"on_janela_destroy": on_janela_destroy})

window = builder.get_object("janela")
window.show_all()

Gtk.main()