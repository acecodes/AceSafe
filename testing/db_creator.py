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


def define_path():

	# Connect to the database and establish a cursor
	conn = sqlite3.connect('settings.db')
	cursor = conn.cursor()

	# View table
	cursor.execute('SELECT * FROM Sources')
	# Convert table to dictionary
	Table = dict(cursor.fetchall())
	# Create path variable from matching object name in table
	name = Table['Flashcards']

	# Commit and close connection to database
	conn.commit()    
	cursor.close()
	conn.close()

	return name

# def backup_loop(self, name, table, dst_sub=''):

#     # Connect to the database and establish a cursor
#     conn = sqlite3.connect('settings.db')
#     cursor = conn.cursor()

#     # View table
#     cursor.execute('SELECT * FROM {0}'.format(table))
#     # Convert table to dictionary
#     Table = dict(cursor.fetchall())

#     # Commit and close connection to database
#     conn.commit()    
#     cursor.close()
#     conn.close()

#     self.copy_warn(name)

#     if dst_sub != '':
#         for directory in db:
#             #self.copy_dirs(db[directory], dst_sub=dst_sub)
#             print(directory)
#     self.finished


conn = sqlite3.connect('settings.db')
cursor = conn.cursor()

# View table
cursor.execute('SELECT * FROM Sources')
# Convert table to dictionary
Table = cursor.fetchall()

# Commit and close connection to database
conn.commit()    
cursor.close()
conn.close()

for name, directory in Table:
    print(name)

def test_func(a, b, c=1, d=3, e=2):
	return a + b * c - d ** e

def test_func2(func, **args):
	return func(**args)

print(test_func2(test_func, a=1, b=2))