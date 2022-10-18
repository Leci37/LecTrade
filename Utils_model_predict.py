import numpy as np
import pandas as pd
import tensorflow as tf
from tensorflow import keras
from sklearn.preprocessing import MinMaxScaler, StandardScaler
from sklearn.model_selection import train_test_split

import UtilsL
import Utils_buy_sell_points
import Utils_col_sele
import a_manage_stocks_dict
from LogRoot.Logging import Logger

METRICS_ACCU_PRE = [
      #keras.metrics.TrueNegatives(name='tn'),
      keras.metrics.BinaryAccuracy(name='accuracy')
      #keras.metrics.Precision(name='precision')
]

METRICS_ALL = [
      keras.metrics.TruePositives(name='tp'),
      keras.metrics.FalsePositives(name='fp'),
      keras.metrics.TrueNegatives(name='tn'),
      keras.metrics.FalseNegatives(name='fn'),
      keras.metrics.BinaryAccuracy(name='accuracy'),
      keras.metrics.Precision(name='precision'),
      keras.metrics.Recall(name='recall'),
      keras.metrics.AUC(name='auc'),
      keras.metrics.AUC(name='prc', curve='PR'), # precision-recall curve
]



def load_and_clean_DF_Train_from_csv(path, op_buy_sell : a_manage_stocks_dict.Op_buy_sell, columns_selection = [], Y_TARGET ='buy_sell_point',  ):
    # https://www.kaggle.com/code/andreanuzzo/balance-the-imbalanced-rf-and-xgboost-with-smote/notebook

    #El metodo puede recibir por path, leer.csv o por un df descargado en el momento
    raw_df = pd.read_csv(path, index_col=False, sep='\t')
    Logger.logr.info("df loaded from .csv Shape: "+ str( raw_df.shape ) + " Path: "+path )
    # else:
    #     Logger.logr.info("df has just loaded in memory (no read .csv) Shape: "+ str(  raw_df.shape))

    df = load_and_clean__buy_sell_atack(raw_df, columns_selection, op_buy_sell, Y_TARGET)
    return df


def load_and_clean__buy_sell_atack( raw_df, columns_selection, op_buy_sell : a_manage_stocks_dict.Op_buy_sell,  Y_TARGET  ='buy_sell_point' ):

    if not columns_selection:
        Logger.logr.info("columns_selection List is empty, works trains with all default columns")
    else:
        Logger.logr.debug("columns_selection List HAS vulues, works trains with: " + ', '.join(columns_selection))
        raw_df = raw_df[columns_selection]
        if 'ti_acc_dist' in raw_df.columns:
            raw_df = UtilsL.fill_last_values_of_colum_with_previos_value(raw_df, "ti_acc_dist")
        if "ti_ease_of_movement_14" in raw_df.columns:
            raw_df = UtilsL.fill_last_values_of_colum_with_previos_value(raw_df, "ti_ease_of_movement_14")
        if "ichi_chikou_span" in raw_df.columns:  # TODO muchas columnas nan eliminar
            raw_df = UtilsL.fill_last_values_of_colum_with_previos_value(raw_df, "ichi_chikou_span")

    # raw_df[Y_TARGET] = raw_df[Y_TARGET].astype(int).replace([101, -101], [100, -100])
    # raw_df[Y_TARGET] = raw_df[Y_TARGET].astype(int).replace(-100, 0)  # Solo para puntos de compra

    df = Utils_buy_sell_points.select_work_buy_or_sell_point(raw_df.copy(), op_buy_sell )

    print("COMPRA VENTA PUNTO")
    Logger.logr.debug(" groupby(Y_TARGET).count() " + str(df[['Date', Y_TARGET]].groupby(Y_TARGET).count()))
    df = cast_Y_label_binary(df, label_name=Y_TARGET)
    df = clean_redifine_df(df)
    return df


def cast_Y_label_binary(raw_df, label_name = 'buy_sell_point'):

    Y_target_classes = raw_df[label_name].unique().tolist()
    Y_target_classes.sort(reverse=False)#nothing must be the first
    Logger.logr.debug(f"Label classes: {Y_target_classes}")
    raw_df[label_name] = raw_df[label_name].map(Y_target_classes.index)

    if len(Y_target_classes) == 2:
        neg, pos = np.bincount(raw_df[label_name])
        total = neg + pos
        print('Examples:\n    Total: {}\n    Positive: {} ({:.2f}% of total)\n'.format(
            total, pos, 100 * pos / total))
    else:
        Logger.logr.info(f"Label classes is NOT 2 (pos/neg) Label classes:: {Y_target_classes}")

    return raw_df


