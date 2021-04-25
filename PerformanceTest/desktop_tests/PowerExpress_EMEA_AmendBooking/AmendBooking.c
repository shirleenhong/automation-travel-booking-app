AmendBooking()
{

lr_start_transaction("Creating PNR");

	ctrx_key("ESC_KEY", MODIF_CONTROL, "", CTRX_LAST);
	
	ctrx_key("NO_KEY", MODIF_CONTROL, "", CTRX_LAST);	
	
	lr_think_time(2);

	ctrx_type("cmd", "", CTRX_LAST);

	lr_think_time(2);

	ctrx_key("ENTER_KEY", 0, "", CTRX_LAST);
	
	lr_think_time(2);

	ctrx_type("call pybot --test \"Amend Booking\" -d d:\\seco\\result\\{CitrixLogin} -v version:18.10 -v test_environment:Test -v surname:{Surname} -v firstname:{Firstname} -v use_mock_env:{UseMockEnv} -v booking_iteration:{BookingIteration} D:\\seco\\desktop_tests\\apac.txt", "", CTRX_LAST);

	lr_think_time(2);

	ctrx_key("ENTER_KEY", 0, "", CTRX_LAST);

	//multiply think time to booking iteration
	
	i = atoi( lr_eval_string( "{BookingIteration}" ));
	i = 900 * i;
	
	lr_think_time(i);

    lr_end_transaction("Creating PNR", LR_AUTO);
	
	return 0;
}
