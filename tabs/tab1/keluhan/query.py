import pandas as pd

def load_keluhan(engine):
    query_keluhan = "SELECT * FROM ds_ipl.tiket_keluhan;"
    return pd.read_sql(query_keluhan, engine)