def clean_redifine_df(raw_df):
    cleaned_df = raw_df.copy()

    # You don't want the `Time` column.
    if 'Date' in cleaned_df.columns:
        cleaned_df['Date'] = pd.to_datetime(cleaned_df['Date']).map(pd.Timestamp.timestamp)
    #cleaned_df = cleaned_df[COLUMNS_VALIDS]
    cleaned_df = cleaned_df.drop(columns= Utils_col_sele.DROPS_COLUMNS, errors='ignore')
    if 'ticker' in cleaned_df.columns:
        cleaned_df = pd.get_dummies(cleaned_df, columns = [ 'ticker'])
        #Si solo hay una accion no hace falta que ponga ticker_U ticker_PYPL
        filter_col = [col for col in cleaned_df if col.startswith('ticker_')]
        if len(filter_col) == 1:
            cleaned_df = cleaned_df.rename({filter_col[0]: 'ticker'}, axis='columns')

    cleaned_df = cleaned_df.dropna()

    return cleaned_df


def scaler_Raw_TF_onbalance(test_df, label_name = 'buy_sell_point'):
    test_labels = np.array(test_df.pop(label_name))
    test_features = np.array(test_df)
    scaler = StandardScaler()
    test_features = scaler.fit_transform(test_features)
    test_features = np.clip(test_features, -5, 5)
    Logger.logr.debug('Test labels shape:'+ str( test_labels.shape))
    Logger.logr.debug('Test features shape:'+ str(  test_features.shape))
    return test_features,  test_labels

def scaler_split_TF_onbalance(cleaned_df, label_name = 'buy_sell_point'):
    # Use a utility from sklearn to split and shuffle your dataset.
    train_df, test_df = train_test_split(cleaned_df, test_size = 0.28, shuffle=False)
    train_df, val_df = train_test_split(train_df, test_size = 0.28, shuffle=False)
    # Form np arrays of labels and features.
    train_labels = np.array(train_df.pop(label_name))
    bool_train_labels = train_labels != 0
    val_labels = np.array(val_df.pop(label_name))
    test_labels = np.array(test_df.pop(label_name))
    train_features = np.array(train_df)
    val_features = np.array(val_df)
    test_features = np.array(test_df)
    scaler = StandardScaler()
    train_features = scaler.fit_transform(train_features)
    val_features = scaler.transform(val_features)
    test_features = scaler.transform(test_features)
    train_features = np.clip(train_features, -5, 5)
    val_features = np.clip(val_features, -5, 5)
    test_features = np.clip(test_features, -5, 5)

    Logger.logr.info('Training labels shape:'+ str( train_labels.shape))
    Logger.logr.debug('Validation labels shape:'+ str( val_labels.shape))
    Logger.logr.debug('Test labels shape:'+ str( test_labels.shape))
    Logger.logr.debug('Training features shape:'+ str( train_features.shape))
    Logger.logr.debug('Validation features shape:'+ str( val_features.shape))
    Logger.logr.debug('Test features shape:'+ str( test_features.shape))

    return train_labels, val_labels, test_labels, train_features, val_features, test_features, bool_train_labels


def make_model_TF_onbalance(shape_features, metrics=METRICS_ALL, output_bias=None):
  if output_bias is not None:
    output_bias = keras.initializers.Constant(output_bias)
  model = keras.Sequential([
      keras.layers.Dense(
          16, activation='relu',
          input_shape=(shape_features,)),
      keras.layers.Dropout(0.5),
      keras.layers.Dense(1, activation='sigmoid',
                         bias_initializer=output_bias),
  ])

  model.compile(
      optimizer=keras.optimizers.Adam(learning_rate=1e-3),
      loss=keras.losses.BinaryCrossentropy(),
      metrics=metrics)

  return model


def make_model_TF_onbalance_fine_28(shape_features, metrics=METRICS_ACCU_PRE, output_bias=None):
  if output_bias is not None:
    output_bias = keras.initializers.Constant(output_bias)
  model = keras.Sequential([
      keras.layers.Dense(28, activation='relu',input_shape=(shape_features,)),
      keras.layers.Dropout(0.2),
      keras.layers.Dense(1, activation='relu',bias_initializer=output_bias),
  ])

  model.compile(
      optimizer=keras.optimizers.Adam(learning_rate=0.001),
      loss=keras.losses.BinaryCrossentropy(),
      metrics=metrics)

  return model

def make_model_TF_onbalance_fine_64(shape_features,metrics=METRICS_ACCU_PRE, output_bias=None):
  if output_bias is not None:
    output_bias = keras.initializers.Constant(output_bias)
  model = keras.Sequential([
      keras.layers.Dense(64, activation='relu',input_shape=(shape_features,)),
      keras.layers.Dense(32, activation='relu', input_shape=(shape_features,)),
      keras.layers.Dropout(0.2),
      keras.layers.Dense(4, activation='relu', input_shape=(shape_features,)),
      keras.layers.Dense(1, activation='relu',bias_initializer=output_bias),
  ])

  model.compile(
      optimizer=keras.optimizers.Adam(learning_rate=0.001),
      loss=keras.losses.BinaryCrossentropy(),
      metrics=metrics)

  return model


