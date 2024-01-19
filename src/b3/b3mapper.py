from pathlib import Path
from datetime import datetime
import re
import sys, os, csv

class B3Mapper:
    
    def __init__(self):
        self.output_name = datetime.now()
        self._ticker_ptrn = r"(\w{4}\d{1,2})"
        self._date_ptrn = r"(\d{2}\/\d{2}\/\d{4,})"
        self._provent_ptrn = r"(\w+)"
        self._quantity_ptrn = r"(\d+)"
        self._value_ptrn = r"\D*(\d+,\d{2})\D*"
        self._total_ptrn = r"\D*(\d+,\d{2})\D*"

    def parse_earnings(self, path:Path) -> None:
        print(f"{path.absolute()} ... ")

        if path.is_file() and path.absolute().suffix == '.csv':
            self.translate_format(path.absolute())
        else:
            print(f"The file '{path.absolute()}' isnt a valid file.")


    def translate_format(self, path:str) -> None:
        errors = []
        with open(path, newline=None) as csvfile:
            spamreader = csv.reader(csvfile, delimiter=';')

            # csv.reader(csvfile) 
            for row in spamreader:
                ticker_match = re.match(self._ticker_ptrn, row[0])
                date_match = re.match(self._date_ptrn, row[1])
                quantity_match = re.match(self._quantity_ptrn, row[4])
                value_match = re.match(self._value_ptrn, row[5])
                total_match = re.match(self._total_ptrn, row[6])

                if None not in [ticker_match, date_match, quantity_match, value_match, total_match]:
                    # print(ticker_match.group(1))
                    # print(date_match.group(1))
                    # print(self.translate_provent(row[2]))
                    # print(quantity_match.group(1))
                    # print(value_match.group(1))
                    # print(total_match.group(1))

                    self.write(ticker_match.group(1), date_match.group(1), self.translate_provent(row[2]), quantity_match.group(1), value_match.group(1), total_match.group(1))
                
                else:
                    dict = {
                        "ticker": ticker_match,
                        "date": date_match,
                        "quantity": quantity_match,
                        "value": value_match,
                        "total": total_match
                    }
                    errors.append(dict)
            
            print(f"\n\tERROS {len(errors)}: \n\t\t{errors}\n\n------------------\n\n")
            

                    
    def translate_provent(self, type:str):
        type_match = re.match(self._provent_ptrn, type.upper())

        if type_match is not None:
            if (type_match.group(0) == "JUROS"):
                return "JCP"
            else:
                return type_match.group(0)
        else:
            return "OUTROS"

                
    def write(self, ticker, date, provent_type, quantity, value, total):
        file = open(self.output_name.strftime("%Y-%m-%d %H:%M:%S") + ".txt", "a+")
        file.write("\t".join([ticker, date, provent_type, quantity, value, total]))
        file.write("\n")
        file.close()

