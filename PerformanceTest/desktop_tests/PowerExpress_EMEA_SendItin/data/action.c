Action()
{

	web_set_sockets_option("SSL_VERSION", "TLS1.2");

	web_url("PilotWeb", 
		"URL=https://emea.cwtdesktop.pilot.int.carlsonwagonlit.com/Citrix/PilotWeb/", 
		"Resource=0", 
		"RecContentType=text/html", 
		"Referer=", 
		"Snapshot=t1.inf", 
		"Mode=HTML", 
		EXTRARES, 
		"Url=receiver/css/ctxs.large-ui.min_62D11B01D15101DA.css", ENDITEM, 
		"Url=receiver/js/external/hammer.v2.0.8.min_F699A1E56189259A.js", ENDITEM, 
		"Url=receiver/js/external/jquery.dotdotdot.min_08EE54CBA886AD0A.js", ENDITEM, 
		"Url=receiver/js/external/velocity.min_B218502A82F66680.js", ENDITEM, 
		"Url=receiver/js/external/slick.min_FEB62CC230E2BA2A.js", ENDITEM, 
		"Url=receiver/js/ctxs.core.min_33B1CC992A07D57E.js", ENDITEM, 
		"Url=custom/style.css", ENDITEM, 
		"Url=receiver/images/1x/actionSprite_531B7A6FF85CA98E.png", ENDITEM, 
		"Url=receiver/js/ctxs.webui.min_91463D1B79731411.js", ENDITEM, 
		"Url=receiver/images/1x/folder_template_C13BB96DEBC9F30F.png", ENDITEM, 
		"Url=receiver/images/1x/CitrixReceiver_WebScreen_CBE548FB8FEE049E.png", ENDITEM, 
		"Url=receiver/images/common/ReceiverFullScreenBackground_46E559C0E6B5A27B.jpg", ENDITEM, 
		"Url=https://www.bing.com/favicon.ico", "Referer=", ENDITEM, 
		"Url=custom/script.js", ENDITEM, 
		"Url=custom/strings.en.js", ENDITEM, 
		"Url=receiver/images/1x/viewSprite_B2F322BDCB824FAF.png", ENDITEM, 
		"Url=receiver/images/common/authspinner_B0BCD339560CA593.gif", ENDITEM, 
		"Url=custom/Citrix_HalfLogonLogo.png", ENDITEM, 
		"Url=receiver/images/1x/spinner_white_auth_button_53FD5A337A529DA7.gif", ENDITEM, 
		"Url=receiver/images/common/icon_loading_9A0623127A028FEB.png", ENDITEM, 
		"Url=receiver/images/1x/search_close_BC5A22358E58905F.png", ENDITEM, 
		"Url=custom/Citrix_HalfHeaderLogo.png", ENDITEM, 
		"Url=receiver/images/1x/spinner_5CF0D1C8A76AAC8E.png", ENDITEM, 
		"Url=receiver/images/1x/ico_search_E84E3D63D821F80D.png", ENDITEM, 
		"Url=Resources/Icon/L0NpdHJpeC9QaWxvdC9yZXNvdXJjZXMvdjIvTTNkT01VZE5Sa1YwVDBkMGEwTnJZVEkzY2xoMGJrTjJRMWRTVDFsU2RUaFdTVlZCVFdaU1ZsUmlkejAtL2ltYWdl?size=128", ENDITEM, 
		"Url=receiver/images/1x/ico_desktop_ready_482FD91B201F2A55.png", ENDITEM, 
		LAST);

	web_add_auto_header("X-Citrix-IsUsingHTTPS", 
		"Yes");

	web_add_auto_header("X-Requested-With", 
		"XMLHttpRequest");

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
		"Url=https://www.bing.com/favicon.ico", "Referer=", ENDITEM, 
		LAST);

	web_add_cookie("CtxsPluginAssistantState=Done; DOMAIN=emea.cwtdesktop.pilot.int.carlsonwagonlit.com");

	web_add_auto_header("Csrf-Token", 
		"B28F8D77DE489D789A2C266CDDE17BB7");

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
		LAST);

	web_submit_data("LoginAttempt", 
		"Action=https://emea.cwtdesktop.pilot.int.carlsonwagonlit.com/Citrix/PilotWeb/ExplicitAuth/LoginAttempt", 
		"Method=POST", 
		"RecContentType=application/xml", 
		"Referer=https://emea.cwtdesktop.pilot.int.carlsonwagonlit.com/Citrix/PilotWeb/", 
		"Snapshot=t6.inf", 
		"Mode=HTML", 
		ITEMDATA, 
		"Name=username", "Value=SvcSyExTest34", ENDITEM, 
		"Name=password", "Value=$y3xtester", ENDITEM, 
		"Name=saveCredentials", "Value=false", ENDITEM, 
		"Name=domain", "Value=CWT", ENDITEM, 
		"Name=loginBtn", "Value=Log On", ENDITEM, 
		"Name=StateContext", "Value=", ENDITEM, 
		LAST);

	web_submit_data("List_2", 
		"Action=https://emea.cwtdesktop.pilot.int.carlsonwagonlit.com/Citrix/PilotWeb/Resources/List", 
		"Method=POST", 
		"RecContentType=application/json", 
		"Referer=https://emea.cwtdesktop.pilot.int.carlsonwagonlit.com/Citrix/PilotWeb/", 
		"Snapshot=t7.inf", 
		"Mode=HTML", 
		ITEMDATA, 
		"Name=format", "Value=json", ENDITEM, 
		"Name=resourceDetails", "Value=Default", ENDITEM, 
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

	ctrx_nfuse_connect("https://emea.cwtdesktop.pilot.int.carlsonwagonlit.com/Citrix/PilotWeb/Resources/LaunchIca/RGVmYXVsdEFnZ3JlZ2F0aW9uR3JvdXAuXFNFQ08gUGVyZm9ybWFuY2UgVGVzdGluZw--.ica?CsrfToken=B28F8D77DE489D789A2C266CDDE17BB7&IsUsingHttps=Yes&displayNameDesktopTitle=SECO%20Performance%20Testing&launchId=1538590216331", CTRX_LAST);

	ctrx_wait_for_event("LOGON", CTRX_LAST);

	lr_think_time(24);

	lr_start_transaction("Login_Amadeus");

	ctrx_sync_on_window("Desktop", ACTIVATE, 0, 0, 1281, 769, "snapshot1", CTRX_LAST);

	ctrx_mouse_double_click(44, 135, LEFT_BUTTON, 0, "Desktop=snapshot2", CTRX_LAST);

	lr_think_time(8);

	ctrx_sync_on_window("Amadeus Selling Platform Connect - Google Chrome", ACTIVATE, 14, 14, 1051, 705, "snapshot3", CTRX_LAST);

	ctrx_mouse_click(181, 375, LEFT_BUTTON, 0, "Amadeus Selling Platform Connect - Google Chrome=snapshot4", CTRX_LAST);

	ctrx_type("TEST01", "", CTRX_LAST);

	ctrx_mouse_click(331, 381, LEFT_BUTTON, 0, "Amadeus Selling Platform Connect - Google Chrome=snapshot7", CTRX_LAST);

	ctrx_mouse_click(318, 435, LEFT_BUTTON, 0, "Amadeus Selling Platform Connect - Google Chrome=snapshot8", CTRX_LAST);

	ctrx_mouse_click(193, 399, LEFT_BUTTON, 0, "Amadeus Selling Platform Connect - Google Chrome=snapshot9", CTRX_LAST);

	ctrx_type("HKGWL2012", "", CTRX_LAST);

	lr_think_time(4);

	ctrx_mouse_click(253, 431, LEFT_BUTTON, 0, "Amadeus Selling Platform Connect - Google Chrome=snapshot11", CTRX_LAST);

	ctrx_type("C@rlson123", "", CTRX_LAST);

	lr_think_time(10);

	ctrx_mouse_click(184, 472, LEFT_BUTTON, 0, "Amadeus Selling Platform Connect - Google Chrome=snapshot15", CTRX_LAST);

	ctrx_key("ENTER_KEY", 0, "", CTRX_LAST);

	lr_think_time(5);

	ctrx_mouse_click(175, 498, LEFT_BUTTON, 0, "Amadeus Selling Platform Connect - Google Chrome=snapshot17", CTRX_LAST);

	lr_think_time(15);

	ctrx_key("BACKSPACE_KEY", 0, "", CTRX_LAST);

	ctrx_type("8", "", CTRX_LAST);

	ctrx_key("TAB_KEY", 0, "", CTRX_LAST);

	ctrx_key("TAB_KEY", 0, "", CTRX_LAST);

	ctrx_key("TAB_KEY", 0, "", CTRX_LAST);

	ctrx_type("C@rlson123", "", CTRX_LAST);

	ctrx_key("ENTER_KEY", 0, "", CTRX_LAST);

	lr_think_time(13);

	ctrx_mouse_click(243, 417, LEFT_BUTTON, 0, "Amadeus Selling Platform Connect - Google Chrome=snapshot26", CTRX_LAST);

	ctrx_key("RIGHT_ARROW_KEY", 0, "", CTRX_LAST);

	ctrx_key("BACKSPACE_KEY", 0, "", CTRX_LAST);

	ctrx_key("BACKSPACE_KEY", 0, "", CTRX_LAST);

	ctrx_key("BACKSPACE_KEY", 0, "", CTRX_LAST);

	ctrx_key("BACKSPACE_KEY", 0, "", CTRX_LAST);

	ctrx_key("RIGHT_ARROW_KEY", 0, "", CTRX_LAST);

	ctrx_key("RIGHT_ARROW_KEY", 0, "", CTRX_LAST);

	ctrx_key("RIGHT_ARROW_KEY", 0, "", CTRX_LAST);

	ctrx_mouse_click(243, 417, LEFT_BUTTON, 0, "Amadeus Selling Platform Connect - Google Chrome=snapshot35", CTRX_LAST);

	ctrx_mouse_click(266, 418, LEFT_BUTTON, 0, "Amadeus Selling Platform Connect - Google Chrome=snapshot36", CTRX_LAST);

	ctrx_mouse_double_click(266, 418, LEFT_BUTTON, 0, "Amadeus Selling Platform Connect - Google Chrome=snapshot37", CTRX_LAST);

	ctrx_mouse_up(108, 414, LEFT_BUTTON, 0, "Amadeus Selling Platform Connect - Google Chrome=snapshot39", CTRX_LAST);

	ctrx_key("DELETE_KEY", 0, "", CTRX_LAST);

	ctrx_key("DELETE_KEY", 0, "", CTRX_LAST);

	ctrx_mouse_click(276, 422, LEFT_BUTTON, 0, "Amadeus Selling Platform Connect - Google Chrome=snapshot43", CTRX_LAST);

	ctrx_key("BACKSPACE_KEY", 0, "", CTRX_LAST);

	ctrx_key("BACKSPACE_KEY", 0, "", CTRX_LAST);

	ctrx_mouse_click(276, 422, LEFT_BUTTON, 0, "Amadeus Selling Platform Connect - Google Chrome=snapshot46", CTRX_LAST);

	ctrx_mouse_click(300, 415, LEFT_BUTTON, 0, "Amadeus Selling Platform Connect - Google Chrome=snapshot48", CTRX_LAST);

	ctrx_mouse_click(228, 417, LEFT_BUTTON, 0, "Amadeus Selling Platform Connect - Google Chrome=snapshot50", CTRX_LAST);

	ctrx_type("HKW", "", CTRX_LAST);

	ctrx_key("BACKSPACE_KEY", 0, "", CTRX_LAST);

	ctrx_type("WL", "", CTRX_LAST);

	ctrx_key("BACKSPACE_KEY", 0, "", CTRX_LAST);

	ctrx_key("BACKSPACE_KEY", 0, "", CTRX_LAST);

	ctrx_key("BACKSPACE_KEY", 0, "", CTRX_LAST);

	ctrx_type("KWL2102", "", CTRX_LAST);

	ctrx_key("RIGHT_ARROW_KEY", 0, "", CTRX_LAST);

	ctrx_key("RIGHT_ARROW_KEY", 0, "", CTRX_LAST);

	ctrx_key("RIGHT_ARROW_KEY", 0, "", CTRX_LAST);

	ctrx_type("   ", "", CTRX_LAST);

	ctrx_key("DELETE_KEY", 0, "", CTRX_LAST);

	ctrx_key("BACKSPACE_KEY", 0, "", CTRX_LAST);

	ctrx_mouse_click(253, 460, LEFT_BUTTON, 0, "Amadeus Selling Platform Connect - Google Chrome=snapshot68", CTRX_LAST);

	ctrx_mouse_click(210, 446, LEFT_BUTTON, 0, "Amadeus Selling Platform Connect - Google Chrome=snapshot70", CTRX_LAST);

	lr_think_time(11);

	ctrx_mouse_click(210, 446, LEFT_BUTTON, 0, "Amadeus Selling Platform Connect - Google Chrome=snapshot74", CTRX_LAST);

	lr_think_time(11);

	ctrx_mouse_click(210, 446, LEFT_BUTTON, 0, "Amadeus Selling Platform Connect - Google Chrome=snapshot78", CTRX_LAST);

	lr_think_time(13);

	ctrx_mouse_double_click(210, 446, LEFT_BUTTON, 0, "Amadeus Selling Platform Connect - Google Chrome=snapshot82", CTRX_LAST);

	ctrx_type("C@rlson123", "", CTRX_LAST);

	ctrx_key("ENTER_KEY", 0, "", CTRX_LAST);

	lr_think_time(7);

	ctrx_mouse_click(184, 422, LEFT_BUTTON, 0, "Amadeus Selling Platform Connect - Google Chrome=snapshot87", CTRX_LAST);

	lr_think_time(10);

	ctrx_mouse_click(233, 416, LEFT_BUTTON, 0, "Amadeus Selling Platform Connect - Google Chrome=snapshot91", CTRX_LAST);

	ctrx_mouse_down(232, 416, LEFT_BUTTON, 0, "Amadeus Selling Platform Connect - Google Chrome=snapshot92", CTRX_LAST);

	ctrx_mouse_up(226, 414, LEFT_BUTTON, 0, "Amadeus Selling Platform Connect - Google Chrome=snapshot94", CTRX_LAST);

	ctrx_mouse_down(236, 415, LEFT_BUTTON, 0, "Amadeus Selling Platform Connect - Google Chrome=snapshot95", CTRX_LAST);

	ctrx_mouse_up(181, 426, LEFT_BUTTON, 0, "Amadeus Selling Platform Connect - Google Chrome=snapshot96", CTRX_LAST);

	ctrx_mouse_click(229, 426, LEFT_BUTTON, 0, "Amadeus Selling Platform Connect - Google Chrome=snapshot98", CTRX_LAST);

	ctrx_key("DELETE_KEY", 0, "", CTRX_LAST);

	ctrx_key("NO_KEY", MODIF_SHIFT, "", CTRX_LAST);

	lr_think_time(6);

	ctrx_mouse_click(251, 418, LEFT_BUTTON, 0, "Amadeus Selling Platform Connect - Google Chrome=snapshot101", CTRX_LAST);

	ctrx_type("HKGWL2102", "", CTRX_LAST);

	ctrx_key("TAB_KEY", 0, "", CTRX_LAST);

	lr_think_time(6);

	ctrx_mouse_click(236, 440, LEFT_BUTTON, 0, "Amadeus Selling Platform Connect - Google Chrome=snapshot106", CTRX_LAST);

	lr_think_time(8);

	ctrx_mouse_click(236, 440, LEFT_BUTTON, 0, "Amadeus Selling Platform Connect - Google Chrome=snapshot110", CTRX_LAST);

	ctrx_type("C@rlson123", "", CTRX_LAST);

	ctrx_key("ENTER_KEY", 0, "", CTRX_LAST);

	lr_think_time(17);

	ctrx_mouse_click(375, 150, LEFT_BUTTON, 0, "HKGWL2102 - Amadeus Selling Platform Connect - Google Chrome=snapshot114", CTRX_LAST);

	lr_think_time(8);

	ctrx_mouse_click(965, 10, LEFT_BUTTON, 0, "HKGWL2102 - Amadeus Selling Platform Connect - Google Chrome=snapshot115", CTRX_LAST);

	return 0;
}