def get_resampled_ds_onBalance(train_features, train_labels, bool_train_labels, BATCH_SIZE):
    # Oversample the minority class
    # A related approach would be to resample the dataset by oversampling the minority class.
    pos_features = train_features[bool_train_labels]
    neg_features = train_features[~bool_train_labels]
    pos_labels = train_labels[bool_train_labels]
    neg_labels = train_labels[~bool_train_labels]
    # You can balance the dataset manually by choosing the right number of random
    # indices from the positive examples:
    ids = np.arange(len(pos_features))
    choices = np.random.choice(ids, len(neg_features))
    res_pos_features = pos_features[choices]
    res_pos_labels = pos_labels[choices]
    res_pos_features.shape
    resampled_features = np.concatenate([res_pos_features, neg_features], axis=0)
    resampled_labels = np.concatenate([res_pos_labels, neg_labels], axis=0)
    order = np.arange(len(resampled_labels))
    np.random.shuffle(order)
    resampled_features = resampled_features[order]
    resampled_labels = resampled_labels[order]
    resampled_features.shape
    """#### Using `tf.data`

    If you're using `tf.data` the easiest way to produce balanced examples is to start with a `positive` and a `negative` dataset, and merge them. See [the tf.data guide](../../guide/data.ipynb) for more examples.
    """
    BUFFER_SIZE = 100000

    def make_ds(features, labels):
        ds = tf.data.Dataset.from_tensor_slices((features, labels))  # .cache()
        ds = ds.shuffle(BUFFER_SIZE).repeat()
        return ds

    pos_ds = make_ds(pos_features, pos_labels)
    neg_ds = make_ds(neg_features, neg_labels)
    # Each dataset provides `(feature, label)` pairs:
    # for features, label in pos_ds.take(1):

    # Merge the two together using `tf.data.Dataset.sample_from_datasets`:
    resampled_ds = tf.data.Dataset.sample_from_datasets([pos_ds, neg_ds], weights=[0.5, 0.5])
    resampled_ds = resampled_ds.batch(BATCH_SIZE).prefetch(2)
    for features, label in resampled_ds.take(1):
        print(label.numpy().mean())

    return resampled_ds

Y_TARGET = 'buy_sell_point'
def __prepare_get_all_result_df(X_test, y_test):
    df_re = X_test[['Date', "Close", "per_Close", 'has_preMarket', 'Volume']].copy()
    list_ticker_stocks = [col for col in X_test.columns if
                          col.startswith('ticker_')]  # todas las que empiecen por ticker_ , son variables tontas
    if (list_ticker_stocks is not None) and len(list_ticker_stocks) > 0:
        df_re['ticker'] = X_test[list_ticker_stocks].idxmax(axis=1).copy()  # undo dummy variable
        df_re[Y_TARGET] = y_test.copy()
        df_re = df_re[['Date', Y_TARGET, 'ticker', "Close", "per_Close", 'has_preMarket', 'Volume']]
    else:
        df_re[Y_TARGET] = y_test.copy()
        df_re = df_re[['Date', Y_TARGET,  "Close", "per_Close", 'has_preMarket', 'Volume']]

    df_re = df_re.loc[:,~df_re.columns.duplicated()].copy() #quitar remove duplicates duplicadas
    return df_re.copy()


def fill_first_time_df_result_all(df):
    global df_result_all
    X = df.drop(columns=Y_TARGET)  # iloc[:,:-1] df.iloc[:,:-1] #iloc[:,:-1]
    y = df[Y_TARGET]  # df.iloc[:,-1] #.iloc[:,-1] #.iloc[:,-1]
    # X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.28, shuffle=False)
    X_test = X.copy()
    y_test = y
    df_result = X.copy()
    # PARA organizar la salida en el df_result de los resultados
    return __prepare_get_all_result_df(X_test, y_test)

def get_df_for_list_of_result(df_full):
    df_list_r = pd.DataFrame()
    list_ticker_stocks = [col for col in df_full.columns if
                          col.startswith('ticker_')]  # todas las que empiecen por ticker_ , son variables tontas
    if (list_ticker_stocks is not None) and len(list_ticker_stocks) > 0:
        df_full['ticker'] = df_full[list_ticker_stocks].idxmax(axis=1).copy()  # undo dummy variable
        df_list_r = df_full[['Date', Y_TARGET, 'ticker', "Close", 'has_preMarket', 'Volume']].copy()
    else:
        df_list_r = df_full[['Date', Y_TARGET, "Close", 'has_preMarket', 'Volume']].copy()
    return df_list_r