IP_ADDRESSES = {

	'I':{
		'BASLER': '192.168.1.56',
		'PLC': '192.168.1.55'
	},
	'II':{
		'BASLER': '192.168.1.46',
		'PLC': '192.168.1.45'
	}
}

import snap7
DB_NUMBER = 100
START_ADDRESS = 0
SIZE 259
PLC = snap7.client.Client()
PLC.connect('192.168.1.55', 0, 1)
db = PLC.db_read(DB_NUMBER, START_ADDRESS, SIZE)
productStatus = bool(db[258])
print("productStatus".format(productStatus))