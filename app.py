from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
app = Flask(__name__)

@app.route("/")
def main():
    return render_template('index.html')
	
@app.route('/showAdd')
def showAdd():
    return render_template('add.html')

@app.route("/events")
def events():
    return "Events"
 
@app.route("/events/<string:name>/")
def getEvent(name):
    return name

@app.route("/showEdit/<string:name>/")
def edit(name):
    return render_template(
        'edit.html',name=name)

if __name__ == "__main__":
    app.run()

import datetime, calendar

class RecurringEvent:
	
	FEDERAL_HOLIDAYS = [datetime.date(2017,1,1),datetime.date(2018,1,1),datetime.date(2019,1,1),datetime.date(2020,1,1),datetime.date(2021,1,1),
	datetime.date(2017,1,16),datetime.date(2018,1,15),datetime.date(2019,1,21),datetime.date(2020,1,20),datetime.date(2021,1,18),
	datetime.date(2017,2,20),datetime.date(2018,2,19),datetime.date(2019,2,18),datetime.date(2020,2,17),datetime.date(2021,2,15),
	datetime.date(2017,5,29),datetime.date(2018,5,28),datetime.date(2019,5,27),datetime.date(2020,5,25),datetime.date(2021,5,31),
	datetime.date(2017,7,4),datetime.date(2018,7,4),datetime.date(2019,7,4),datetime.date(2020,7,4),datetime.date(2021,7,4),
	datetime.date(2017,9,4),datetime.date(2018,9,3),datetime.date(2019,9,2),datetime.date(2020,9,7),datetime.date(2021,9,6),
	datetime.date(2017,10,9),datetime.date(2018,10,8),datetime.date(2019,10,14),datetime.date(2020,10,12),datetime.date(2021,10,11),
	datetime.date(2017,11,11),datetime.date(2018,11,11),datetime.date(2019,11,11),datetime.date(2020,11,11),datetime.date(2021,11,11),
	datetime.date(2017,11,23),datetime.date(2018,11,22),datetime.date(2019,11,28),datetime.date(2020,11,26),datetime.date(2021,11,25),
	datetime.date(2017,12,25),datetime.date(2018,12,25),datetime.date(2019,12,25),datetime.date(2020,12,25),datetime.date(2021,12,25)]

	def __init__(self, name, start_date, no_months, day_of_month):
		self.name = name
		self.start_date = start_date
		self.no_months = no_months
		self.day_of_month = day_of_month

	def displayNextFourEvents(self):
		delivery_dates = []
		tempDate = datetime.date(self.start_date.year, self.start_date.month, self.day_of_month)
		if self.day_of_month >= self.start_date.day:
		  tempDate = self.addMonths(tempDate,1)
		while(len(delivery_dates)<4):
		  nextDate = self.nextDeliveryDate(tempDate)
		  if nextDate >= self.start_date:
		    delivery_dates.append(nextDate)
			tempDate = self.addMonths(tempDate,self.no_months)
		  else:
		    tempDate = self.addMonths(tempDate,1)
		return delivery_dates

	def nextDeliveryDate(self, target_date):
		delivery_date = target_date
		while ( delivery_date.isoweekday() > 5 or delivery_date in self.FEDERAL_HOLIDAYS):
			delivery_date -= datetime.timedelta(days=1)
		return delivery_date
		
	def addMonths(self, sourcedate, months):
	  month = sourcedate.month - 1 + months
	  year = int(sourcedate.year + month / 12 )
	  month = month % 12 + 1
	  day = min(sourcedate.day,calendar.monthrange(year,month)[1])
	  return datetime.date(year,month,day)

import unittest
# from app import RecurringEvent
 
class TestUM(unittest.TestCase):
 
    def setUp(self):
      re1 = RecurringEvent("test1", datetime.date(2018,1,13), 3, 15)
      re2 = RecurringEvent("test1", datetime.date(2017,11,15), 3, 10)
      re3 = RecurringEvent("test1", datetime.date(2019,1,10), 3, 15)
 
    def test_startDateAfterDeliveryDate(self):
        self.assertEqual( set(re1.displayNextFourEvents()), set([datetime.date(2018, 2, 15), datetime.date(2018, 3, 15), datetime.date(2018, 4, 13), datetime.date(2018, 5, 15)]))
 
    def test_startDateAfterTarget(self):
        self.assertEqual( set(re2.displayNextFourEvents()), set([datetime.date(2017, 12, 8), datetime.date(2018, 1, 10), datetime.date(2018, 2, 9), datetime.date(2018, 3, 9)]))
 
    def test_startDateBeforeDelivery(self):
        self.assertEqual( set(re3.displayNextFourEvents()), set([datetime.date(2019, 2, 15), datetime.date(2019, 3, 15), datetime.date(2019, 4, 15), datetime.date(2019, 5, 15)]))
 
if __name__ == '__main__':
    unittest.main()