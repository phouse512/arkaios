def parseFileName(quarter, week):
	if(quarter[:1] == 's'):
		wholeQuarter = "spring_20" + quarter[1:]

	elif(quarter[:1] == 'w'):
		wholeQuarter = "winter_20" + quarter[1:]
	else:
		wholeQuarter = "fall_20" + quarter[1:]

	filename = wholeQuarter + "_week_" + str(week) + ".csv"
	return filename