from shop.models import Produto

class Carrinho():
    def __init__(self, request):
        self.sessao = request.session

        carrinho = self.sessao.get('session_key')

        if 'session_key' not in request.session:
            carrinho = self.sessao['session_key'] = {}

        self.carrinho = carrinho

    def adicionar(self, produto):
        produto_id = str(produto.id)
        if produto_id in self.carrinho:
            pass
        else:
            self.carrinho[produto_id] = {'preço': str(produto.preco)}

        self.sessao.modified = True

    def __len__(self):
        return len(self.carrinho)
    
    def get_produtos(self):
        produto_ids = self.carrinho.keys()
        produtos = Produto.objects.filter(id__in=produto_ids)

        return produtos