/* -------------------------------------------------------------------------------
	Script Title       : 
	Script Description : 
                        
                        
	Recorder Version   : 911
   ------------------------------------------------------------------------------- */

vuser_init()
{

	web_set_sockets_option("SSL_VERSION", "2&3");

	web_url("InternalWeb", 
		"URL=https://apac.cwtdesktop.uat.int.carlsonwagonlit.com/Citrix/InternalWeb/", 
		"Resource=0", 
		"RecContentType=text/html", 
		"Referer=", 
		"Snapshot=t1.inf", 
		"Mode=HTML", 
		EXTRARES, 
		"Url=receiver/js/external/velocity.min_B218502A82F66680.js", ENDITEM, 
		"Url=receiver/css/ctxs.large-ui.min_62D11B01D15101DA.css", ENDITEM, 
		"Url=custom/style.css", ENDITEM, 
		"Url=receiver/images/1x/actionSprite_531B7A6FF85CA98E.png", ENDITEM, 
		"Url=receiver/images/1x/folder_template_C13BB96DEBC9F30F.png", ENDITEM, 
		"Url=https://www.bing.com/favicon.ico", "Referer=", ENDITEM, 
		"Url=receiver/images/1x/CitrixReceiver_WebScreen_CBE548FB8FEE049E.png", ENDITEM, 
		"Url=receiver/images/common/ReceiverFullScreenBackground_46E559C0E6B5A27B.jpg", ENDITEM, 
		"Url=receiver/js/external/slick.min_FEB62CC230E2BA2A.js", ENDITEM, 
		"Url=receiver/js/ctxs.core.min_33B1CC992A07D57E.js", ENDITEM, 
		"Url=receiver/js/ctxs.webui.min_91463D1B79731411.js", ENDITEM, 
		"Url=receiver/js/external/hammer.v2.0.8.min_F699A1E56189259A.js", ENDITEM, 
		"Url=receiver/js/external/jquery.dotdotdot.min_08EE54CBA886AD0A.js", ENDITEM, 
		"Url=custom/script.js", ENDITEM, 
		"Url=custom/strings.en.js", ENDITEM, 
		"Url=receiver/images/1x/viewSprite_B2F322BDCB824FAF.png", ENDITEM, 
		"Url=receiver/images/common/authspinner_B0BCD339560CA593.gif", ENDITEM, 
		"Url=receiver/images/1x/CitrixStoreFront_auth_14B96BFF2B0A6FF8.png", ENDITEM, 
		"Url=receiver/images/1x/spinner_white_auth_button_53FD5A337A529DA7.gif", ENDITEM, 
		"Url=receiver/images/common/icon_loading_9A0623127A028FEB.png", ENDITEM, 
		"Url=receiver/images/1x/CitrixReceiverLogo_Home_5C24BCEC5A182425.png", ENDITEM, 
		"Url=receiver/images/1x/search_close_BC5A22358E58905F.png", ENDITEM, 
		"Url=receiver/images/1x/spinner_5CF0D1C8A76AAC8E.png", ENDITEM, 
		"Url=receiver/images/1x/ico_search_E84E3D63D821F80D.png", ENDITEM, 
		"Url=Resources/Icon/L0NpdHJpeC9JbnRlcm5hbC9yZXNvdXJjZXMvdjIvTTNkT01VZE5Sa1YwVDBkMGEwTnJZVEkzY2xoMGJrTjJRMWRTVDFsU2RUaFdTVlZCVFdaU1ZsUmlkejAtL2ltYWdl?size=128", ENDITEM, 
		"Url=receiver/images/1x/ico_desktop_ready_482FD91B201F2A55.png", ENDITEM, 
		LAST);

	web_add_auto_header("X-Citrix-IsUsingHTTPS", 
		"Yes");

	web_add_auto_header("X-Requested-With", 
		"XMLHttpRequest");

	web_custom_request("Configuration", 
		"URL=https://apac.cwtdesktop.uat.int.carlsonwagonlit.com/Citrix/InternalWeb/Home/Configuration", 
		"Method=POST", 
		"Resource=0", 
		"RecContentType=application/xml", 
		"Referer=https://apac.cwtdesktop.uat.int.carlsonwagonlit.com/Citrix/InternalWeb/", 
		"Snapshot=t2.inf", 
		"Mode=HTML", 
		"EncType=", 
		LAST);

	web_add_cookie("CtxsPluginAssistantState=Done; DOMAIN=apac.cwtdesktop.uat.int.carlsonwagonlit.com");

	web_add_auto_header("Csrf-Token", 
		"9D80BF732A2A03FDA92A705B86EE7FEE");

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

	web_add_cookie("SRCHD=AF=NOFORM; DOMAIN=iecvlist.microsoft.com");

	web_add_cookie("SRCHUID=V=2&GUID=CB1590A5828343A982D2036A09337303&dmnchg=1; DOMAIN=iecvlist.microsoft.com");

	web_add_cookie("SRCHUSR=DOB=20181114; DOMAIN=iecvlist.microsoft.com");

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
		"Url=https://iecvlist.microsoft.com/IE11/1479242656000/iecompatviewlist.xml", "Referer=", ENDITEM, 
		LAST);

	web_submit_data("LoginAttempt", 
		"Action=https://apac.cwtdesktop.uat.int.carlsonwagonlit.com/Citrix/InternalWeb/ExplicitAuth/LoginAttempt", 
		"Method=POST", 
		"RecContentType=application/xml", 
		"Referer=https://apac.cwtdesktop.uat.int.carlsonwagonlit.com/Citrix/InternalWeb/", 
		"Snapshot=t6.inf", 
		"Mode=HTML", 
		ITEMDATA, 
		"Name=username", "Value=SvcSyExTest30", ENDITEM, 
		"Name=password", "Value=$y7xtester", ENDITEM, 
		"Name=saveCredentials", "Value=false", ENDITEM, 
		"Name=domain", "Value=CWT", ENDITEM, 
		"Name=loginBtn", "Value=Log On", ENDITEM, 
		"Name=StateContext", "Value=", ENDITEM, 
		LAST);

	web_submit_data("List_2", 
		"Action=https://apac.cwtdesktop.uat.int.carlsonwagonlit.com/Citrix/InternalWeb/Resources/List", 
		"Method=POST", 
		"RecContentType=application/json", 
		"Referer=https://apac.cwtdesktop.uat.int.carlsonwagonlit.com/Citrix/InternalWeb/", 
		"Snapshot=t7.inf", 
		"Mode=HTML", 
		ITEMDATA, 
		"Name=format", "Value=json", ENDITEM, 
		"Name=resourceDetails", "Value=Default", ENDITEM, 
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

	web_add_cookie("SRCHD=AF=NOFORM; DOMAIN=ieonline.microsoft.com");

	web_add_cookie("SRCHUID=V=2&GUID=CB1590A5828343A982D2036A09337303&dmnchg=1; DOMAIN=ieonline.microsoft.com");

	web_add_cookie("SRCHUSR=DOB=20181114; DOMAIN=ieonline.microsoft.com");

	web_custom_request("AllowSelfServiceAccountManagement", 
		"URL=https://apac.cwtdesktop.uat.int.carlsonwagonlit.com/Citrix/InternalWeb/ExplicitAuth/AllowSelfServiceAccountManagement", 
		"Method=POST", 
		"Resource=0", 
		"RecContentType=application/xml", 
		"Referer=https://apac.cwtdesktop.uat.int.carlsonwagonlit.com/Citrix/InternalWeb/", 
		"Snapshot=t9.inf", 
		"Mode=HTML", 
		"EncType=", 
		EXTRARES, 
		"Url=https://ieonline.microsoft.com/iedomainsuggestions/ie11/suggestions.en-US", "Referer=", ENDITEM, 
		LAST);

	ctrx_nfuse_connect("https://apac.cwtdesktop.uat.int.carlsonwagonlit.com/Citrix/InternalWeb/Resources/LaunchIca/RGVmYXVsdEFnZ3JlZ2F0aW9uR3JvdXAuXEFQQUMgTG9hZCBUZXN0aW5n.ica?CsrfToken=9D80BF732A2A03FDA92A705B86EE7FEE&IsUsingHttps=Yes&displayNameDesktopTitle=APAC%20Load%20Testing&launchId=1548145663063", CTRX_LAST);

	ctrx_wait_for_event("LOGON", CTRX_LAST);

	ctrx_logoff(CTRX_NORMAL_LOGOFF, CTRX_LAST);

	web_add_cookie("CtxsDesktopAutoLaunchDone=no; DOMAIN=apac.cwtdesktop.uat.int.carlsonwagonlit.com");

	lr_think_time(7);

	web_custom_request("Logoff", 
		"URL=https://apac.cwtdesktop.uat.int.carlsonwagonlit.com/Citrix/InternalWeb/Authentication/Logoff", 
		"Method=POST", 
		"Resource=0", 
		"RecContentType=text/plain", 
		"Referer=https://apac.cwtdesktop.uat.int.carlsonwagonlit.com/Citrix/InternalWeb/", 
		"Snapshot=t10.inf", 
		"Mode=HTML", 
		"EncType=", 
		LAST);

	return 0;
}