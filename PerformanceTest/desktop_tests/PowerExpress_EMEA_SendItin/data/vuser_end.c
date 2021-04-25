vuser_end()
{

	lr_think_time(13);

	ctrx_sync_on_window("Power Express V18.10.63.0  [SVCSYEXTEST34 in TEST]", ACTIVATE, 0, 0, 1029, 756, "snapshot146", CTRX_LAST);

	ctrx_mouse_click(12, 12, LEFT_BUTTON, 0, "Power Express V18.10.63.0  [SVCSYEXTEST34 in TEST]=snapshot147", CTRX_LAST);

	ctrx_sync_on_window("3_21_147_130", CREATE, 3, 21, 147, 130, "snapshot148", CTRX_LAST);

	ctrx_mouse_click(52, 131, LEFT_BUTTON, 0, "Power Express V18.10.63.0  [SVCSYEXTEST34 in TEST]=snapshot149", CTRX_LAST);

	ctrx_sync_on_window("Shell_TrayWnd", CREATE, -2, 724, 1285, 47, "snapshot150", CTRX_LAST);

	ctrx_mouse_click(140, 8, LEFT_BUTTON, 0, "Shell_TrayWnd=snapshot152", CTRX_LAST);

	ctrx_sync_on_window("HKGWL2102 - Amadeus Selling Platform Connect - Google Chrome", ACTIVATE, 14, 14, 1051, 705, "snapshot153", CTRX_LAST);

	ctrx_mouse_click(1022, 152, LEFT_BUTTON, 0, "HKGWL2102 - Amadeus Selling Platform Connect - Google Chrome=snapshot155", CTRX_LAST);

	ctrx_mouse_click(524, 449, LEFT_BUTTON, 0, "HKGWL2102 - Amadeus Selling Platform Connect - Google Chrome=snapshot157", CTRX_LAST);

	lr_think_time(6);

	ctrx_mouse_click(1026, 10, LEFT_BUTTON, 0, "Amadeus Selling Platform Connect - Google Chrome=snapshot158", CTRX_LAST);

	ctrx_sync_on_window("Start", ACTIVATE, 2, 728, 53, 39, "snapshot159", CTRX_LAST);

	ctrx_mouse_click(39, 13, LEFT_BUTTON, 0, "Start=snapshot160", CTRX_LAST);

	ctrx_sync_on_window("Start menu", ACTIVATE, 0, 268, 406, 457, "snapshot161", CTRX_LAST);

	ctrx_mouse_click(273, 433, LEFT_BUTTON, 0, "Start menu=snapshot163", CTRX_LAST);

	lr_think_time(14);

	ctrx_mouse_click(285, 432, LEFT_BUTTON, 0, "Start menu=snapshot164", CTRX_LAST);

	ctrx_logoff(CTRX_NORMAL_LOGOFF, CTRX_LAST);

	web_add_cookie("CtxsDesktopAutoLaunchDone=no; DOMAIN=emea.cwtdesktop.pilot.int.carlsonwagonlit.com");

	web_add_header("Csrf-Token", 
		"B28F8D77DE489D789A2C266CDDE17BB7");

	web_add_header("X-Citrix-IsUsingHTTPS", 
		"Yes");

	web_add_header("X-Requested-With", 
		"XMLHttpRequest");

	lr_think_time(6);

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

	return 0;
}