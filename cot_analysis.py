import pandas as pd

def cot_index(series, lookback=156):
    lowest = series.rolling(lookback).min()
    highest = series.rolling(lookback).max()
    return 100 * (series - lowest) / (highest - lowest + 1e-9)

def percent_of_oi(net, oi):
    return 100 * (net / oi.replace(0, 1e-9))

def wof_change(series, periods=1):
    return series.diff(periods=periods)

def advanced_signals(df):
    # Compute main institutional metrics
    df['Noncommercial_Net'] = df['Noncommercial_Long_All'] - df['Noncommercial_Short_All']
    df['Commercial_Long'] = df.get('Commercial_Long_All', 0)
    df['Commercial_Short'] = df.get('Commercial_Short_All', 0)
    df['Commercial_Net'] = df['Commercial_Long'] - df['Commercial_Short']
    df['COT_Index'] = df.groupby('Market_and_Exchange_Names')['Noncommercial_Net'].transform(lambda x: cot_index(x, 156))
    df['Comm_COT_Index'] = df.groupby('Market_and_Exchange_Names')['Commercial_Net'].transform(lambda x: cot_index(x, 156))

    # Percentage metrics
    df['NetPctOI'] = percent_of_oi(df['Noncommercial_Net'], df['Open_Interest_All'])
    df['CommNetPctOI'] = percent_of_oi(df['Commercial_Net'], df['Open_Interest_All'])

    # Rate of change metrics (w/w, 4w, 8w)
    df['Net_1w_Change'] = df.groupby('Market_and_Exchange_Names')['Noncommercial_Net'].transform(lambda x: wof_change(x, 1))
    df['Net_4w_Change'] = df.groupby('Market_and_Exchange_Names')['Noncommercial_Net'].transform(lambda x: wof_change(x, 4))
    df['Net_8w_Change'] = df.groupby('Market_and_Exchange_Names')['Noncommercial_Net'].transform(lambda x: wof_change(x, 8))
    df['Comm_1w_Change'] = df.groupby('Market_and_Exchange_Names')['Commercial_Net'].transform(lambda x: wof_change(x, 1))

    def detect_signal(row):
        # Multi-factor logic, return confidence score as well
        score = 0
        notes = []

        # Smart money: commercials
        if row['Comm_COT_Index'] < 10:
            score -= 1
            notes.append("Commercials at extreme short")
        elif row['Comm_COT_Index'] > 90:
            score += 1
            notes.append("Commercials at extreme long")

        # Non-commercials
        if row['COT_Index'] > 85:
            score += 1
            notes.append("Specs at extreme long")
        elif row['COT_Index'] < 15:
            score -= 1
            notes.append("Specs at extreme short")

        # Net Position as % of OI
        if row['NetPctOI'] > 20:
            score += 0.5
            notes.append("Spec net posit. %OI high")
        elif row['NetPctOI'] < -20:
            score -= 0.5
            notes.append("Spec net posit. %OI low")

        # Position change (momentum/reversal!)
        if abs(row['Net_1w_Change']) > 10000 and abs(row['Net_1w_Change']) > 0.2 * abs(row['Noncommercial_Net']):
            if row['Net_1w_Change'] > 0:
                score += 0.5
                notes.append("Large weekly net increase")
            else:
                score -= 0.5
                notes.append("Large weekly net drop")

        # Commercials shift (contrarian signal)
        if abs(row['Comm_1w_Change']) > 10000:
            if row['Comm_1w_Change'] > 0:
                score += 0.5
                notes.append("Commercials adding long fast")
            else:
                score -= 0.5
                notes.append("Commercials dumping fast")

        # Final multi-factor signal determination
        if score >= 1.5:
            s = 'Strong Bullish'
        elif score >= 0.5:
            s = 'Bullish'
        elif score <= -1.5:
            s = 'Strong Bearish'
        elif score <= -0.5:
            s = 'Bearish'
        else:
            s = 'Neutral'

        return pd.Series([s, score, '; '.join(notes)])

    latest = df.groupby('Market_and_Exchange_Names').tail(1).copy()
    latest[['AdvancedSignal', 'Score', 'Factors']] = latest.apply(detect_signal, axis=1)
    return latest[[
        'Market_and_Exchange_Names', 'Report_Date_as_YYYY-MM-DD', 'AdvancedSignal', 'Score', 'Factors',
        'Noncommercial_Net', 'Commercial_Net', 'COT_Index', 'Comm_COT_Index', 'NetPctOI', 'Net_1w_Change', 'Comm_1w_Change', 'Open_Interest_All'
    ]]

if __name__ == "__main__":
    df = pd.read_csv("cot_currencies.csv")
    adv_signals = advanced_signals(df)
    adv_signals.to_csv("advanced_signals.csv", index=False)
    print(adv_signals)
