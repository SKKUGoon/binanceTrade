# SENDING
back_conn_init = {
    'signal_type': 'init',
    'data': {
        'dep': 'back',
        'dep_sep': 'conn'
    }
}

back_data_init = {
    'signal_type': 'init',
    'data': {
        'dep': 'back',
        'dep_sep': 'dbms'
    }
}

back_test_init = {
    'signal_type': 'init',
    'data': {
        'dep': 'back',
        'dep_sep': 'test'
    }
}

midl_conn_init = {
    'signal_type': 'init',
    'data': {
        'dep': 'midl'
    }
}

frnt_conn_init = {
    'signal_type': 'init',
    'data': {
        'dep': 'frnt'
    }
}


# RESPONSE
# BACKOFFICE RESPONSE
# CONNECTION RESPONSE
back_conn_resp = {
    'signal_type': 'conn_resp',
    'data': {
        'status': 'normal',
        'msg': 'connection_normal'
    }
}

# DATABASE RESPONSE
back_data_resp = {
    'signal_type': 'data_resp',
    'data': {
        'status': 'normal',
        'msg': 'database_normal'
    }
}

# TEST ORDER RESPONSE
back_test_resp = {
    'signal_type': 'test_resp',
    'data': {
        'status': 'normal',
        'msg': 'trade_test_normal'
    }
}

# MIDDLEOFFICE RESPONSE
midl_trde_resp = {
    'signal_type': 'trade_resp',
    'data': {
        'status': 'recieved',
        'msg': 'successfully recieved'
    }
}

# FRONTOFFICE RESPONSE
frnt_trde_resp = {
    'signal_type': 'trade_resp',
    'data': {
        'status': 'executed',
        'msg': 'successfully executed.'
    }
}