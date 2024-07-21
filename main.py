from resources.QuakeLog import QuakeLog

formated_data = QuakeLog()

file = formated_data.read_file('./data/qltest.log')

file = formated_data.extract_informations(file)

print(file)