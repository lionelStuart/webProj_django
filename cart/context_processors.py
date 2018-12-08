from .cart import Cart

"""
上下文处理器
settings
templates
tempaltes.context_processors
"""

def cart(request):
    return {'cart': Cart(request)}
