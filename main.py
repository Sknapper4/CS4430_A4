from dbConnector import add_customer, get_highest_id, add_order, remove_order, print_pending_orders, ship_order, restock


def menu():
	print(
		' 1. Add a customer\n',
		'2. Add an order\n',
		'3. Remove an order\n',
		'4. Ship an order\n',
		'5. Print pending orders (not shipped yet) with customer information\n',
		'6. Restock products\n',
		'7. Exit\n'
		)
	menu_choice = input('Please select a task: ')

	if menu_choice == '1':
		add_customer()
		menu()
	
	elif menu_choice == '2':
		add_order()
		menu()
		
	elif menu_choice == '3':
		remove_order()
		menu()
		
	elif menu_choice == '4':
		ship_order()
		menu()
		
	elif menu_choice == '5':
		print_pending_orders()
		menu()
		
	elif menu_choice == '6':
		restock()
		menu()
		
	elif menu_choice == '7':
		print('Goodbye')
	else:
		print('\n\nThat input is not an option.\n')
		menu()


if __name__ == '__main__':
	get_highest_id('orders', 'OrderID')
	menu()
