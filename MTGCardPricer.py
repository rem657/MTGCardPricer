from Card import Card, time
from typing import List
import pandas as pd


def make_card(card_name: str, card_set: str, is_foil: bool, quantity: int):
    try:
        new_card = Card(card_name, card_set, is_foil, quantity)
    except:
        print('an error occurred trying again soon')
        time.sleep(2)
        new_card = make_card(card_name, card_set, is_foil, quantity)
    return new_card


class MTGCardPricer:
    def __init__(self, filename: str):
        self.cards_data = self.make_card_dataframe(filename)
        self.calculate_total_price()
        self.save_to_csv(filename[:-4])

    @staticmethod
    def open_and_read(filename: str) -> List[str]:
        """
        This method opens up a file named `filename` and returns a list of every line.
        :param filename: A string for the name of a file with the extension and the path
        :return: A list of string where every element is a line in the file
        """
        with open(filename, 'r') as read_file:
            list_lines = read_file.readlines()
        return list_lines

    @staticmethod
    def get_card_from_string(card_string: str):
        """
        This method takes a string in the form `quantity`x`cardname`~`cardset`~`card finish` and return a these parameters.
        quantity, cardset and card finish are optional
        :param card_string:
        :return: An int for the quantity, a string of the card name, a string of the card set, a bool whether or not it'
        s foil.
        """
        # checks quantity
        if card_string[0].isnumeric():
            quantity_card = card_string.split('x')
            quantity = int(quantity_card[0])
            card_string = ''.join(quantity_card[1:])
        else:
            quantity = 1
        # Checks card name
        name_set = card_string[0:-1].split('~')
        card_name = name_set[0]
        # Checks card set
        if len(name_set) >= 2:
            card_set = name_set[1]
        else:
            card_set = ''
        if len(name_set) >= 3:
            card_finish = name_set[2]
        else:
            card_finish = ''
        # check finish
        if card_finish.capitalize() == 'FOIL':
            is_foil = True
        else:
            is_foil = False
        return quantity, card_name, card_set, is_foil

    def generate_card_objects(self, filename: str) -> List[Card]:
        """
        This method reads the file named `filename` and creates a Card object for each valid card in the file.
        :param filename: A string for the name of a file with the extension and the path
        :return:
        """
        list_lines = self.open_and_read(filename)
        list_card = []
        number_of_entry = len(list_lines)
        for i, line in enumerate(list_lines):
            if line not in ['', '\n']:
                quantity, card_name, card_set, is_foil = self.get_card_from_string(line)
                new_card = make_card(card_name, card_set, is_foil, quantity)
                print(f'card done : {i + 1}/{number_of_entry}')
                list_card.append(new_card)
        return list_card

    def make_card_dataframe(self, filename: str) -> pd.DataFrame:
        """
        This method generates a dataframe containing the card names, their sets and their price from face to face games
        :param filename:
        :return:
        """
        list_card = self.generate_card_objects(filename)

        def get_card_attribute(card: Card, attribute_name: str):
            return card.__dict__[attribute_name]

        list_card_name = list(map(lambda card: get_card_attribute(card, 'name'), list_card))
        list_card_set = list(map(lambda card: get_card_attribute(card, 'set'), list_card))
        list_card_price = list(map(lambda card: get_card_attribute(card, 'price_ftf'), list_card))
        list_card_quantity = list(map(lambda card: get_card_attribute(card, 'quantity'), list_card))

        return pd.DataFrame({'name': list_card_name, 'quantity': list_card_quantity, 'set': list_card_set,
                             'price_ftf': list_card_price})

    def calculate_total_price(self):
        """
        This method calculates the total price of the given cards and adds a line to the card_data dataframe with this
         information
        :return:
        """
        index = self.cards_data.index
        total_price = 0
        total_quantity = 0
        for index_num in index:
            quantity = self.cards_data.loc[index_num, 'quantity']
            price = self.cards_data.loc[index_num, 'price_ftf']
            total_price += price * quantity
            total_quantity += quantity
        self.cards_data.loc[index[-1] + 1, 'name'] = 'TOTAL'
        self.cards_data.loc[index[-1] + 1, 'quantity'] = total_quantity
        self.cards_data.loc[index[-1] + 1, 'price_ftf'] = total_price

    def save_to_csv(self, filename: str):
        """
        This method saves the attribute cards_data, which is a dataframe, to a csv file name `filename`
        :param filename:
        :return:
        """
        self.cards_data.to_csv(f'{filename}.csv')


if __name__ == '__main__':
    MTGCardPricer('sellList.txt')
