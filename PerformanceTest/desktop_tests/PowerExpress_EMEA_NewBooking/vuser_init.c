vuser_init()
{

	web_cleanup_cookies();
	web_set_max_html_param_len("99999");
	web_set_sockets_option("SSL_VERSION", "TLS1.2");
	
	web_url("PilotWeb", 
		"URL=https://emea.cwtdesktop.pilot.int.carlsonwagonlit.com/Citrix/PilotWeb/", 
		"Resource=0", 
		"RecContentType=text/html", 
		"Referer=", 
		"Snapshot=t1.inf", 
		"Mode=HTML", 
		EXTRARES, 
		LAST);

	web_add_auto_header("X-Citrix-IsUsingHTTPS", 
		"Yes");

	web_add_auto_header("X-Requested-With", 
		"XMLHttpRequest");

	web_reg_save_param_regexp(
		"ParamName=CsrfToken",
		"RegExp=CsrfToken=(.*?);",
		SEARCH_FILTERS,
		"Scope=Cookies",
		"IgnoreRedirections=No",
		"RequestUrl=*/Configuration*",
		LAST);

	web_custom_request("Configuration", 
		"URL=https://emea.cwtdesktop.pilot.int.carlsonwagonlit.com/Citrix/PilotWeb/Home/Configuration", 
		"Method=POST", 
		"Resource=0", 
		"RecContentType=application/xml", 
		"Referer=https://emea.cwtdesktop.pilot.int.carlsonwagonlit.com/Citrix/PilotWeb/", 
		"Snapshot=t2.inf", 
		"Mode=HTML", 
		"EncType=", 
		EXTRARES, 
		LAST);

	web_add_auto_header("Csrf-Token",
		"{CsrfToken}");
	
	lr_start_transaction("Citrix_LoginPage");

	web_submit_data("List", 
		"Action=https://emea.cwtdesktop.pilot.int.carlsonwagonlit.com/Citrix/PilotWeb/Resources/List", 
		"Method=POST", 
		"RecContentType=text/plain", 
		"Referer=https://emea.cwtdesktop.pilot.int.carlsonwagonlit.com/Citrix/PilotWeb/", 
		"Snapshot=t3.inf", 
		"Mode=HTML", 
		ITEMDATA, 
		"Name=format", "Value=json", ENDITEM, 
		"Name=resourceDetails", "Value=Default", ENDITEM, 
		LAST);

	web_custom_request("GetAuthMethods", 
		"URL=https://emea.cwtdesktop.pilot.int.carlsonwagonlit.com/Citrix/PilotWeb/Authentication/GetAuthMethods", 
		"Method=POST", 
		"Resource=0", 
		"RecContentType=application/xml", 
		"Referer=https://emea.cwtdesktop.pilot.int.carlsonwagonlit.com/Citrix/PilotWeb/", 
		"Snapshot=t4.inf", 
		"Mode=HTML", 
		"EncType=", 
		LAST);

	web_custom_request("Login", 
		"URL=https://emea.cwtdesktop.pilot.int.carlsonwagonlit.com/Citrix/PilotWeb/ExplicitAuth/Login", 
		"Method=POST", 
		"Resource=0", 
		"RecContentType=application/vnd.citrix.authenticateresponse-1+xml", 
		"Referer=https://emea.cwtdesktop.pilot.int.carlsonwagonlit.com/Citrix/PilotWeb/", 
		"Snapshot=t5.inf", 
		"Mode=HTML", 
		"EncType=", 
		EXTRARES, 
		LAST);
	
lr_end_transaction("Citrix_LoginPage", LR_AUTO);


//**********************************************************************************
// Login into Citrix Client
//**********************************************************************************

lr_start_transaction("Citrix_Login");

	web_submit_data("LoginAttempt", 
		"Action=https://emea.cwtdesktop.pilot.int.carlsonwagonlit.com/Citrix/PilotWeb/ExplicitAuth/LoginAttempt", 
		"Method=POST", 
		"RecContentType=application/xml", 
		"Referer=https://emea.cwtdesktop.pilot.int.carlsonwagonlit.com/Citrix/PilotWeb/", 
		"Snapshot=t6.inf", 
		"Mode=HTML", 
		ITEMDATA, 
		"Name=username", "Value={CitrixLogin}", ENDITEM,
		"Name=password", "Value=$y7xtester", ENDITEM, 
		"Name=saveCredentials", "Value=false", ENDITEM, 
		"Name=domain", "Value=CWT", ENDITEM, 
		"Name=loginBtn", "Value=Log On", ENDITEM, 
		"Name=StateContext", "Value=", ENDITEM, 
		LAST);
		
	web_custom_request("GetUserName", 
		"URL=https://emea.cwtdesktop.pilot.int.carlsonwagonlit.com/Citrix/PilotWeb/Authentication/GetUserName", 
		"Method=POST", 
		"Resource=0", 
		"Referer=https://emea.cwtdesktop.pilot.int.carlsonwagonlit.com/Citrix/PilotWeb/", 
		"Snapshot=t8.inf", 
		"Mode=HTML", 
		"EncType=", 
		LAST);

	web_custom_request("AllowSelfServiceAccountManagement", 
		"URL=https://emea.cwtdesktop.pilot.int.carlsonwagonlit.com/Citrix/PilotWeb/ExplicitAuth/AllowSelfServiceAccountManagement", 
		"Method=POST", 
		"Resource=0", 
		"RecContentType=application/xml", 
		"Referer=https://emea.cwtdesktop.pilot.int.carlsonwagonlit.com/Citrix/PilotWeb/", 
		"Snapshot=t9.inf", 
		"Mode=HTML", 
		"EncType=", 
		LAST);

	lr_think_time(2);
	
	ctrx_nfuse_connect("https://emea.cwtdesktop.pilot.int.carlsonwagonlit.com/Citrix/PilotWeb/Resources/LaunchIca/RGVmYXVsdEFnZ3JlZ2F0aW9uR3JvdXAuXFNFQ08gUGVyZm9ybWFuY2UgVGVzdGluZw--.ica?CsrfToken={CsrfToken}&IsUsingHttps=Yes&displayNameDesktopTitle=SECO%20Performance%20Testing&launchId={LaunchID}", CTRX_LAST);

	lr_end_transaction("Citrix_Login", LR_AUTO);
	
	ctrx_set_waiting_time(60);

	ctrx_wait_for_event("LOGON", CTRX_LAST);
		
lr_start_transaction("Sellco Login");

	lr_think_time(5);

	ctrx_type("a", CTRX_LAST);
	
	lr_think_time(2);

	ctrx_type("a", CTRX_LAST);

	lr_think_time(2);
	
	ctrx_key("ENTER_KEY", 0, CTRX_LAST);

//	ctrx_key("ESC_KEY", MODIF_CONTROL, "", CTRX_LAST);

//	ctrx_key("NO_KEY", MODIF_CONTROL, "", CTRX_LAST);

//	lr_think_time(5);
	
//	ctrx_type("run", "", CTRX_LAST);
//
//	lr_think_time(2);
//
//	ctrx_key("ENTER_KEY", 0, "", CTRX_LAST);
//
//	lr_think_time(5);
//
//	ctrx_type("chrome https://acceptance.custom.sellingplatformconnect.amadeus.com", "", CTRX_LAST);
//	
//	lr_think_time(3);
//
//	ctrx_key("ENTER_KEY", 0, "", CTRX_LAST);

	lr_think_time(10);

	ctrx_key("a", MODIF_CONTROL, CTRX_LAST);

	lr_think_time(2);

	ctrx_key("BACKSPACE_KEY", 0, CTRX_LAST);

	lr_think_time(2);

	ctrx_type("{GDSLogin}", CTRX_LAST);

	lr_think_time(2);
	
	ctrx_key("TAB_KEY", 0, CTRX_LAST);

	lr_think_time(2);
	
	ctrx_type("su", CTRX_LAST);

	lr_think_time(2);

	ctrx_key("TAB_KEY", 0, CTRX_LAST);

	lr_think_time(2);

	ctrx_type("HKGWL2102", CTRX_LAST);

	lr_think_time(2);

	ctrx_key("TAB_KEY", 0, CTRX_LAST);

	lr_think_time(3);	

	ctrx_type("{GDSPassword}", CTRX_LAST);

	lr_think_time(2);

	ctrx_key("ENTER_KEY", 0, CTRX_LAST);

	lr_think_time(15);

	ctrx_key("ENTER_KEY", 0, CTRX_LAST);
	
	lr_think_time(10);

lr_end_transaction("Sellco Login", LR_AUTO);

	return 0;
}