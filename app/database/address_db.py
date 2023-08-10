from ..exceptions import AddressNotFountException

def get_addresses(conn, user_id):
    results = conn.execute('select * from address where user_id = ?', (str(user_id))).fetchall()
    results = [dict(row) for row in results]
    return results

def create_address(conn, address, user_id):
    conn.execute('insert into address (address_line_1, city, state, pin, user_id) values (?, ?, ?, ?, ?)',
                 (address.address_line_1, address.city, address.state, address.pin, str(user_id)))
    

def get_address(conn, id):
    result = conn.execute('select * from address where id = ?',(str(id))).fetchone()

    if result is None:
        raise AddressNotFountException(f'Address with Id [{id}] not found in database', 404)
    return dict(result)

def update_address(conn, id, address):
    conn.execute('update address set address_line_1 = ? , city = ?, state = ?, pin = ? where id = ?', (address.address_line_1, address.city, address.state, address.pin, str(id)))

def delete_address(conn, id):
    conn.execute('delete from address where id = ?',(str(id)))