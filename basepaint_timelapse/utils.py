import os

import pandas as pd
import requests
from dotenv import load_dotenv
from flipside import Flipside

load_dotenv()

def get_data():
  
  FLIPSIDE_API_KEY = os.environ['FLIPSIDE_API_KEY']
  """Initialize Flipside with your API Key / API Url"""
  flipside = Flipside(FLIPSIDE_API_KEY, "https://api-v2.flipsidecrypto.xyz")
  sql = """select * from base.core.fact_decoded_event_logs where contract_address =   lower('0xBa5e05cb26b78eDa3A2f8e3b3814726305dcAc83') and event_name = 'Painted'"""
  """Run the query against Flipside's query engine and await the results"""
  query_result_set = flipside.query(sql)
  df = pd.DataFrame(query_result_set.records)
  return df 


def decode_blob(hex_blob):
    # Convert the hex to binary, skipping the '0b' prefix
    bin_blob = bin(hex_blob)[2:]

    # Ensure the binary blob is a multiple of 24 by padding with zeros if necessary
    while len(bin_blob) % 24 != 0:
        bin_blob = '0' + bin_blob

    # Split the binary blob into 24-bit chunks
    chunks = [bin_blob[i:i+24] for i in range(0, len(bin_blob), 24)]

    decoded_data = []
    for chunk in chunks:
        x = int(chunk[:8], 2)   # First 8 bits
        y = int(chunk[8:16], 2)  # Next 8 bits
        color_index = int(chunk[16:], 2)  # Last 8 bits
        decoded_data.append((x, y, color_index))

    return decoded_data

def convert_and_decode(hex_string):
  pixel_int = int(hex_string, 16)
  res = decode_blob(pixel_int)
  return res



def get_color_mapping(day: int):
  base_url = "https://basepaint.xyz/api/theme/{}"
  resp = requests.get(base_url.format(str(day)))
  resp_json = resp.json()
  color_mapping = {i:v for i,v in enumerate(resp_json['palette'])}
  return (resp_json['theme'] , color_mapping )