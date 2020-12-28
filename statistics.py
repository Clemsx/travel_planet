import pandas as pd
import numpy as np
import requests
import os
import json
import matplotlib.pyplot as plt
import plotly.express as px

from bs4 import BeautifulSoup


class Statistics():

    def __init__(self, path):
        self.path = path
        self.orders = []

    def get_files(self):
        list_files = os.listdir(self.path)

        for files in list_files:
            with open(self.path + "/" + files, encoding='utf-8-sig') as f:
                tmp_data = json.load(f)
                self.orders.append(tmp_data)

    def stats_by_type(self):
        presta_df = pd.DataFrame()

        for order in self.orders:
            presta_df = presta_df.append(
                pd.DataFrame.from_dict(order['prestations']), ignore_index=True)

        presta_df.value_counts('type').plot(
            kind='barh', figsize=(10, 7), rot=0)
        plt.xlabel("number", labelpad=14)
        plt.ylabel("number of order", labelpad=14)
        plt.show()

    def stats_by_currency(self):
        curr_df = pd.DataFrame()

        for order in self.orders:
            curr_df = curr_df.append(
                pd.json_normalize(order['prestations'][0]['price']), ignore_index=True)

        curr_df.value_counts('currency').plot(
            kind='bar', figsize=(10, 7), rot=0)
        plt.xlabel("currency", labelpad=14)
        plt.ylabel("number of order", labelpad=14)
        plt.show()

    def stats_by_origin(self):
        df = pd.DataFrame()

        for order in self.orders:
            if "trip" in order:
                df = df.append(pd.json_normalize(
                    order['trip']), ignore_index=True)

        df.value_counts('origin.country_code').plot(
            kind='bar', figsize=(10, 7), rot=50)
        plt.xlabel("country code", labelpad=14)
        plt.ylabel("number of order", labelpad=14)
        plt.show()

    def stats_by_destination(self):
        df = pd.DataFrame()

        for order in self.orders:
            if "trip" in order:
                df = df.append(pd.json_normalize(
                    order['trip']), ignore_index=True)

        df.value_counts('destination.country_code').plot(
            kind='bar', figsize=(10, 7), rot=50)
        plt.xlabel("country code", labelpad=14)
        plt.ylabel("number of order", labelpad=14)
        plt.show()

    def stats_by_supplier(self):
        supplier_df = pd.DataFrame()

        for order in self.orders:
            supplier_df = supplier_df.append(
                pd.DataFrame.from_dict(order['prestations']), ignore_index=True)

        supplier_df.value_counts('supplier').plot(
            kind='barh', figsize=(10, 7), rot=0)
        plt.xlabel("currency", labelpad=14)
        plt.ylabel("number of order", labelpad=14)
        plt.show()


if __name__ == "__main__":

    stats = Statistics(path="DATA")

    stats.get_files()

    # UNCOMMENT TO SEE THE CORRESPONDING PLOT
    # stats.stats_by_type()
    # stats.stats_by_currency()
    # stats.stats_by_origin()
    # stats.stats_by_destination()
    # stats.stats_by_supplier()
