vuser_init()
{

	web_cleanup_cookies();
	web_set_max_html_param_len("99999");
	web_set_sockets_option("SSL_VERSION", "TLS1.2");
	
	web_url("PilotWeb", 
		"URL=https://apac.cwtdesktop.uat.int.carlsonwagonlit.com/Citrix/InternalWeb/", 
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
		"URL=https://apac.cwtdesktop.uat.int.carlsonwagonlit.com/Citrix/InternalWeb/Home/Configuration", 
		"Method=POST", 
		"Resource=0", 
		"RecContentType=application/xml", 
		"Referer=https://apac.cwtdesktop.uat.int.carlsonwagonlit.com/Citrix/InternalWeb/", 
		"Snapshot=t2.inf", 
		"Mode=HTML", 
		"EncType=", 
		EXTRARES, 
		LAST);

	web_add_auto_header("Csrf-Token",
		"{CsrfToken}");
	
	lr_start_transaction("Citrix_LoginPage");

	web_submit_data("List", 
		"Action=https://apac.cwtdesktop.uat.int.carlsonwagonlit.com/Citrix/InternalWeb/Resources/List", 
		"Method=POST", 
		"RecContentType=text/plain", 
		"Referer=https://apac.cwtdesktop.uat.int.carlsonwagonlit.com/Citrix/InternalWeb/", 
		"Snapshot=t3.inf", 
		"Mode=HTML", 
		ITEMDATA, 
		"Name=format", "Value=json", ENDITEM, 
		"Name=resourceDetails", "Value=Default", ENDITEM, 
		LAST);

	web_custom_request("GetAuthMethods", 
		"URL=https://apac.cwtdesktop.uat.int.carlsonwagonlit.com/Citrix/InternalWeb/Authentication/GetAuthMethods", 
		"Method=POST", 
		"Resource=0", 
		"RecContentType=application/xml", 
		"Referer=https://apac.cwtdesktop.uat.int.carlsonwagonlit.com/Citrix/InternalWeb/", 
		"Snapshot=t4.inf", 
		"Mode=HTML", 
		"EncType=", 
		LAST);

	web_custom_request("Login", 
		"URL=https://apac.cwtdesktop.uat.int.carlsonwagonlit.com/Citrix/InternalWeb/ExplicitAuth/Login", 
		"Method=POST", 
		"Resource=0", 
		"RecContentType=application/vnd.citrix.authenticateresponse-1+xml", 
		"Referer=https://apac.cwtdesktop.uat.int.carlsonwagonlit.com/Citrix/InternalWeb/", 
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
		"Action=https://apac.cwtdesktop.uat.int.carlsonwagonlit.com/Citrix/InternalWeb/ExplicitAuth/LoginAttempt", 
		"Method=POST", 
		"RecContentType=application/xml", 
		"Referer=https://apac.cwtdesktop.uat.int.carlsonwagonlit.com/Citrix/InternalWeb/", 
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
		"URL=https://apac.cwtdesktop.uat.int.carlsonwagonlit.com/Citrix/InternalWeb/Authentication/GetUserName", 
		"Method=POST", 
		"Resource=0", 
		"Referer=https://apac.cwtdesktop.uat.int.carlsonwagonlit.com/Citrix/InternalWeb/", 
		"Snapshot=t8.inf", 
		"Mode=HTML", 
		"EncType=", 
		LAST);

	web_custom_request("AllowSelfServiceAccountManagement", 
		"URL=https://apac.cwtdesktop.uat.int.carlsonwagonlit.com/Citrix/InternalWeb/ExplicitAuth/AllowSelfServiceAccountManagement", 
		"Method=POST", 
		"Resource=0", 
		"RecContentType=application/xml", 
		"Referer=https://apac.cwtdesktop.uat.int.carlsonwagonlit.com/Citrix/InternalWeb/", 
		"Snapshot=t9.inf", 
		"Mode=HTML", 
		"EncType=", 
		LAST);

	lr_think_time(2);

	ctrx_nfuse_connect("https://apac.cwtdesktop.uat.int.carlsonwagonlit.com/Citrix/InternalWeb/Resources/LaunchIca/RGVmYXVsdEFnZ3JlZ2F0aW9uR3JvdXAuXEFQQUMgTE9BRCBURVNUSU5H.ica?CsrfToken={CsrfToken}&IsUsingHttps=Yes&displayNameDesktopTitle=APAC%20Load%20Testing&launchId={LaunchID}", CTRX_LAST);
	
	lr_end_transaction("Citrix_Login", LR_AUTO);
	
	ctrx_set_waiting_time(60);

	ctrx_wait_for_event("LOGON", CTRX_LAST);

	return 0;
}