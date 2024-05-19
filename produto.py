
class Produto: # Cria a classe Produto
    def __init__ (self, id, nome, preco): 
        self.id = id
        self.nome = nome
        self.preco = preco
        self.quantidade = 0 # Inicia a quantidade como 1, quando um produto é adicionado ao estoque
        
        
    def __str__(self): # Método para transformar em string
        return f"ID: {self.id}, Nome: {self.nome}, Preço: R$ {self.preco:.2f}, Quantidade: {self.quantidade}" # Retorna os produtos no estoque
        
    def adicionar_quantidade(self, quantidade): # Método para escolher a quantidade
        self.quantidade += quantidade # Como já inicia com a quantidade 1, ele pega a quantidade digitada pelo usuário e adiciona mais 1
        
        
    def listar_produtos(self): # Método para listar os produtos do estoque
        print("\nProdutos Cadastrados:")
        self.carrinho.listar_produtos() # Chama o método listar_produtos() da classe CarrinhoDeCompras
        
   
    