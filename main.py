import requests
from bs4 import BeautifulSoup
import pandas as pd
import random

headers = {'User-Agent':
               'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.106 Safari/537.36'}

pages = ["https://www.transfermarkt.com/slovan-bratislava/startseite/verein/540/saison_id/2023",
         "https://www.transfermarkt.com/msk-zilina/startseite/verein/1443/saison_id/2023",
         "https://www.transfermarkt.com/spartak-trnava/startseite/verein/365/saison_id/2023",
         "https://www.transfermarkt.com/mfk-dukla-banska-bystrica/startseite/verein/20758/saison_id/2023",
         "https://www.transfermarkt.com/dac-dunajska-streda/startseite/verein/4529/saison_id/2023",
         "https://www.transfermarkt.com/as-trencin/startseite/verein/7918/saison_id/2023",
         "https://www.transfermarkt.com/fk-zeleziarne-podbrezova/startseite/verein/20063/saison_id/2023",
         "https://www.transfermarkt.com/mfk-ruzomberok/startseite/verein/7087/saison_id/2023",
         "https://www.transfermarkt.com/mfk-skalica/startseite/verein/35488/saison_id/2023",
         "https://www.transfermarkt.com/fc-kosice/startseite/verein/51316/saison_id/2023",
         "https://www.transfermarkt.com/zemplin-michalovce/startseite/verein/13744/saison_id/2023",
         "https://www.transfermarkt.com/vion-zlate-moravce-vrable/startseite/verein/12005/saison_id/2023"]

all_players = []
all_values = []
for page in pages:
    pageTree = requests.get(page, headers=headers)
    pageSoup = BeautifulSoup(pageTree.content, 'html.parser')

    PlayersList = [x.text.replace("\n", "").replace("\xa0", "").strip() for x in
                   pageSoup.find_all("td", {"class": "hauptlink"})[:-7]][::2]
    all_players.extend(PlayersList)

    # Values = pageSoup.find_all("td", {"class": "rechts hauptlink"})
    Values = [x.text.replace("€", "").replace("k", "000").replace("m", "0000").replace(".", "").strip() for x in
              pageSoup.find_all("td", {"class": "rechts hauptlink"})]
    all_values.extend(Values)

# print(all_values)
# print(all_players)
df = pd.DataFrame({"Players": all_players, "Values": all_values})
#df.to_csv("nike_liga_data.csv", index=True)

def football_player_guess_game():
    # Randomly select two different indices
    indices = random.sample(range(len(df)), 2)

    # Display the names and ask for the guess
    print("Football Player Value Guessing Game:")
    # print(f"1. {df['Players'][indices[0]]}")
    # print(f"2. {df['Players'][indices[1]]}")
    # print(f"1. {df['Values'][indices[0]]}")
    # print(f"2. {df['Values'][indices[1]]}")

    # Get user input for the guess
    user_guess = input(
        f"{df['Players'][indices[0]]} market value is €{int(df['Values'][indices[0]]) / 1000000}m.\nDoes {df['Players'][indices[1]]} have a HIGHER or LOWER market value than {df['Players'][indices[0]]}?\n Type 'H' for HIGHER and type 'L' for LOWER: ")

    # Check the answer
    user_guess = user_guess.lower()
    if user_guess == "h":
        # final_price = df['Values'][indices[1]] -  df['Values'][indices[0]]
        if int(df['Values'][indices[1]]) > int(df['Values'][indices[0]]):
            print(
                f"Correct! You guessed it right. {df['Players'][indices[1]]} value is €{int(df['Values'][indices[1]]) / 1000000}m.")

        elif int(df['Values'][indices[1]]) < int(df['Values'][indices[0]]):
            print(
                f"Wrong! because {df['Players'][indices[1]]} value is only €{int(df['Values'][indices[1]]) / 1000000}m.")

        elif int(df['Values'][indices[0]]) == int(df['Values'][indices[1]]):
            print(
                f"Values of {df['Players'][indices[0]]} and {int(df['Players'][indices[1]])} are equal: €{int(df['Values'][indices[0]]) / 1000000}m.")

    elif user_guess == "l":
        if int(df['Values'][indices[0]]) > int(df['Values'][indices[1]]):
            print(
                f"Yes you are right, {df['Players'][indices[1]]} value is lower --->>> €{int(df['Values'][indices[1]]) / 1000000}m.")

        elif int(df['Values'][indices[0]]) < int(df['Values'][indices[1]]):
            print(
                f"Wrong answer! because {df['Players'][indices[1]]} value is higher --->>> €{int(df['Values'][indices[1]]) / 1000000}m.")

        elif int(df['Values'][indices[0]]) == int(df['Values'][indices[1]]):
            print(
                f"Values of {df['Players'][indices[0]]} and {int(df['Players'][indices[1]])} are equal: €{int(df['Values'][indices[0]]) / 1000000}m.")

    else:
        print("I do not understand your query...")


# Run the game
football_player_guess_game()