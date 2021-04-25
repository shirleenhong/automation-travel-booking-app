Action1()
{

	lr_think_time(19);

	lr_start_transaction("Launch_PowerEX");

	ctrx_sync_on_window("Start", ACTIVATE, 2, 728, 53, 39, "snapshot116", CTRX_LAST);

	ctrx_sync_on_window("HKGWL2102 - Amadeus Selling Platform Connect - Google Chrome", CREATE, 14, 14, 1051, 705, "snapshot118", CTRX_LAST);

	ctrx_mouse_double_click(105, 26, LEFT_BUTTON, 0, "HKGWL2102 - Amadeus Selling Platform Connect - Google Chrome=snapshot119", CTRX_LAST);

	lr_think_time(13);

	ctrx_sync_on_window("Desktop", ACTIVATE, 0, 0, 1281, 769, "snapshot120", CTRX_LAST);

	ctrx_key("ENTER_KEY", 0, "", CTRX_LAST);

	lr_end_transaction("Launch_PowerEX",LR_AUTO);

	lr_think_time(48);

	lr_start_transaction("SelectTeam");

	ctrx_sync_on_window("Team Selection", ACTIVATE, 100, 55, 322, 313, "snapshot122", CTRX_LAST);

	ctrx_mouse_click(31, 65, LEFT_BUTTON, 0, "Team Selection=snapshot124", CTRX_LAST);

	ctrx_mouse_click(262, 285, LEFT_BUTTON, 0, "Team Selection=snapshot126", CTRX_LAST);

	lr_end_transaction("SelectTeam",LR_AUTO);

	lr_think_time(13);

	lr_start_transaction("SelectClient");

	ctrx_sync_on_window("Power Express V18.10.63.0  [SVCSYEXTEST34 in TEST]", ACTIVATE, 0, 0, 1029, 756, "snapshot127", CTRX_LAST);

	ctrx_mouse_click(125, 449, LEFT_BUTTON, 0, "Power Express V18.10.63.0  [SVCSYEXTEST34 in TEST]=snapshot128", CTRX_LAST);

	ctrx_key("NO_KEY", MODIF_SHIFT, "", CTRX_LAST);

	lr_think_time(14);

	ctrx_mouse_click(507, 443, LEFT_BUTTON, 0, "Power Express V18.10.63.0  [SVCSYEXTEST34 in TEST]=snapshot130", CTRX_LAST);

	ctrx_mouse_click(505, 594, LEFT_BUTTON, 0, "Power Express V18.10.63.0  [SVCSYEXTEST34 in TEST]=snapshot132", CTRX_LAST);

	ctrx_mouse_click(505, 594, LEFT_BUTTON, 0, "Power Express V18.10.63.0  [SVCSYEXTEST34 in TEST]=snapshot133", CTRX_LAST);

	lr_think_time(4);

	ctrx_mouse_click(505, 594, LEFT_BUTTON, 0, "Power Express V18.10.63.0  [SVCSYEXTEST34 in TEST]=snapshot134", CTRX_LAST);

	ctrx_mouse_down(272, 523, LEFT_BUTTON, 0, "Power Express V18.10.63.0  [SVCSYEXTEST34 in TEST]=snapshot136", CTRX_LAST);

	ctrx_mouse_up(276, 524, LEFT_BUTTON, 0, "Power Express V18.10.63.0  [SVCSYEXTEST34 in TEST]=snapshot136", CTRX_LAST);

	ctrx_mouse_click(197, 495, LEFT_BUTTON, 0, "Power Express V18.10.63.0  [SVCSYEXTEST34 in TEST]=snapshot139", CTRX_LAST);

	ctrx_type("bear", "", CTRX_LAST);

	ctrx_key("ENTER_KEY", 0, "", CTRX_LAST);

	ctrx_type(" ", "", CTRX_LAST);

	lr_end_transaction("SelectClient",LR_AUTO);

	lr_think_time(25);

	lr_start_transaction("ClearALL");

	ctrx_mouse_click(982, 427, LEFT_BUTTON, 0, "Power Express V18.10.63.0  [SVCSYEXTEST34 in TEST]=snapshot142", CTRX_LAST);

	lr_think_time(4);

	ctrx_sync_on_window("Power Express", ACTIVATE, 212, 342, 592, 228, "snapshot143", CTRX_LAST);

	ctrx_mouse_click(254, 195, LEFT_BUTTON, 0, "Power Express=snapshot145", CTRX_LAST);

	lr_end_transaction("ClearALL",LR_AUTO);

	return 0;
}
