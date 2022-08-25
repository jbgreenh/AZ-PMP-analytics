import pandas as pd

def scorecard(fp, ob=False):
    if ob:
        df_47 = pd.read_csv(f'data/47/disp_{fp}_ob.csv', sep='|')
    else:
        df_47 = pd.read_csv(f'data/47/disp_{fp}.csv', sep='|')
    df_48 = pd.read_csv(f'data/48/{fp}.csv', sep='|')
    
    df_47 = df_47[df_47['state'] == 'AZ']
    df_47 = df_47[['dea_number']]
    df_48 = df_48[['dea_number','totallookups']]
    df_merge = pd.merge(df_47, df_48, on='dea_number', how='left')
    df_merge = df_merge.groupby(['dea_number'], as_index=False).sum()
    
    n = df_merge.shape[0]
    n_lookups = df_merge[df_merge['totallookups'] > 0].shape[0]
    n_lookups_per = n_lookups/n
    n_lookups_per = n_lookups_per * 100
    n_lookups_str = f'{round(n_lookups_per, 2)}%'
    ob_str = 'ob_' if ob else ''
    df_lookups = pd.DataFrame({f'{ob_str}n_prescribers': [n], f'{ob_str}n_lookups': [n_lookups], f'{ob_str}%': [n_lookups_str]})
    score_str = f'{ob = } {n_lookups} / {n} = {n_lookups_str}'
    print(score_str)
    return df_lookups

def main():
    reg_scores = pd.DataFrame(columns=['n_prescribers', 'n_lookups', '%'])
    ob_scores = pd.DataFrame(columns=['ob_n_prescribers', 'ob_n_lookups', 'ob_%'])
    for fp in range(1, 17):
        reg_scores = pd.concat([reg_scores, scorecard(fp)])
        ob_scores = pd.concat([ob_scores, scorecard(fp, ob=True)])
    
    combined = pd.concat([reg_scores, ob_scores], axis=1)

    combined.to_clipboard(index=False)
    print('combined copied to clipboard')

if __name__ == '__main__':
    main() 