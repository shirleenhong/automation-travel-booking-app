SellcoLogin()
{
	
lr_start_transaction("Sellco Login");

	lr_think_time(30);

	ctrx_key("w", MODIF_CONTROL, CTRX_LAST);
	ctrx_type("a", CTRX_LAST);
	ctrx_type("a", CTRX_LAST);

// Open Google Chrome
//	ctrx_type("go", CTRX_LAST);
//	ctrx_type("go", CTRX_LAST);
//	lr_think_time(2);	
//	ctrx_key("ENTER_KEY", 0, CTRX_LAST);
//	lr_think_time(5);
//	ctrx_key("l", MODIF_CONTROL, CTRX_LAST);
//	lr_think_time(2);
//	ctrx_type("acceptance.custom.sellingplatformconnect.amadeus.com", CTRX_LAST);
	
	ctrx_key("ENTER_KEY", 0, CTRX_LAST);	

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
