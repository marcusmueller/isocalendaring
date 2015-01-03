#!/usr/bin/python2

import datetime
import locale
from sys import stdout, stderr
from os import linesep

_day = datetime.timedelta(days=1)
_week = 7 * _day
_monday_n = 1 #just to avoid confusion
_weekdays = [getattr(locale, "DAY_"+str((d + 1) % 7 + 1)) for d in range(7)]

class isoyearcalendar(object):
    """
    Class representing a year's calendar in ISO weeks. Start with week 1 (the first week of the year containing a thursday).
    """

    _output_stream = stdout
    def __init__(self, year):
        """
        Constructs the isocalendar object for the given year.
        """
        self._year = year
        self._jan1 = datetime.date(year, 1, 1)
        isoyear, isoweek, isoweekday = self._jan1.isocalendar()
        assert(isoyear == year)
        self._firstweek = isoweek
    
    def _print(self, string):
            self._output_stream.write(string.encode("utf8"))
    def _println(self, string):
        self._print(string + linesep)


    def getweekof(self, month, day = 1):
        """
        Returns a list containing the days in that week
        """
        date = datetime.date(self._year, month, day)
        _, isoweek, isoweekday = date.isocalendar()
        monday = date - ((isoweekday - _monday_n) * _day)
        return isoweek, [monday + day * _day for day in range(7)]

    def monthweeks(self, month):
        week = self.getweekof(month, 1)
        _, currweek = week
        currday = currweek[0]
        while currday.month == month or (currday.month%12 == month - 1): #January of next year is < december...
            yield week
            currday += _week
            week = self.getweekof(month, currday.day)
            _, currweek = week
    _latex_prolog = """\\documentclass{scrartcl}
    \\usepackage[latin1]{inputenc}
    \\usepackage[T1]{fontenc}
    \\usepackage{lmodern}
    \\usepackage[paperwidth=20cm,paperheight=30cm,margin=1cm]{geometry}
    \\usepackage{microtype}
    \\usepackage[table]{xcolor}
    \\usepackage{tabularx}
    \\begin{document}
    \\color{white}
    """
    _latex_eulog = "\\end{document}"

    def yearcalendar(self):
        self._println(self._latex_prolog)
        for month in range(1,13):
            currmonth = list(self.monthweeks(month))
            weeknumbers, weeklists = zip(*currmonth)
            monthname = datetime.date(self._year, month,1).strftime("%B").decode("latin1")
            self._println('\\newpage\\pagecolor{black}\\color{white}')
            self._println('')
            self._println('')
            self._println('\\centering{\\fontsize{2.5cm}{1.2em}\\selectfont '+monthname+'\\vfill}')
            self._println('')
            self._println('')
            self._println('\\fontsize{0.75cm}{1em}\\selectfont')
            self._println('\\rowcolors{3}{lightgray}{white}')
            self._println('\\begin{tabularx}{\\textwidth}' + '{>{\\fontsize{0.4cm}{1em}\\selectfont}r<{\\fontsize{1cm}{1em}\\selectfont}@{\\hspace{1cm}}*{6}{X}}')
            self._println('\\hiderowcolors&'+ '&'.join([str(w) for w in weeknumbers]) + '\\\\[1em]')
            self._print('\\showrowcolors')
            for day, dayopt in enumerate(_weekdays):
                self._print('{\\color{white}\\cellcolor{black}'+locale.nl_langinfo(dayopt) + '} & ')
                self._println(" & ".join(['{\\color{black}'+str(w[day].day)+'}' for w in weeklists]) + '\\\\')
            self._println('\\end{tabularx}')

        self._println(self._latex_eulog)


if __name__ == "__main__":
    locale.setlocale(locale.LC_ALL, "de_DE")
    isoyearcalendar(2015).yearcalendar()
