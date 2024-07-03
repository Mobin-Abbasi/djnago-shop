from store.models import Product


class Cart:
    def __init__(self, request):
        self.session = request.session
        cart = self.session.get('cart')
        if not cart:
            cart = self.session['cart'] = {}
        self.cart = cart

    def add(self, product):
        product_id = str(product.id)
        if product_id not in self.cart:
            self.cart[product_id] = {'quantity': 1, 'price': product.new_price, 'weight': product.weight}
        else:
            self.cart[product_id]['quantity'] += 1
        self.save()

    def save(self):
        self.session.modified = True
