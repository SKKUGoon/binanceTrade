STATUS_0 = "Database Stable"
STATUS_1 = "Database Initiation"
STATUS_2 = "Signal Received"
STATUS_3 = "No Signal Received"
STATUS_4 = "Ordering {} on {}"
STATUS_5 = "Trade Fail. Order Not Filled During Window. Cancel Existing Order."
STATUS_6 = "Trade Partial Success. Partial Order Filled. Cancel Existing Order. Waiting for Exit Window"
STATUS_7 = "Trade Success. All Order Filled. Waiting for Exit Window"
STATUS_8 = "Sell Complete. All Trade Complete. Waiting 60 seconds safe margin."

EXIT_0 = "EventDriven Trading Exit Window: Time Expired"
EXIT_1 = "EventDriven Trading Exit Windiw: Return Fullfilled"

ERROR_0 = "Unique Assertion Failed. No New Information"
ERROR_1 = "All Asset Not Available in Binance"


ORDERFILL = "{}\nORDER INFO\n[{}]\nOrderID: {}\nQuantity: {}\nPrice: {}\nUsed: {}\n{}"
ORDERFILLPADDING = "================"

ORDERCANCEL = "{}\nORDER INFO\n[{}]\nOrderID: {}\nCancelled Successfully\n{}"


from settings.color import BColors

bc = BColors()
BROADCAST_TOTL_SIG0 = "[WS] Client Just Connected"
BROADCAST_TOTL_SIG1 = "[WS] A client just disconnected"

BROADCAST_BACK_SIG0 = f"{bc.HEADER}[WS] BackOffice has +1 Client{bc.ENDC}"
BROADCAST_BACK_SIG1 = f"{bc.HEADER}[WS] BackOffice has -1 Client{bc.ENDC}"
BROADCAST_BACK_SIG2 = f"{bc.HEADER}[WS] Received connection message from back office{bc.ENDC}"
BROADCAST_BACK_SIG3 = f"{bc.HEADER}[WS] Received test message from back office{bc.ENDC}"

BROADCAST_MIDD_SIG0 = f"{bc.OKBLUE}[WS] MiddleOffice has +1 Client{bc.ENDC}"
BROADCAST_MIDD_SIG1 = f"{bc.OKBLUE}[WS] MiddleOffice has -1 Client{bc.ENDC}"
BROADCAST_MIDD_SIG2 = f"{bc.OKBLUE}[WS] Received trade messages from middle office{bc.ENDC}"

BROADCAST_FRNT_SIG0 = f"{bc.OKCYAN}[WS] FrontOffice has +1 Client{bc.ENDC}"
BROADCAST_FRNT_SIG1 = f"{bc.OKCYAN}[WS] FrontOffice has -1 Client{bc.ENDC}"
