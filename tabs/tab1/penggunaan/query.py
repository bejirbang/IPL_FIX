import pandas as pd

def load_stamping(engine):
    query = "SELECT * FROM ds_ipl.penggunaan;"
    return pd.read_sql(query, engine)
