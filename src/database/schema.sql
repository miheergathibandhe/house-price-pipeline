CREATE TABLE IF NOT EXISTS house_prices(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    GrLivArea REAL,
    BedroomAbvGr REAL,
    FullBath REAL,
    YearBuilt REAL,
    OverallQual REAL,
    SalePrice REAL);

CREATE TABLE IF NOT EXISTS model_version(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    timestamp TEXT,
    model_name TEXT,
    rmse REAL,
    r2 REAL,
    params TEXT);

CREATE TABLE if not EXISTS predictions(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    mode_version_id INTEGER,
    predicted_price REALO,
    timestamp TEXT);