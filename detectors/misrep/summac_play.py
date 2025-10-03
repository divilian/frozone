# (All these warnings are harmless, so suppressing for now to reduce clutter.)
import warnings
warnings.filterwarnings("ignore", category=FutureWarning)
warnings.filterwarnings("ignore", category=UserWarning)
import os
os.environ["TRANSFORMERS_VERBOSITY"] = "error"  # fallback, set before HF imports
from transformers.utils import logging as hf_logging
hf_logging.set_verbosity_error()
import logging as pylog
pylog.getLogger("transformers").setLevel(pylog.ERROR)
pylog.getLogger("transformers.modeling_utils").setLevel(pylog.ERROR)
# (optional) remove any pre-attached handlers that might print anyway
pylog.getLogger("transformers").handlers.clear()
from transformers import logging
logging.set_verbosity_error()   # or .warning()
# -----------------------------------------------------------------------------

# Requires summac, nltk, and nltk.download('punkt_tab')

import torch
from summac.model_summac import SummaCZS, SummaCConv

device = "cuda" if torch.cuda.is_available() else "cpu"

model_zs = SummaCZS(
    granularity="sentence",
    model_name="vitc",
    device=device,
)

model_conv = SummaCConv(
    #models=["mnli","anli","vitc"],
    models=["mnli"],
    bins='percentile',
    granularity="sentence",
    nli_labels="e",
    start_file="default",
    agg="mean",
    device=device,
)

document = """
According to the American Presidency Project, in the 2020 U.S. presidential
election, Democratic nominee Joe Biden defeated incumbent Republican President
Donald Trump, winning 306 electoral votes to Trump’s 232. Biden also won the
popular vote, garnering about 51.3 % to Trump’s 46.9 %
"""

print("Source:")
print(document)

claim = input("\nEnter claim: ")
while claim != "done":
    zs = model_zs.score([document], [claim])
    conv = model_conv.score([document], [claim])
    print(f"ZS: {zs['scores'][0]:.3f}, Conv: {conv['scores'][0]:.3f}")
    claim = input("Enter claim: ")

