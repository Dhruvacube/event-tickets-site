from django import template
from main.models import Games

register = template.Library()

class Invoice:
    def __init__(self, game_class: Games, amount: int, mode:str):
        self.game_class = game_class
        self.amount = amount
        self.mode = mode

@register.filter(name="payment_stats")
def payment_stats(stat: str):
    if stat == "P":
        return '<strong class="text-warning><i class="bx bx-time-five text-warning"></i> Pending</strong>'
    if stat == "F":
        return '<strong class="text-danger"><i class="bx bx-x text-danger"></i> Failed</strong>'
    if stat == "R":
        return '<strong class="text-success"><i class="bx bx-money text-success"></i> Refund Initiated</strong>'
    return '<strong class="text-success"><i class="bx bx-check-double text-success"></i> Success</strong>'

@register.filter(name="generate_invoice")
def generate_invoice(list_detailed: list):
    list_invoice_class=[]
    for i in list_detailed:
        game_class = Games.objects.filter(game_unique_id=i[0]).get()
        amount = i[-1]
        if i[1] == 'so':
            mode = 'SOLO'
        else:
            mode = 'SQUAD'
        list_invoice_class.append(Invoice(game_class=game_class, amount=amount, mode=mode))
    return list_invoice_class
