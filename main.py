import os
import pandas as pd
import numpy as np
import sqlite3
import matplotlib.pyplot as plt
import requests


def fetch_race_results(season=2023):
    url = f"http://ergast.com/api/f1/{season}/results.json?limit=1000"
    response = requests.get(url)
    data = response.json()
    
    races = data['MRData']['RaceTable']['Races']
    
    records = []
    for race in races:
        race_name = race['raceName']
        round_no = race['round']
        date = race['date']
        for result in race['Results']:
            driver = result['Driver']
            constructor = result['Constructor']
            records.append({
                'season': season,
                'round': int(round_no),
                'race': race_name,
                'date': date,
                'position': int(result['position']),
                'driver': f"{driver['givenName']} {driver['familyName']}",
                'constructor': constructor['name'],
                'points': float(result['points'])
            })

    return pd.DataFrame(records)

def save_to_sqlite(df, db_name="f1_data.db"):
    conn = sqlite3.connect(db_name)
    df.to_sql("race_results", conn, if_exists="replace", index=False)
    conn.close()



def load_from_sqlite(db_name="f1_data.db"):
    conn = sqlite3.connect(db_name)
    df = pd.read_sql("SELECT * FROM race_results", conn)
    conn.close()
    return df


def plot_driver_points(df):
    summary = df.groupby('driver')['points'].sum().sort_values(ascending=False).head(10)
    summary.plot(kind='barh')
    plt.xlabel("Total Points")
    plt.title("Top 10 Drivers by Points")
    plt.gca().invert_yaxis()
    plt.tight_layout()
    plt.show()

def plot_constructors(df):
    summary = df.groupby('constructor')['points'].sum().sort_values(ascending=False).head(10)
    summary.plot(kind='bar')
    plt.ylabel("Total Points")
    plt.title("Top 10 Constructors by Points")
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()
    
def plot_driver_trend(df, driver_name):
    df_driver = df[df['driver'] == driver_name]
    df_driver = df_driver.sort_values('round')
    plt.plot(df_driver['round'], df_driver['points'], marker='o')
    plt.title(f"{driver_name} - Points per Race")
    plt.xlabel("Round")
    plt.ylabel("Points")
    plt.grid(True)
    plt.tight_layout()
    plt.show()

def plot_constructor_trend(df, constructor_name):
    df_team = df[df['constructor'] == constructor_name]
    df_team = df_team.groupby('round')['points'].sum().sort_index()
    df_team.plot(marker='o')
    plt.title(f"{constructor_name} - Team Points per Round")
    plt.xlabel("Round")
    plt.ylabel("Points")
    plt.grid(True)
    plt.tight_layout()
    plt.show()

def plot_podium_counts(df):
    podium_df = df[df['position'] <= 3]
    podium_counts = podium_df['driver'].value_counts().head(10)
    podium_counts.plot(kind='bar')
    plt.title("Top 10 Drivers by Podium Finishes")
    plt.ylabel("Number of Podiums (Top 3)")
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()

def plot_points_distribution(df):
    top_drivers = df.groupby('driver')['points'].sum().sort_values(ascending=False).head(5).index
    df_filtered = df[df['driver'].isin(top_drivers)]
    df_filtered.boxplot(column='points', by='driver')
    plt.title("Points per Race Distribution (Top 5 Drivers)")
    plt.suptitle("")  # Removes extra default title
    plt.xlabel("Driver")
    plt.ylabel("Points per Race")
    plt.tight_layout()
    plt.show()


def main():
    df = fetch_race_results(season=2023)
    save_to_sqlite(df)
    df_loaded = load_from_sqlite()

    plot_driver_points(df_loaded)
    plot_constructors(df_loaded)
    plot_podium_counts(df_loaded)
    plot_points_distribution(df_loaded)
    plot_driver_trend(df_loaded, "Max Verstappen")
    plot_constructor_trend(df_loaded, "Red Bull")


if __name__ == "__main__":
    main()