"""
    - Management of the days of the week
    - How many days until a given day

    Returns:
        String: A response at the question concerning calendar or day 
"""
import calendar
import datetime

from lib.sound import Audio
from lib.logger import Logger
from lib.utils import Utils
from lib.__init__ import Settings

# ---- File for get the week of the day ----
class Calendar:
    """
    Class for manage the function and settings
    """
    def __init__(self) -> None:
        self.utils =Utils()
        self.logger = Logger()
        self.audio = Audio()
        self.setting = Settings()
        self.lang = self.setting.language



    def clear_number(self,day:str,month:str) -> tuple:
        """
        This works by forming the numbers in such a way that they do not contain the 0 in the case of single-digit numbers 

        Example: 09 -> 9

        Args:
            day (str): The day to format
            month (str):The month to format

        Returns:
            tuple: The two number formatted
        """

        day = int(day)
        month = int(month)
        day = str(day)
        month = str(month)
        return day,month

    def gen_phrase(self,date:str) -> str or None:
        """
        The function generates the final phrase that will then be played back

        Args:
            date (str): The final date calculated

        Returns:
            str or None: The final phrase that will then be played back
        """
        day,month,year = date.split("-")
        day,month = self.clear_number(day,month)
        index_week = self.index_day_of_week(year,month,day)
        print(f" {self.setting.split_calendar[0]} {day} {self.setting.split_calendar[1]} {self.setting.months_calendar[int(month)-1]} {self.setting.split_calendar[2]} {year} {self.setting.split_calendar[3]} {self.setting.week_calendar[index_week]}",
              flush=True)
        if (day is None or day == '') or month is None or year is None:
            print("I'm sorry but I couldn't get the date right you can reapply",
                  flush=True)
            self.audio.create(file=True,namefile="ErrorDate")
        else:
            if(day != 1 or day != 11):
                return f"{self.setting.split_calendar[0]} {self.utils.number_to_word(str(day))} {self.setting.split_calendar[1]} {self.setting.months_calendar[int(month)-1]} {self.setting.split_calendar[2]} {self.utils.number_to_word(str(year))} {self.setting.split_calendar[3]} {str(self.setting.week_calendar[index_week])}"
            return f"{self.setting.split_calendar[6]}{self.utils.number_to_word(str(day))} {self.setting.split_calendar[1]} {self.setting.months_calendar[int(month)-1]} {self.setting.split_calendar[2]} {self.utils.number_to_word(str(year))} {self.setting.split_calendar[3]} {str(self.setting.week_calendar[index_week])}"
        return None    

    def index_day_of_week(self,year:int,month:int,day:int) -> int:
        """
        This function calculates which week of the year it belongs and returns its index

        Args:
            year (int): The year 
            month (int): The month
            day (int): The day

        Returns:
            int: The index of the week from 0 to 6
        """
        year = int(year)
        month = int(month)
        day = int(day)
        index = 0
        for week in calendar.monthcalendar(year,month):
            for days in week:
                if days == day:
                    index=week.index(days)
        return index

    def recover_date(self,sentence) -> str:
        """
        This function extracts the dates from a sentence

        Args:
            sentence (list): The input sentence

        Returns:
            str: The date formatted
        """
        count_of_number = self.utils.count_number(sentence)
        if count_of_number == 2:
            year = sentence[-1]
            month = self.setting.months_calendar.index(sentence[len(sentence) - 2]) + 1
            day = sentence[len(sentence) - 3]
            return f"{day}-{month}-{year}"
        if(count_of_number  == 1 and self.check_month(sentence)):
            today_date  = datetime.datetime.now().date()
            month = self.setting.months_calendar.index(sentence[-1]) + 1
            day = sentence[len(sentence) - 2]
            return f"{day}-{month}-{today_date.year}"
        if(count_of_number  == 1 and not self.check_month(sentence)):
            today_date  = datetime.datetime.now().date()
            day = sentence[-1]
            return f"{day}-{today_date.month}-{today_date.year}"
        return "I'm sorry there was an error of some kind"

    def check_month(self,sentence):
        """
        Checks whether or not the word is part of months list

        Args:
            sentence (list): The input sentence

        Returns:
            bool: if the word is a months
        """
        for word in sentence:
            if word in self.setting.months_calendar:
                return True
        return False

    def recov_preset_date(self,command:str) -> str or None:
        """
        Check if there is a fixed date pattern in the sentence if there is, retrieve the date

        Args:
            command (str): The input sentence

        Returns:
            str/none: formatted date or None if in the sentence there is no pattern
        """
        pattern = "%d-%m-%Y"
        if any(elem in self.setting.words_meaning_after_tomorrow  for elem in command):
            today = datetime.datetime.today()
            after_tomorrow = today + datetime.timedelta(days=2)
            formatted_date = after_tomorrow.strftime(pattern)
            return formatted_date
        if  any(elem in self.setting.words_meaning_tomorrow  for elem in command):
            today = datetime.datetime.today()
            tomorrow = today + datetime.timedelta(days=1)
            formatted_date = tomorrow.strftime(pattern)
            return formatted_date
        if any(elem in self.setting.words_meaning_yesterday  for elem in command):
            today = datetime.datetime.today()
            yesterday = today + datetime.timedelta(days=-1)
            formatted_date = yesterday.strftime(pattern)
            return formatted_date
        if any(elem in self.setting.words_meaning_today  for elem in command):
            today = datetime.datetime.today()
            today = today + datetime.timedelta(days=0)
            formatted_date = today.strftime(pattern)
            return formatted_date
        return None

    def diff_date(self,command:list) -> str:
        """
        Try to calculate the difference between the current date and the date in the sentence

        Args:
            command (list): Input

        Returns:
            str: The final phrase which will then be reproduced 
        """
        preset_date  = self.recov_preset_date(command)
        if preset_date is None:
            date = self.recover_date(command)
        elif self.utils.count_number("".join(command)) > 0:
            date = self.recover_date(command)
            date[0] = date[0] + 1
            date = "-".join(date)
        else:
            date = preset_date

        day,month,year = date.split("-")
        day,month = self.clear_number(day,month)
        correct_date = datetime.datetime(int(year), int(month), int(day))
        diff_days = (datetime.datetime.now() - correct_date).days
        print(self.logger.log(
            f"result: {self.setting.phrase_calendar[0]} {day} {month} {year} {self.setting.phrase_calendar[2]} {diff_days * -1}"),
              flush=True)
        if diff_days * -1 == 1:
            return f" {self.setting.phrase_calendar[0]} {self.utils.number_to_word(day)} {self.utils.number_to_word(month)} {self.utils.number_to_word(year)} {self.setting.phrase_calendar[1]}"
        return f" {self.setting.phrase_calendar[0]} {self.utils.number_to_word(day)}, {self.utils.number_to_word(month)}, {self.utils.number_to_word(year)} {self.setting.phrase_calendar[2]} {self.utils.number_to_word(diff_days * -1)} {self.setting.phrase_calendar[3]}"

    def get_date(self,command:list) -> str:
        """
        Try to get the date in the sentence and then calculate which day of the week it falls on

        Args:
            command (list): input sentence

        Returns:
            str: The final sentence with the correct information 
        """
        preset_date  = self.recov_preset_date(command)
        if preset_date is None:
            date = self.recover_date(command)
            output = self.gen_phrase(date)
            return output
        if self.utils.count_number("".join(command)) > 0:
            date = self.recover_date(command)
            date[0] = date[0] + 1
            date = "-".join(date)
            output = self.gen_phrase(date)
            return output
        output = self.gen_phrase(preset_date)
        return output
