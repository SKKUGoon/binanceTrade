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
