*** Settings ***
Library           Collections
Library           ExcelLibrary
Resource          ../../../../resources/common/global_resources.txt
Resource          ../other_services_verification.txt
Resource          ../../client_info/client_info_verification.txt
Resource          ../../../../resources/panels/other_svcs.txt
Resource          ../../../../resources/api_resource/remarks_core.txt

*** Test Cases ***
Sample - Getting values from excel file (containing product and vendor data)
    Comment    ${product_code} =    Get Product Code    SG    Deposit
    Comment    Comment    Log    Product code is ${product_code}
    Comment    Comment    Comment    ${product_gst} =    Get GST Percentage    SG    Insurance
    Comment    Comment    Comment    Log    Product GST percentage is ${product_gst}
    Get Vendor Code    HK    Car Rental Prepaid    FIRST MARKETING
    Log    Vendor Code is: ${vendor_code}

Select Product name
    Comment    Open Excel    ${product_vendor_sg_hk_in}    ${product_vendor_sg_hk_in}
    Comment    ${row_count} =    Get Row Count    Conso
    Comment    : FOR    ${each_row}    IN RANGE    ${row_count}
    Comment    \    ${product_name} =    Get Product Name    ${each_row}
    Comment    \    Select Product    ${product_name}
    Comment    \    Take Screenshot
    Comment    Select Product    24 Hours Emergency Svcs
    Comment    Select Product    Car - Local Booking Fee
    Comment    Select Product    CWT Refund Admin Fee
    Comment    Select Product    Hotel - Local Booking Fee
    Comment    Select Product    Management Fee
    Comment    Select Product    Meet And Greet
    Comment    Select Product    MICE- Activities
    Comment    Select Product    MISC - Local Booking Fee
    Comment    Select Product    Despatch Charge
    Comment    HK
    Comment    Select Product    ADDITIONAL BSP AIR
    Comment    Select Product    AIR REFUND
    Comment    Select Product    CONSOLIDATOR TICKET
    Comment    Select Product    TOUR PACKAGE
    Comment    Select Product    TRANSACTION FEE
    Comment    Select Product    HOTEL - PREPAID
    Comment    Select Product    LIMOUSINE
    Comment    Select Product    MEETING AND EVENTS
    Comment    Select Product    INSURANCE
    Comment    Select Product    BSP AIR TICKET
    Comment    Select Product    MEET AND GREET SERVICE
    Comment    Select Product    CRUISE
    Comment    Select Product    FERRY TICKET
    Comment    Select Product    TRAIN TICKET
    Comment    Select Product    VISA PROCESSING
    Comment    Select Product    24 EMERGENCY SERVICE FEE
    Comment    Select Product    C2G HOTEL FEE
    Comment    Select Product    Certificate Deposit
    Comment    Select Product    DISCOUNT
    Comment    Select Product    DOC BANK FEE
    Comment    Select Product    HANDLING FEE
    Comment    Select Product    LOCAL EMERGENCY SVC
    Comment    Select Product    LOW COST CARRIER SVC FEE
    Comment    Select Product    OTHER
    Comment    Select Product    REFERRAL
    Comment    Select Product    REVALIDATION FEE
    Comment    Select Product    SVC Fee for Surcharges
    Comment    Select Product    Car Rental Prepaid
    Comment    Select Product    Low Cost Carrier
    Comment    Select Product    ENTITLEMT INV - MICE
    Comment    Select Product    AEL Ticket
    Comment    SG
    Select Product    Consolidator Ticket
    Comment    Select Product    Prepaid Hotel
    Comment    Select Product    Tour Package
    Comment    Select Product    Insurance
    Comment    Select Product    Visa Cost
    Comment    Select Product    Car Transfer
    Comment    Select Product    AA SEGMENT BOOKING FEE
    Comment    Select Product    BSP Ticket And MPD
    Comment    Select Product    FERRY
    Comment    Select Product    NULL
    Comment    Select Product    24 Hours Emergency Svcs
    Comment    Select Product    Car - Local Booking Fee
    Comment    Select Product    CWT Refund Admin Fee
    Comment    Select Product    Hotel - Local Booking Fee
    Comment    Select Product    Management Fee
    Comment    Select Product    Meet And Greet
    Comment    Select Product    MICE- Activities
    Comment    Select Product    MISC - Local Booking Fee
    Comment    Select Product    Visa Handling Fee
    Comment    Select Product    MICE-GST
    Comment    Select Product    Airline Penalty Fee
    Comment    Select Product    Car - Overseas Booking Fee
    Comment    Select Product    CWT TO GO HOTEL FEE
    Comment    Select Product    Deposit
    Comment    Select Product    Documentation Fee
    Comment    Select Product    Hotel - Overseas Booking Fee
    Comment    Select Product    MISC - Overseas Booking Fee
    Comment    Select Product    Miscellaneous - MICE
    Comment    Select Product    Reissue-Revalidation Fee
    Comment    Select Product    Train Tickets
    Comment    Select Product    Transaction Fee
    Comment    Select Product    Despatch Charge
    Comment    Select Product    LOW COST CARRIER - CLIENT CARD
    Comment    Select Product    Air Commission Returned

