from Card import Card
from typing import List
import pandas as pd


class MTGCardPricer:
    def __init__(self, filename: str):
        self.cards_data = self.make_card_dataframe()

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

    def generate_card_objects(self, filename: str) -> List[Card]:
        """
        This method reads the file named `filename` and creates a Card object for each valid card in the file.
        :param filename: A string for the name of a file with the extension and the path
        :return:
        """
        list_lines = self.open_and_read(filename)
        list_card = []
        for line in list_lines:
            if line not in ['', '\n']:
                name_set = line[0:-1].split('~')
                card_name = name_set[0]
                if len(name_set) == 2:
                    card_set = name_set[1]
                else:
                    card_set = ''
                list_card.append(Card(card_name, card_set))
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
        return pd.DataFrame({'name': list_card_name, 'set': list_card_set, 'price_ftf': list_card_price})

    def save_to_csv(self):
        pass
