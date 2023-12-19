import logging
import sys

# Create report logger and set level to info.
logger = logging.getLogger("ReportLogger")
logger.setLevel("INFO")

# Create handler, set output stream to stdout instead of default stderr and set level to info.
handler = logging.StreamHandler(sys.stdout)
handler.setLevel("INFO")

# Create message format (used for printing into console) and add it to handler.
message_format = logging.Formatter('%(levelname)s     %(message)s')
handler.setFormatter(message_format)

# Add handler to report logger.
logger.addHandler(handler)
