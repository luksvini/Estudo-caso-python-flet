from produto import Produto # Importa produto da classe Produto

class CarrinhoDeCompras: # Cria a classe carrinho de compras
    def __init__(self):
        self.produtos = [] # Cria a lista de produtos
        self.produtosCarrinho = []
        self.id_counter = 1 #Inicia o ID do produto como 1
        
        
    def adicionar_produto(self, nome, preco):  # Método para adicionar produto na lista
        # Cria objeto com nome e preço informados
        preco = float(preco) # Transforma o preco para float
        produto = Produto(self.id_counter, nome, preco) # Instancia a classe Produto
        self.produtos.append(produto) # Adiciona o produto na lista
        produto_id = self.id_counter
        self.id_counter += 1 # Auto incrementa o produto_id baseado em qual produto for adicionado
        return produto_id # Imprime o produto_id
        
        
    def listar_produtos(self): # Método para listar produtos
        return self.produtos
    

    def remover_produto_estoque(self, id_produto):
        for produto in self.produtos:
            if produto.id == id_produto:
                self.produtos.remove(produto)
                return True
            return False
        
    def remover_produto_carrinho(self, id_produto):
        for produto in self.produtosCarrinho:
            if produto.id == id_produto:
                self.produtosCarrinho.remove(produto)
                return True
            return False
            
        
    def adicionar_carrinho(self, id_produto, quantidade): # Método para adicionar ao carrinho
        produto_encontrado = False # Caso NÃO seja encontrado o produto ao usuário digitar o ID na função def adicionar_produto_carrinho(self): da classe menu
        for produto in self.produtos: # Varre a lista produtos
            if produto.id == id_produto:  # Procura o produto pela ID
                produto.quantidade += quantidade # Adiciona a quantidade
                produto_encontrado = True # Produto encontrado
                if produto not in self.produtosCarrinho:
                    self.produtosCarrinho.append(produto) 
                break
        return produto_encontrado
            
    
    def exibir_carrinho(self): # Método para exibir carrinho
        return self.produtosCarrinho
                        
            
    def finalizar_compra(self): # Método para finalizar a compra
        if self.produtosCarrinho: # Caso haja item / itens no carrinho 
            total = sum(produto.preco * produto.quantidade for produto in self.produtosCarrinho) # Pega o preco do produto e multiplica com a quantidade selecionada, dentro da lista produto
            produtos_comprados = self.produtosCarrinho.copy()
            self.produtosCarrinho = []
            return total, produtos_comprados
        else:
           return 0, []
    

    