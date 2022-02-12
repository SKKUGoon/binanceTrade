from settings.color import BColors

bc = BColors()

# BROADCASTING MODULE
BROADCAST_TOTL_SIG0 = "[WS] Client Just Connected"
BROADCAST_TOTL_SIG1 = "[WS] A client just disconnected"
BROADCAST_TOTL_SIG2 = "[WS] Active Ping"

# BROADCAST_BACK
BROADCAST_BACK_SIG0 = f"{bc.HEADER}[WS] BackOffice has +1 Client{bc.ENDC}"
BROADCAST_BACK_SIG1 = f"{bc.HEADER}[WS] BackOffice has -1 Client{bc.ENDC}"
BROADCAST_BACK_SIG2 = f"{bc.HEADER}[WS] Received connection message from back office{bc.ENDC}"
BROADCAST_BACK_SIG3 = f"{bc.HEADER}[WS] Received test message from back office{bc.ENDC}"

# BROADCAST_MIDDLE
BROADCAST_MIDD_SIG0 = f"{bc.OKBLUE}[WS] MiddleOffice has +1 Client{bc.ENDC}"
BROADCAST_MIDD_SIG1 = f"{bc.OKBLUE}[WS] MiddleOffice has -1 Client{bc.ENDC}"
BROADCAST_MIDD_SIG2 = f"{bc.OKBLUE}[WS] Received trade messages from middle office{bc.ENDC}"

# BROADCAST_FRONT
BROADCAST_FRNT_SIG0 = f"{bc.OKCYAN}[WS] FrontOffice has +1 Client{bc.ENDC}"
BROADCAST_FRNT_SIG1 = f"{bc.OKCYAN}[WS] FrontOffice has -1 Client{bc.ENDC}"

# BACK OFFICE MODULE
BACK01_DATABASE_MSG0 = f"[B01 DBMS] {bc.HEADER}TRADE signal{bc.ENDC} inserted"
BACK01_DATABASE_MSG1 = f"[B01 DBMS] {bc.HEADER}TEST TRADE{bc.ENDC} signal inserted"
BACK01_DATABASE_MSG2 = f"[B01 DBMS] {bc.HEADER}PING{bc.ENDC} signal inserted"

BACK03_DISCORD_READY = f"[Discord] Ready"
BACK03_DISCORD_CONNECTION = f"[Discord] sending connection ping"


# MIDDLE OFFICE MODULE
# MIDDLE01
MIDDLE01_MSG_NOINFO = f"{bc.OKBLUE}[M01 Upbit] No new information{bc.ENDC}"
MIDDLE01_MSG_ORDER = f"{bc.OKBLUE}[M01 Upbit] Order Sent. Sleeping for 60 sec{bc.ENDC}"
MIDDLE01_MSG_ERROR = f"{bc.WARNING}Not able. Restarting class method{bc.ENDC}"

# MIDDLE02
MIDDLE02_MSG_NOINFO = f"{bc.OKBLUE}[M02 Bitthumb] No new information{bc.ENDC}"
MIDDLE02_MSG_ORDER = f"{bc.OKBLUE}[M02 Bitthumb] Order Sent. Sleeping for 140 sec{bc.ENDC}"
MIDDLE02_MSG_ERROR = f"{bc.WARNING}Not able. Restarting class method{bc.ENDC}"

# MIDDLE03
MIDDLE03_MSG_PREP = f"{bc.OKBLUE}[Spread Arbitrage] Collecting..{bc.ENDC}"
MIDDLE03_MSG_SIG_TIME = "=========={}=========="  # Date goes inside
MIDDLE03_MSG_SIG_IND_ON = f"{bc.OKBLUE}[Spread Arbitrage] Signal On{bc.ENDC}"
MIDDLE03_MSG_SIG_IND_OFF = f"{bc.OKBLUE}[Spread Arbitrage] Signal Off{bc.ENDC}"
MIDDLE03_MSG_SIG_PRC = "Current Price Delivery: {}\nCurrent Price Perp: {}"
MIDDLE03_MSG_SIG_SPD = "Current LONG Delivery: {}\nCurrent SHORT Perp: {}"
MIDDLE03_MSG_SIG_FAIL = "Spread Signal too weak. Current Spread {}. Minimum Dist {}"


# FRONT OFFICE MODULE
# FRONT00
FRONT00_MSG_BALANCE = f"{bc.OKCYAN}[F00 SPOT TRADER] Re-checking Balance.{bc.ENDC}"

# FRONT01
FRONT01_MSG_BALANCE = f"{bc.OKCYAN}[F01 SPREAD TRADER] Re-checking Balance.{bc.ENDC}"

# FRONT02
FRONT02_MSG_BALANCE = f"{bc.OKCYAN}[F02 FUTURE TRADER] Re-checking Balance.{bc.ENDC}"