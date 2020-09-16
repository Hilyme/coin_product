class Common(object):

    server_host = '0.0.0.0'
    server_port = 5000

    trade_side_buy = 'buy'
    trade_side_sell = 'sell'

    trade_type_limit = 'limit'
    trade_type_market = 'market'
    trade_type_up = 'up'
    trade_type_down = 'down'
    trade_type_updown = 'up_down'
    trade_type_downup = 'down_up'

    trade_source_spot = 'spot'
    trade_source_lever = 'lever'

    trend_short = 'short'
    trend_long = 'long'
    trend_long_short = 'long_short'

    open_long = 'open_long'
    open_short = 'open_short'
    close_long = 'close_long'
    close_short = 'close_short'

    status_open = 'open'
    status_part_filled = 'part_filled'
    status_filled = 'filled'
    status_part_canceled = 'part_canceled'
    status_canceling = 'canceling'
    status_canceled = 'canceled'
    status_failure = 'failure'
    status_ordering = 'ordering'
    status_expired = 'expired'
    status_closed = 'closed'

    kline_1m = 'm_1'
    kline_3m = 'm_3'
    kline_5m = 'm_5'
    kline_15m = 'm_15'
    kline_30m = 'm_30'
    kline_1h = 'h_1'
    kline_2h = 'h_2'
    kline_4h = 'h_4'
    kline_6h = 'h_6'
    kline_1d = 'd_1'
    kline_1w = 'w_1'

    db_host = 'localhost'
    db_port = 27017
    db = 'coin'
    db_spot = 'spot'
    db_lever = 'lever'
    db_future = 'future'
    db_future_auto = 'future_auto'
    db_spot_auto = 'spot_auto'
    db_lever_auto = 'lever_auto'
    db_coin_pair = 'coin_pair'
    db_future_coin_pair = 'future_coin_pair'
    db_fc = 'fc'
    db_analyze = 'analyze'
    db_etf = 'etf'

    switch_start = 'start'
    switch_pause = 'pause'
    switch_stop = 'stop'

    # ------trade_kind------
    spot = 'spot'   # 币币
    futures = 'futures'     # 交割
    swap = 'swap'   # 永续
    # ------frequency------
    frequency_tick = "ticker"
    frequency_1min = "candle60s"
    frequency_3min = "candle180s"
    frequency_5min = "candle300s"
    frequency_15min = "candle900s"
    frequency_30min = "candle1800s"
    frequency_1hour = "candle3600s"
    frequency_2hour = "candle7200s"
    frequency_4hour = "candle14400s"
    frequency_6hour = "candle21600s"
    frequency_12hour = "candle43200s"
    frequency_1day = "candle86400s"
    frequency_1week = "candle604800s"
    frequency_depth = "depth"

    interval_1min = "60"
    interval_3min = "180"
    interval_5min = "300"
    interval_15min = "900"
    interval_30min = "1800"
    interval_1hour = "3600"
    interval_2hour = "7200"
    interval_4hour = "14400"
    interval_6hour = "21600"
    interval_12hour = "43200"
    interval_1day = "86400"
    interval_1week = "604800"

    # ------币币------
    ws_order = 'order'
    ws_account = 'account'
    ws_ticker = 'ticker'
    ws_kline = 'kline'
    ws_trade = 'trade'
    ws_depth = 'depth'
    # ------交割合约------
    ws_f_order = 'f_order'
    ws_f_account = 'f_account'
    ws_f_ticker = 'f_ticker'
    ws_f_kline = 'f_kline'
    ws_f_position = 'f_position'
    # ------永续合约------
    ws_sf_order = 'sf_order'
    ws_sf_account = 'sf_account'
    ws_sf_ticker = 'sf_ticker'
    ws_sf_kline = 'sf_kline'
    ws_sf_position = 'sf_position'
