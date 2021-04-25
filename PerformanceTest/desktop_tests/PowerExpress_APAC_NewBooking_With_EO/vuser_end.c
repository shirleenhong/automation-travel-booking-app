vuser_end()
{

lr_start_transaction("Citrix Logout");

	ctrx_logoff(CTRX_FORCED_LOGOFF, CTRX_LAST);
				
	ctrx_disconnect_server("", CTRX_LAST);

	web_add_header("Csrf-Token",
		"{CsrfToken}");

	web_custom_request("Disconnect", 
		"URL=https://apac.cwtdesktop.uat.int.carlsonwagonlit.com/Citrix/InternalWeb/Sessions/Disconnect", 
		"Method=POST", 
		"Resource=0", 
		"RecContentType=text/plain", 
		"Referer=https://apac.cwtdesktop.uat.int.carlsonwagonlit.com/Citrix/InternalWeb/", 
		"Snapshot=t10.inf", 
		"Mode=HTML", 
		"EncType=", 
		LAST);
	
	web_custom_request("Logoff", 
		"URL=https://emea.cwtdesktop.pilot.int.carlsonwagonlit.com/Citrix/PilotWeb/Authentication/Logoff", 
		"Method=POST", 
		"Resource=0", 
		"RecContentType=text/plain", 
		"Referer=https://emea.cwtdesktop.pilot.int.carlsonwagonlit.com/Citrix/PilotWeb/", 
		"Snapshot=t10.inf", 
		"Mode=HTML", 
		"EncType=", 
		LAST);		

lr_end_transaction("Citrix Logout", LR_AUTO);

	return 0;
}