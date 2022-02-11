from datetime import datetime


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

midl_actv_mesg = {
    'signal_type': 'active',
    'data': {
        't': datetime.now().strftime('%Y%m%dT%H:%M:%S'),
    }
}

frnt_conn_init = {
    'signal_type': 'init',
    'data': {
        'dep': 'frnt'
    }
}

dscd_conn_init = {
    'signal_type': 'init',
    'data': {
        'dep': 'dscd'
    }
}


# RESPONSE
actv_conn_stat = {
    'signal_type': 'active_log',
    'status': 'normal'
}

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

midl_actv_resp = {
    'signal_type': 'ping_resp',
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