Try reading the excel file when its part of framework
    Comment    Open Excel    ${CURDIR}../../../../resources/test_data/other_services_productvendor_master.xls
    Log    ${CURDIR}
    Log    ${EXECDIR}
    Open Excel    ${EXECDIR}\\resources\\test_data\\other_services_productvendor_data.csv

Getting HK Vendor Default EO Status Value
    ${auto_complete}    Verify If HK Vendor Should Default To Complete Status    100
    Log    ${auto_complete}

*** Keywords ***
Obsolete Get Product Code
    [Arguments]    ${country_code}    ${product_name}
    Comment    Open Excel    C:\\Python27\\ExcelRobotTest\\Consolidated ProductVendor_HKSG_UATProd.xls
    Open Excel    ${product_vendor_data}
    Comment    Log    ${product_vendor_data}
    Comment    ${row_count} =    Get Row Count    Conso
    Comment    ${product_code} =    Set Variable    ${EMPTY}
    Comment    : FOR    ${product_pointer}    IN RANGE    ${row_count}
    Comment    \    ${current_cocode} =    Read Cell Data By Coordinates    Conso    0    ${product_pointer}
    Comment    \    ${current_product} =    Read Cell Data By Coordinates    Conso    1    ${product_pointer}
    Comment    \    ${current_pcode} =    Read Cell Data By Coordinates    Conso    2    ${product_pointer}
    Comment    \    Run Keyword If    '${current_product.lower()}' == '${product_name.lower()}' and '${current_cocode.lower()}' == '${country_code.lower()}'    Exit For Loop
    Comment    ${product_code} =    Set Variable    ${current_pcode} =
    [Return]    ${product_code}

Get GST Percentage
    [Arguments]    ${country_code}    ${product_name}
    Open Excel    C:\\Python27\\ExcelRobotTest\\Consolidated ProductVendor_HKSG_UATProd.xls
    ${row_count} =    Get Row Count    Conso
    ${current_gst_percentage} =    Set Variable    ${EMPTY}
    : FOR    ${product_pointer}    IN RANGE    ${row_count}
    \    ${current_cocode} =    Read Cell Data By Coordinates    Conso    0    ${product_pointer}
    \    ${current_product} =    Read Cell Data By Coordinates    Conso    1    ${product_pointer}
    \    ${current_gst_percentage} =    Read Cell Data By Coordinates    Conso    4    ${product_pointer}
    \    Run Keyword If    '${current_product.lower()}' == '${product_name.lower()}' and '${current_cocode.lower()}' == '${country_code.lower()}'    Exit For Loop
    ${gst_percentage} =    Set Variable    ${current_gst_percentage}
    [Return]    ${gst_percentage}

Get Product Name
    [Arguments]    ${row_number}
    Open Excel    C:\\Python27\\ExcelRobotTest\\Consolidated ProductVendor_HKSG_UATProd.xls
    ${product_name} =    Read Cell Data By Coordinates    Conso    1    ${row_number}
    [Return]    ${product_name}

Get Vendor Name

Verify If HK Vendor Should Default To Complete Status
    [Arguments]    ${vendor_code}
    ${vendor_auto_complete}=    Create Dictionary
    Set To Dictionary    ${vendor_auto_complete}    3075    FEDERAL INSURANCE COMPANY
    Set To Dictionary    ${vendor_auto_complete}    252    NORTHWEST AIRLINES
    Set To Dictionary    ${vendor_auto_complete}    800    CWT VISA
    Set Test Variable    ${vendor_auto_complete}
    ${row_count}=    Get Length    ${vendor_auto_complete}
    ${vendor_key_auto_complete} =    Get Dictionary Keys    ${vendor_auto_complete}
    :FOR    ${each_product}    IN RANGE    ${row_count}
    \    ${auto_complete}    Set Variable If    '${vendor_code}'=='@{vendor_key_auto_complete}[${each_product}]'    True    False
    \    Exit For Loop If    '${vendor_code}'=='@{vendor_key_auto_complete}[${each_product}]'
    ${default_eo_status}    Set Variable If    '${auto_complete}'=='True'    Complete    New
    Set Suite Variable    ${default_eo_status}
    [Return]    ${auto_complete}
