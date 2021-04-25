import shutil
import win32wnet
import os

def covert_unc(host, path):
    """ Convert a file path on a host to a UNC path."""
    return ''.join(['\\\\', host, '\\', path.replace(':', '$')])

def network_connect(host):
    unc_host = ''.join(['\\\\', host])
    try:
        win32wnet.WNetAddConnection2(0, None, unc_host, None, 'cwt\\adm_panganiban', 'Carlson0!%')
    except Exception, err:
        if isinstance(err, win32wnet.error):
            # Disconnect previous connections if detected, and reconnect.
            if err[0] == 1219:
                win32wnet.WNetCancelConnection2(unc_host, 0, 0)
                return wnet_connect(host, 'cwt\\adm_panganiban', 'Carlson0!%')
        raise err

def delete_syex_logs(host):
    path = covert_unc(host, 'd:\\SyEx_Logs')
    for file in os.listdir(path):
    	os.remove(os.path.join(path, file))

def delete_rf_logs(host):
    path = covert_unc(host, 'd:\\test_result')
    for root, dirnames, filenames in os.walk(path):
    	for dir_name in dirnames:
    		shutil.rmtree(os.path.join(path, dir_name))
    	for file in filenames:
	    	os.remove(os.path.join(path, file))

def delete_syex_and_rf_logs(*hosts):
	for host in hosts:
		network_connect(host)
		delete_syex_logs(host)
		delete_rf_logs(host)

if __name__ == '__main__':
	delete_syex_and_rf_logs('vwsng1ir01006', 'vwsng1ir01007', 'vwsng1ir01008')
	# network_connect('vwsng1ir01006')
	# delete_syex_logs('vwsng1ir01006')

