from django import template

register = template.Library()

@register.filter
def get_discounted_price(deal, price):
    """Calculate discounted price for a deal"""
    return deal.get_discounted_price(price)