import stripe

from django.conf import settings

stripe.api_key = settings.STRIPE_SECRET_KEY


def create_stripe_product(product):
    """Создаёт продукт в Stripe и возвращает его ID."""
    stripe_product = stripe.Product.create(
        name=product.title,
        description=product.description or 'Без описания',
    )

    return stripe_product.id


def create_stripe_price(product, stripe_product_id):
    """Создаёт цену в Stripe и возвращает её ID."""
    stripe_price = stripe.Price.create(
        product=stripe_product_id,
        unit_amount=int(product.price * 100),
        currency=settings.STRIPE_CURRENCY,
    )

    return stripe_price.id


def create_stripe_checkout_session(product, stripe_price_id):
    """Создаёт Checkout Session и возвращает ссылку на оплату."""
    session = stripe.checkout.Session.create(
        line_items=[
            {
                'price': stripe_price_id,
                'quantity': 1,
            }
        ],
        mode='payment',
        success_url='http://127.0.0.1:8000/api/payments/success/',
        cancel_url='http://127.0.0.1:8000/api/payments/cancel/',
    )

    return session.id, session.url


def create_payment_session(product):
    """
    Полный сценарий:
    продукт → цена → checkout-сессия.
    """
    stripe_product_id = create_stripe_product(product)
    stripe_price_id = create_stripe_price(product, stripe_product_id)
    session_id, payment_url = create_stripe_checkout_session(
        product,
        stripe_price_id,
    )

    return {
        'stripe_product_id': stripe_product_id,
        'stripe_price_id': stripe_price_id,
        'stripe_session_id': session_id,
        'payment_url': payment_url,
    }


def retrieve_stripe_session(session_id):
    """Получает статус checkout-сессии из Stripe."""
    session = stripe.checkout.Session.retrieve(session_id)

    return {
        'session_id': session.id,
        'payment_status': session.payment_status,
        'status': session.status,
    }