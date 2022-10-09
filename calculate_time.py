from math import ceil as c
from json import load


def calculate(microsoft_gift_card: bool, purchase_cost: int, accounts: int, daily_points: int):
    """:param microsoft_gift_card: bool - this needs to be specified since microsoft gift cards are cheaper
    :param purchase_cost: int - eg. for a $72.50 item, enter 73
    :param accounts: int - eg. 3 accounts running consecutively
    :param daily_points: int - the average amount of points you will make daily, which should practically always be 230"""
    needed_gift_cards = c(purchase_cost / 5)
    needed_points_per_account = 0

    if accounts == 1:
        if microsoft_gift_card == "yes":
            needed_points_per_account += needed_gift_cards * 4750
        else:
            needed_points_per_account += needed_gift_cards * 6750

        estimated_time = c(needed_points_per_account / daily_points)
        excess_value = purchase_cost - (needed_gift_cards * 5)
        print(f'It will take {estimated_time} days to get {needed_gift_cards} $5 gift cards to purchase your item that costs ${purchase_cost}, therefore an excess giftcard value of ${excess_value}')
    elif accounts >= 2:
        gift_cards_needed_per_account = c(needed_gift_cards / accounts)

        if microsoft_gift_card == "yes":
            needed_points_per_account += gift_cards_needed_per_account * 4750
        else:
            needed_points_per_account += gift_cards_needed_per_account * 6750

        estimated_time = c(needed_points_per_account / daily_points)
        excess_value = (gift_cards_needed_per_account * 5 * accounts) - purchase_cost
        print(f'It will take {estimated_time} days to get {gift_cards_needed_per_account} $5 gift cards on each {accounts} accounts, to purchase your item that costs ${purchase_cost}, therefore an excess giftcard value of ${excess_value}')


calculate(microsoft_gift_card=load(open('credentials.json'))['calculate time config']['redeem_microsoft_gift_card?'],
          purchase_cost=load(open('credentials.json'))['calculate time config']["how much does it cost to buy your item in $"],
          accounts=load(open('credentials.json'))['config']['How many accounts are you using?'],
          daily_points=230)
