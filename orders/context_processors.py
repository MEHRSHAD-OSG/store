"""
NOTE:
    this folder available everywhere
"""

from .cart import Cart

def cart(request):
    return {'cart': Cart(request)}