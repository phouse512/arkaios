def parseFileName(quarter, week):
	if(quarter[:1] == 's'):
		wholeQuarter = "spring_20%s" % quarter[1:]
	elif(quarter[:1] == 'w'):
		wholeQuarter = "winter_20%s" % quarter[1:]
	else:
		wholeQuarter = "fall_20%s" % quarter[1:]

	return '%s_week_%s.csv' % (wholeQuarter, str(week))

def searchConstruction(inputDict):
	sql = []
	for key in inputDict:
		if inputDict[key]:
			sql.append("Attendee.{}.like('%{}%')".format(str(key), inputDict[key]))

	return 'and_(%s)' % ", ".join(sql)