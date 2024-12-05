from shop.models import Produto

class Carrinho():
    def __init__(self, request):
        self.sessao = request.session

        carrinho = self.sessao.get('session_key')

        if 'session_key' not in request.session:
            carrinho = self.sessao['session_key'] = {}

        self.carrinho = carrinho

    def adicionar(self, produto, quantidade):
        produto_id = str(produto.id)
        produto_quantidade = str(quantidade)
        if produto_id in self.carrinho:
            pass
        else:
            #self.carrinho[produto_id] = {'preço': str(produto.preco)}
            self.carrinho[produto_id] = int(produto_quantidade)

        self.sessao.modified = True

    def carrinho_total(self):
        produto_ids = self.carrinho.keys()
        produtos = Produto.objects.filter(id__in=produto_ids)
        quantidade = self.carrinho
        total = 0
        for key, value in quantidade.items():
            key = int(key)
            for produto in produtos:
                if produto.id == key:
                    if produto.promocao:
                        total = total + (produto.preco_promocao * value)
                    else:
                        total = total + (produto.preco * value)
        return total

    def __len__(self):
        return len(self.carrinho)
    
    def get_produtos(self):
        produto_ids = self.carrinho.keys()
        produtos = Produto.objects.filter(id__in=produto_ids)

        return produtos
    
    def get_quantidade(self):
        quantidade = self.carrinho
        return quantidade
    
    def atualizar(self, produto, quantidade):
        produto_id = str(produto)
        produto_quantidade = int(quantidade)
        ourcarrinho = self.carrinho
        ourcarrinho[produto_id] = produto_quantidade

        self.sessao.modified = True

        thing = self.carrinho
        return thing
    
    def deletar(self, produto):
        produto_id = str(produto)
        if produto_id in self.carrinho:
            del self.carrinho[produto_id]
        
        self.sessao.modified = True
