"""Configuration of report logger, uses colorlog for coloring log records."""
from sys import stdout
import colorlog


# Create report logger and set level to debug.
logger = colorlog.getLogger("ReportLogger")
logger.setLevel("DEBUG")

# Create handler, set output stream to stdout instead of default stderr and set level to debug.
handler = colorlog.StreamHandler(stdout)
handler.setLevel("DEBUG")

# Create message format and add it to handler.
message_format = colorlog.ColoredFormatter(
	"%(log_color)s%(asctime)s     %(message)s",
	datefmt="%d.%m.%Y %H:%M:%S",
	log_colors={
		"DEBUG":    "green",     # Used for assertion passed messages.
		"INFO":     "blue",      # Used for info messages.
		"WARNING":  "red"        # Used for assertion failed and exception messages.
	}
)
handler.setFormatter(message_format)

# Add handler to report logger.
logger.addHandler(handler)
