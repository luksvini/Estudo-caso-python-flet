import flet as ft
from carrinho import CarrinhoDeCompras

class App:
    def __init__(self):
        self.carrinho = CarrinhoDeCompras()

    def main(self, page: ft.Page): # Configurando titulo da página e o tema
        page.title = "Mercado"
        page.theme_mode = ft.ThemeMode.DARK

        def fechar_janela(dialog): # Começa com  a janela fechada
            dialog.open = False
            page.update()

        def mostrar_dialogo(titulo, conteudo, input_field=None, input_quantidade_field=None): # Cria uma função para chamar uma janela de dialogo com um botão OK
            dialog = ft.AlertDialog(
                modal=True,
                title=ft.Text(titulo),
                content=ft.Text(conteudo),
                actions=[ft.ElevatedButton("OK", on_click=lambda e: fechar_janela(dialog))]
            )
            page.dialog = dialog  
            dialog.open = True  # Abre essa janela
            page.update()

            if input_field:
                input_field.value = ""  

            if input_quantidade_field:
                input_quantidade_field.value = ""


        def atualizar_lista_produtos():   # Método para atualizar de forma dinamica a lista de produtos
            produtos = self.carrinho.listar_produtos()
            produtos_text = "\n".join(f"{produto.nome} - R$ {produto.preco:.2f} - ID: {produto.id}" for produto in produtos)
            if not produtos_text:
                produtos_text = "Nenhum produto no Estoque." # Se não existir produtos no estoque
            lbl_produtos.value = produtos_text
            page.update()

        def atualizar_carrinho(): # Método para atualizar de forma dinamica o carrinho
            produtos = self.carrinho.exibir_carrinho() # Chama a função de exibir itens no carrinho 
            carrinho_text = "\n".join(f"{produto.nome} - R$ {produto.preco:.2f} - Quantidade: {produto.quantidade}" for produto in produtos)
            if not carrinho_text:
                carrinho_text = "Carrinho vazio."
            lbl_carrinho.value = carrinho_text
            page.update()

        def cadastrar_produto(e):
            nome = input_nome.value.title().strip()  # Campo de input para o nome, 
            # title faz com que a primeira letra de cada palavra fique maiuscula automaticamente
            # e strip remove os espaços no inicio e no final
            preco = input_preco.value # Campo de input para o preço

            if not nome or not preco: # Se algum campo não estiver preenchido
                mostrar_dialogo("Erro", "Todos os campos devem ser preenchidos")
                return
            

            if any(char.isdigit() for char in nome):  # Se existir algum número no nome do produto
                mostrar_dialogo("Erro", "O nome do produto não pode conter números." )
                input_nome.value = "" # Limpa o valor que foi digitado
                return

            try:    # Verifica se o preço digitado foi um número
                preco = float(preco)
            except ValueError:
                mostrar_dialogo("Erro", "Preço deve ser um número")
                input_preco.value = "" # Limpa o valor que foi digitado
                return

            produto_id = self.carrinho.adicionar_produto(nome, preco) # Chama a função de adicionar produto no estoque
            mostrar_dialogo("Sucesso", f"Produto cadastrado com sucesso! ID: {produto_id}")
            input_nome.value = "" # Limpa o campo após obter sucesso em adicionar um produto
            input_preco.value = "" # Limpa o campo após obter sucesso em adicionar um produto
            atualizar_lista_produtos()  # Atualiza a lista de produtos


        def adicionar_ao_carrinho(e):
            try:                                            # Se não for digitado NÚMEROS para ID e QUANTIDADE, retorna um erro e limpa os campos
                id_produto = int(input_id_produto.value)
                quantidade = int(input_quantidade.value)
            except ValueError:
                mostrar_dialogo("Erro", "ID e quantidade devem ser números e/ou todos os campos precisam estar preenchidos",  input_id_produto, input_quantidade)
                return

            if self.carrinho.adicionar_carrinho(id_produto, quantidade):  # Função para adicionar ao carrinho e limpar os campos após
                mostrar_dialogo("Sucesso", "Produto adicionado ao carrinho com sucesso!")
                atualizar_carrinho()
                input_id_produto.value = " " # Limpa o valor que foi digitado
                input_quantidade.value = " " # Limpa o valor que foi digitado
            else:
               mostrar_dialogo("Erro", "Produto não encontrado.") # Caso não ache o produto pelo ID
               input_id_produto.value = " " # Limpa o valor que foi digitado
               input_quantidade.value = " " # Limpa o valor que foi digitado
            

        
        def remover_produto_carrinho(id_produto):    # Para remover um produto do carrinho
            if self.carrinho.remover_produto_carrinho(id_produto): # Chama a função de remover produto do carrinho
                mostrar_dialogo("Sucesso", "Produto removido do carrinho com sucesso!")
                atualizar_carrinho() 
                input_id_produto_remover_carrinho.value = "" # Limpa o valor que foi digitado
            else:
                mostrar_dialogo("Erro", "Produto não encontrado no carrinho.") # Exibe um erro caso o produto não seja encontrado pelo ID 
                input_id_produto_remover_carrinho.value = "" # Limpa o valor que foi digitado


        def remover_produto_estoque(id_produto):  # Para remover um produto do estoque
            if self.carrinho.remover_produto_estoque(id_produto): # Chama a função de remover produto do estoque
                mostrar_dialogo("Sucesso", "Produto removido do estoque com sucesso!")
                atualizar_lista_produtos()
                input_id_produto_remover_estoque.value = "" # Limpa o valor que foi digitado
            else:
                mostrar_dialogo("Erro", "Produto não encontrado no estoque." ) # Exibe um erro caso o produto não seja encontrado pelo ID 
                input_id_produto_remover_estoque.value = "" # Limpa o valor que foi digitado

        def finalizar_compra(e): # Para finalizar a compra
            total, produtos_comprados = self.carrinho.finalizar_compra() # Chama o método de finalizar a compra
            if total > 0: # Se o total for maior que 0, imprime uma mensagem com o preço do(s) produto(s) e o nome
                produtos_text = "\n".join(f"{produto.nome} - R$ {produto.preco:.2f} - Quantidade: {produto.quantidade}" for produto in produtos_comprados) 
                mostrar_dialogo("Sucesso", f"Compra finalizada.\nTotal: R$ {total:.2f}\nProduto(s): {produtos_text}")
                atualizar_carrinho() # Limpa o carrinho após a compra
            else: 
                mostrar_dialogo("Erro", "Carrinho vazio. Nenhuma compra realizada.") # Se o total for menor que 0

        input_nome = ft.TextField(label="Nome do produto") # Campo de Input para o nome do produto
        input_preco = ft.TextField(label="Preço do produto") # Campo de Input para o preço do produto
        btn_cadastrar = ft.ElevatedButton(text="Cadastrar", on_click=cadastrar_produto) # Botão para cadastrar o produto

        input_id_produto = ft.TextField(label="ID do produto") # Campo de Input para o ID do produto
        input_quantidade = ft.TextField(label="Quantidade") # Campo de Input para o a quantidade do produto
        btn_adicionar_carrinho = ft.ElevatedButton(text="Adicionar ao carrinho", on_click=adicionar_ao_carrinho) # Botão para adicionar o produto ao carrinho

        lbl_produtos = ft.Text(value="") # Cria os produtos armazenados no estoque
        lbl_carrinho = ft.Text(value="") # Cria os produtos armazenados no carrinho

        btn_finalizar_compra = ft.ElevatedButton(text="Finalizar compra", on_click=finalizar_compra) # Botão para finalizar a compra 

        input_id_produto_remover_estoque = ft.TextField(label="ID do produto para remover do estoque") # Campo de Input para remover um produto do estoque através do ID 

        input_id_produto_remover_carrinho = ft.TextField(label="ID do produto para remover do carrinho") # Campo de Input para remover um produto do carrinho através do ID 

        btn_remover_estoque = ft.ElevatedButton( # Botão para remover um produto do estoque
        text="Remover do estoque",
        on_click=lambda e: remover_produto_estoque(int(input_id_produto_remover_estoque.value)) if input_id_produto_remover_estoque.value.isdigit()  # Remove se o valor digitado correspondeer
        else mostrar_dialogo("Erro", "ID do produto deve ser um número e não pode ficar vazio.")) #  Se o valor digitado não for um número ou estiver vazio

        btn_remover_carrinho = ft.ElevatedButton( # Botão para remover um produto do carrinho
        text="Remover do carrinho",
        on_click=lambda e: remover_produto_carrinho(int(input_id_produto_remover_carrinho.value)) if input_id_produto_remover_carrinho.value.isdigit() # Remove se o valor digitado correspondeer
        else mostrar_dialogo("Erro", "ID do produto deve ser um número e não pode ficar vazio."))  #  Se o valor digitado não for um número ou estiver vazio
        
        coluna_conteudo = ft.Column([
                ft.Text("Menu", size=30, weight="bold"), # Nome do Menu, tamanho da fonte e estilo da fonte
                ft.Text("Cadastrar Produto", size=20), # Nome de Cadastrar Produto e tamanho da fonte
                input_nome, # Campo de input para o nome do produto
                input_preco, # Campo de input para o preço do produto
                btn_cadastrar, # Botão para cadastrar o produto
                ft.Divider(), # Cria uma linha divisória
                ft.Text("Produtos no Estoque", size=20), # Nome de Produtos no Estoque e tamanho da fonte
                lbl_produtos, # Produtos que foram armazenados no estoque
                ft.Divider(), # Cria uma linha divisória
                ft.Text("Adicionar ao Carrinho", size=20), # Nome de Adicionar ao Carrinho e tamanho da fonte
                input_id_produto, # Campo de input para o ID do produto
                input_quantidade, # Campo de input para a quantidade do produto
                btn_adicionar_carrinho, # Botão para adicionar o produto no carrinho
                ft.Divider(), # Cria uma linha divisória
                ft.Text("Remover Produto", size=20), # Nome de Remover Produto o e tamanho da fonte
                input_id_produto_remover_estoque, # Campo de input para o ID do produto para remover do estoque
                btn_remover_estoque, # Botão para remover um produto do estoque
                input_id_produto_remover_carrinho, # Campo de input para o ID do produto para remover do carrinho
                btn_remover_carrinho, # Botão para remover um produto do carrinho
                ft.Divider(), # Cria uma linha divisória
                ft.Text("Carrinho de Compras", size=20), # Nome de Carrinho de Compras o e tamanho da fonte
                lbl_carrinho, # Produtos que foram armazenados no carrinho de compras
                btn_finalizar_compra, # Botão para finalizar a compra
            ], alignment="start") # Alinhar no topo da coluna
        

        coluna_scroll = ft.Column([coluna_conteudo],scroll=True) # Para adicionar o Scroll ao APP

        linha_scroll = ft.Column([coluna_scroll],scroll=True,expand=1) # Para adicionar o Scroll ao APP

        page.add(linha_scroll) # Para adicionar tudo a página

    def run(self): 
        ft.app(target=self.main)

if __name__ == "__main__":
    app = App()
    app.run()
