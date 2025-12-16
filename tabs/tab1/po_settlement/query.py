import pandas as pd

def load_po_settlement(engine):
    query = "SELECT * FROM ds_ipl.po_settlement;"
    return pd.read_sql(query, engine)
