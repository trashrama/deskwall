# Deskwall: Aplicação de Wallpaper
## 2. Deskwall - Implementações de S.O

> O programa deve incluir um campo de texto e
> dois botões. Ao clicar no botão “Baixar”, o programa baixa a imagem indicada na URL, salvando como um arquivo local.
> 
> Ao clicar no botão “Definir como Wallpaper”, o Wallpaper do Desktop (Gnome) deverá ser definido para esse arquivo baixado.
> 
> Além disso, uma notificação deve ser apresentada no Desktop avisando que o Wallpaper foi modificado. Para fazer essa notificação, você pode executar o programa notify-send passando como argumento a mensagem.
> 
> Você deve executar isso a partir do seu código Python (sugestão: usar
> o comando em Python os.system).
> 
> Bônus (opcional): seu programa deve tocar um som gravado dizendo
> “Wallpaper modificado”.
> 
> Obs.: a interface deve ser feita em **Glade**.

Bom, este é o segundo programa que eu implementei. Ele tem a interface em **Glade**, e segue a risca as instruções da implementação, juntamente dos sons que adicionei nas ações. Foi feito em **Python**, **Glade** e algumas funções externas de **Gtk**.

---
### Para problemas de dependência:

 - Talvez, você encontre problemas de dependências, então é recomendável que você instale:
#### subprocess: `sudo apt install subprocess`
#### notify-send: `sudo apt install notify-send`
#### pyGObject (para rodar o Gi): `pip install PyGObject`


