import sqlite3

# conn = sqlite3.connect('settings.db')
# c = conn.cursor()

# def DB(name, location):
	
# 	data = (name, location)
# 	table = name

# 	try:
# 		# Create table if it doesn't exist
# 		c.execute('''CREATE TABLE %s (name text, location text)''' % table)
# 		print('Table does not exist, creating and adding data...')
# 		# Insert name and location into database
# 		c.execute("INSERT INTO " + table + " VALUES (?, ?)", data)
# 		conn.commit()
# 	except:
# 		print('Table already exists, adding data...')
# 		# Insert name and location into database
# 		c.execute("INSERT INTO " + table + " VALUES (?, ?)", data)
# 		conn.commit()

# 	for row in c.execute('SELECT location FROM %s ORDER BY name' % table):
# 		print(row)


# for rows in c.execute("""SELECT * FROM Sources"""):
# 	print(rows[0])

# conn.close()


conn = sqlite3.connect('database.db')

cursor = conn.cursor()

cursor.execute('''CREATE TABLE Sources (Name text PRIMARY KEY, Location text)''')
result = c.fetchall()

conn.commit()    
cursor.close()
conn.close()


#DB('Fuck', 'Yeah')