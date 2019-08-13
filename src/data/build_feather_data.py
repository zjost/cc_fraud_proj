import os
import argparse
import pandas as pd

cat_cols = (['ProductCD'] + 
            ['card%d' % i for i in range(1, 7)] + 
            ['addr1', 'addr2', 'P_emaildomain', 'R_emaildomain'] + 
            ['M%d' % i for i in range(1, 10)] + 
            ['DeviceType', 'DeviceInfo'] +
            ['id_%d' % i for i in range(12, 39)])

id_cols = ['TransactionID', 'TransactionDT']
target = 'isFraud'
type_map = {c: str for c in cat_cols}


def load_raw_data(data_dir, data_type, is_gz):
    if data_type not in ['train', 'test']:
        raise Exception('data_type can only be "train" or "test"')
    fp_id = '{}_identity.csv'.format(data_type)
    fp_trans = '{}_transaction.csv'.format(data_type)
    if is_gz:
        fp_id += '.gz'
        fp_trans += '.gz'
    df_id = pd.read_csv(os.path.join(data_dir, fp_id), dtype=type_map)
    df_trans = pd.read_csv(os.path.join(data_dir, fp_trans), dtype=type_map)
    return df_trans.merge(df_id, on='TransactionID', how='left')
        
def main():
    parser = argparse.ArgumentParser(description='Process raw Kaggle data')
    parser.add_argument('data_dir', help='the directory with the raw csv data')
    parser.add_argument('--gzipped', type=bool, default=False,
                        help='whether or not you gzipped the data.')

    args = parser.parse_args()
    
    df_train = load_raw_data(args.data_dir, 'train', args.gzipped)
    df_test = load_raw_data(args.data_dir, 'test', args.gzipped)
    # Save in feather format 
    df_train.to_feather(os.path.join(args.data_dir, 'train.feather'))
    df_test.to_feather(os.path.join(args.data_dir, 'test.feather'))
    
    
if __name__ == '__main__':
    main()
