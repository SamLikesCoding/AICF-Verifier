from selenium.webdriver import Firefox as Ff
from selenium.webdriver.firefox.options import Options
from collections import Counter
import pandas as pd
from datetime import datetime as dt


class Verifier:

    def __init__(self):
        print(" Initalizing program... ")
        options = Options()
        options.headless = True
        self.browser = Ff(options=options)
        self.playerSet = None
        self.URL = 'http://aicf.in/player-search/?q='

    def start_checking(self, input_file):
        names = []
        rtg = []
        fide_ids = []
        status = []
        print(" Accessing csv file... ")
        self.playerSet = pd.read_csv(input_file)
        print(" Getting Player Data... ")
        self.playerSet["Fide-No"].fillna(0, inplace=True)
        for player in self.playerSet.index:
            if self.playerSet["Fide-No"][player] != 0:
                self.browser.get("{}{}".format(self.URL, self.playerSet["Fide-No"][player]))
                results = self.browser.find_elements_by_tag_name('td')
                if len(results) != 0:
                    names.append(self.playerSet["Name"][player])
                    fide_ids.append(self.playerSet["Fide-No"][player])
                    rtg.append(self.playerSet["IRtg"][player])
                    status.append(results[5].text)
                    print("{} ({}) -> {}".format(self.playerSet["Name"][player], self.playerSet["Fide-No"][player],
                                                results[5].text))
                else:
                    names.append(self.playerSet["Name"][player])
                    fide_ids.append(self.playerSet["Fide-No"][player])
                    rtg.append(self.playerSet["IRtg"][player])
                    status.append("PlayerNotExists")
                    print("{}({}) -> {}".format(self.playerSet["Name"][player], self.playerSet["Fide-No"][player],
                                                "PlayerNotExists"))
            else:
                names.append(self.playerSet["Name"][player])
                fide_ids.append(self.playerSet["Fide-No"][player])
                rtg.append(self.playerSet["IRtg"][player])
                status.append("Not Found")
                print("{} ({}) -> {}".format(self.playerSet["Name"][player], self.playerSet["Fide-No"][player], "Not Found"))

        print(" Writing out to file... ")
        pd.DataFrame({
            "Name": names,
            "Rating": rtg,
            "FIDE-ID": fide_ids,
            "Status": status
        },).to_csv("AICF_Checked_{}.csv".format(dt.now().strftime("%d-%m-%Y_%H.%m.%S")))
        print(" => AICF Check completed ")
        print("\n --- Statistics --- ")
        stat = [[x, status.count(x)] for x in set(status)]
        for item in stat:
            print("{} : {}".format(item[0], item[1]))

    def end(self):
        print("\n== Program terminated ==")
        self.browser.close()


if __name__ == '__main__':
    verify = Verifier()
    verify.start_checking("AICF_FIDE_LIST.csv")
    verify.end()
