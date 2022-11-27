"""https://github.com/Leci37/LecTrade LecTrade is a tool created by github user @Leci37. instagram @luis__leci Shared on 2022/11/12 .   . No warranty, rights reserved """

from enum import Enum
Y_TARGET = 'buy_sell_point'

# **DOCU**
# 0.3 In the file a_manage_stocks_dict.py all the configurations are stored, take a look and know where it is.
# In it there is the dictionary DICT_COMPANYS
# Which contains the IDs (google quotes with the ID: GOOG) of the companies to analyze can be customized and create class from the nasdaq tikers, by default will use the key @FOLO3 which will analyze these 39 companies.
DICT_COMPANYS = {
    "@FAV":
        ["MELI", "TWLO", "RIVN", "SNOW", "UBER", "U" , "PYPL", "GTLB", "MDB", "TSLA", "DDOG"],
    "@ROLL" :
        ["MELI", "TWLO","RIVN","SNOW", "UBER", "U" , "PYPL", "GTLB","MDB", "TSLA", "DDOG","SHOP", "NIO","RBLX", "TTD", "APPS", "ASAN",  "DOCN", "AFRM", "PINS"],
    "@VOLA" :
        ["UPST", "RIVN", "SNOW", "LYFT", "SPOT", "GTLB", "MDB", "HUBS", "TTD", "APPS", "ASAN", "AFRM", "DOCN", "DDOG", "SHOP", "NIO", "U", "RBLX"],
    #top LAS MÁS activas por Volumen  realizado por https://www.webull.com/quote/us/actives
    "@TOP200": #Xpath //p[@class="tit bold"]/text()   good side https://codebeautify.org/Xpath-Tester
        ["AMD", "TSLA", "AAPL", "MULN", "NVDA", "AMZN", "AGFY", "CCL", "NIO", "BAC",  "F", "INTC", "T", "FNHC", "VALE", "ACI", "ILAG", "IMRA", "PLTR", "SOFI", "AAL", "WFC", "NU", "JPM", "XPEV", "SHOP", "MSFT", "NOK", "DBGI", "C", "PBR", "CMCSA", "SNAP", "HBAN", "DNA", "PLUG", "SWN", "VZ", "LASE", "NCLH", "GOOGL", "PTON", "CEI", "PCG", "ZVO", "META", "LCID", "ABEV", "MMAT", "GOOG", "UBER", "RIVN", "DAL", "AMC", "DKNG", "WISH", "WBD", "MU", "UMC", "KR", "CSCO", "TSM", "USB", "GOLD", "OPEN", "NKLA", "PBTS", "OXY", "ARVL", "BEKE", "TLRY", "KMI", "BB", "PFE", "MPW", "FFIE", "GRAB", "SQ", "HPE", "CCJ", "ASX", "KEY", "KO", "MARA", "CSX", "RIG", "NFLX", "SIRI", "XOM", "BCS", "KGC", "CS", "RBLX", "SYTA", "LUMN", "CPG", "AGNC", "FCX", "NTNX", "COIN", "BABA", "MS", "INFY", "LU", "SCHW", "LYG", "AUY", "MRVL", "JD", "SMRT", "ACB", "ET", "GM", "PYPL", "PINS", "AFRM", "SLB", "PING", "NUTX", "MO", "HAL", "MRO", "UAL", "CGC", "TELL", "KHC", "NVTA", "HPQ", "CVE", "BP", "WBA", "RUN", "AMAT", "ERIC", "CVNA", "CLF", "TOP", "TWTR", "BMY", "RIOT", "MRK", "NEM", "IDEX", "X", "TFC", "LYFT", "BTG", "UEC", "RF", "PDD", "KDP", "DVN", "FCEL", "VTGN", "HST", "RTO", "NEE", "CPNG", "FTCH", "MF", "JBLU", "CARR", "COMS", "AG", "VRM", "FTI", "TEVA", "MOS", "ROKU", "CHPT", "DIS", "IBN", "ORCL", "QCOM", "VOD", "MDLZ", "GILD", "NLY", "NKE", "LI", "GFI", "BSX", "M", "HMY", "COP", "APA", "NYCB", "IQ", "HUT", "VTRS", "TXN", "AZN", "AMCR", "HL", "QS", "BBBY", "IMUX", "PATH", "CVX"],
    "@TOP100":
        ["AMD", "TSLA", "AAPL", "MULN", "NVDA", "AMZN", "AGFY", "CCL", "NIO", "BAC",  "F", "INTC", "T", "FNHC", "VALE", "ACI", "ILAG", "IMRA", "PLTR", "SOFI", "AAL", "WFC", "NU", "JPM", "XPEV", "SHOP", "MSFT", "NOK", "DBGI", "C", "PBR", "CMCSA", "SNAP", "HBAN", "DNA", "PLUG", "SWN", "VZ", "LASE", "NCLH", "GOOGL", "PTON", "CEI", "PCG", "ZVO", "META", "LCID", "ABEV", "MMAT", "GOOG", "UBER", "RIVN", "DAL", "AMC", "DKNG", "WISH", "WBD", "MU", "UMC", "KR", "CSCO", "TSM", "USB", "GOLD", "OPEN", "NKLA", "PBTS", "OXY", "ARVL", "BEKE", "TLRY", "KMI", "BB", "PFE", "MPW", "FFIE", "GRAB", "SQ", "HPE", "CCJ", "ASX", "KEY", "KO", "MARA", "CSX", "RIG", "NFLX", "SIRI", "XOM", "BCS", "KGC", "CS", "RBLX", "SYTA", "LUMN", "CPG", "AGNC", "FCX"],
    "@TOP50":
        ["AMD", "TSLA", "AAPL", "MULN", "NVDA", "AMZN", "AGFY", "CCL", "NIO", "BAC",  "F", "INTC", "T", "FNHC", "VALE", "ACI", "ILAG", "IMRA", "PLTR", "SOFI", "AAL", "WFC", "NU", "JPM", "XPEV", "SHOP", "MSFT", "NOK", "DBGI", "C", "PBR", "CMCSA", "SNAP", "HBAN", "DNA", "PLUG", "SWN", "VZ", "LASE", "NCLH", "GOOGL", "PTON", "CEI", "PCG", "ZVO", "META", "LCID", "ABEV"],
    "@TOP25":
        ["AMD", "TSLA", "AAPL", "MULN", "NVDA", "AMZN", "AGFY", "CCL", "NIO", "BAC", "ATXI", "F", "INTC", "T", "FNHC", "VALE", "ACI", "ILAG", "IMRA", "PLTR", "SOFI", "AAL", "WFC", "NU", "JPM"],

    #lista de seguimiento @FOLO1, lista Aux seguimiento @FOLO2 ambas @FOLO3 19/10/2022
    "@FOLO1":
        ["UPST", "MELI", "TWLO", "RIVN", "SNOW", "LYFT", "ADBE", "UBER", "ZI", "QCOM", "PYPL", "SPOT", "RUN", "GTLB", "MDB", "NVDA", "AMD", "ADSK", "AMZN", "BABA", "NFLX", "FFIV", "GOOG", "MSFT", "ABNB", "TSLA", "META"],
    "@FOLO2":
        ["DBX", "PTON", "CRWD", "NVST", "HUBS", "EPAM", "PINS", "TTD", "SNAP", "APPS", "ASAN", "AFRM", "DOCN", "ETSY", "DDOG", "SHOP", "NIO", "U", "GME", "RBLX", "CRSR"],
    "@FOLO3": #"META", ERROR no buy points "GOOG", "MSFT", "TSLA",
        [ "GOOG", "MSFT", "TSLA","UPST", "MELI", "TWLO", "RIVN", "SNOW", "LYFT", "ADBE", "UBER", "ZI", "QCOM", "PYPL", "SPOT", "RUN", "GTLB", "MDB", "NVDA", "AMD" , "ADSK", "AMZN", "CRWD", "NVST", "HUBS", "EPAM", "PINS", "TTD", "SNAP", "APPS", "ASAN", "AFRM", "DOCN", "ETSY", "DDOG", "SHOP", "NIO", "U", "GME", "RBLX", "CRSR"],
                #"PTON", error callearly no se xq
         #[  "CRWD", "NVST", "HUBS", "EPAM", "PINS", "TTD", "SNAP", "APPS", "ASAN", "AFRM", "DOCN", "ETSY", "DDOG", "SHOP", "NIO", "U", "GME", "RBLX", "CRSR"],
    "@CHIC":
        [ "ATHE", "MU", "CRM", "SNPS", "DHI", "MPWR", "CZR", "NOW", "BBWI", "DXCM", "TER", "KLAC", "ALGN", "CARV", "UONE", "SPG", "STAG", "O", "PSEC"],
    "@CHIC3":
        ["GOOG", "MSFT", "TSLA","UPST", "MELI", "TWLO", "RIVN", "SNOW", "LYFT", "ADBE", "UBER",  "ATHE", "MU", "CRM", "SNPS", "DHI", "MPWR", "CZR", "NOW", "BBWI", "DXCM", "TER", "KLAC", "ALGN", "CARV", "UONE", "SPG", "STAG", "O", "PSEC"]
    }

PATH_REGISTER_RESULT_REAL_TIME = "d_result/prediction_real_time.csv"
MIN_SCALER = 0
MAX_SCALER = 1

class MODEL_TYPE_COLM(Enum):
    VGOOD = "_vgood16_"
    GOOD = "_good9_"
    REG = "_reg4_"
    LOW = "_low1_"

class Option_Historical(Enum):
    YEARS_3 = 1
    MONTH_3 = 2
    MONTH_3_AD = 3
    DAY_6 = 4
    DAY_1 = 5

class ExtendedEnum(Enum):
    @classmethod
    def list_values(cls):
        return list(map(lambda c: c.value, cls))
    @classmethod
    def list(cls):
        return list(map(lambda c: c, cls))
class Op_buy_sell(ExtendedEnum):
    BOTH = "both"
    POS = "pos"
    NEG = "neg"

class MODEL_TF_DENSE_TYPE_MULTI_DIMENSI(Enum):
    @classmethod
    def list_values(cls):
        return list(map(lambda c: c.value, cls))
    @classmethod
    def list(cls):
        return list(map(lambda c: c, cls))
    SIMP_DENSE28 = "mult_28"
    SIMP_DENSE64 = "mult_64"
    SIMP_DENSE128 =  "mult_128"
    SIMP_CONV2 = "mult_conv2"
    SIMP_CONV	= "mult_conv"
    SIMP_CORDO	= "_simp_cordo"
    #SIMP_DENSE	= "_simp_dense"
    #MULT_DENSE	= "_mult_dense"
    MULT_LINEAR	= "mult_linear"
    MULT_DENSE2	= "mult_dense2"
    #MULT_CONV	= "_mult_conv" #error al save()
    MULT_LSTM	= "mult_lstm"  #  MAÑANA
    ####SIMPL_BIDI	= "_simpl_bidi"
    # MULT_TIME	= "_mult_time"
    MULT_GRU	= "_mult_gru" #  MAÑANA


class MODEL_TF_DENSE_TYPE_ONE_DIMENSI(Enum):
    @classmethod
    def list_values(cls):
        return list(map(lambda c: c.value, cls))
    @classmethod
    def list(cls):
        return list(map(lambda c: c, cls))
    SIMP_28 = "s28"
    SIMP_64 = "s64"
    SIMP_128 =  "s128"

#In case of does not have a value form webull.com , the tool to obtains news code: Utils/Volume_WeBull_get_tikcers.py
DICT_WEBULL_ID = {
    #@CRPTO
    "BTC-USD" : 950160802,
    "ETH-USD" : 950160804,
    "DASH-USD" : 950181555,
    "LTC-USD" : 950160801,
    "ADA-USD" : 950185924,
    "XLM-USD" : 950181553,
    "ZEC-USD" : 950181635,
    "LINK-USD" : 950188154,
    "DOGE-USD" : 950181551,
    #@FOLO3
    "UPST" : 950177837,
    "MELI" : 913323930,
    "TWLO" : 913254831,
    "RIVN" : 950188536,
    "SNOW" : 950173560,
    "LYFT" : 950116149,
    "ADBE" : 913256192,
    "UBER" : 950121423,
    "ZI" : 950157730,
    "QCOM" : 913323878,
    "PYPL" : 913256043,
    "SPOT" : 925418520,
    "RUN" : 913256036,
    "GTLB" : 950188178,
    "MDB" : 925377113,
    "NVDA" : 913257561,
    "AMD" : 913254235,
    "ADSK" : 913256187,
    "AMZN" : 913256180,
    "BABA" : 913254558,
    "NFLX" : 913257027,
    "FFIV" : 913256674,
    "GOOG" : 913303964,
    "MSFT" : 913323997,
    "ABNB" : 950178075,
    "TSLA" : 913255598,
    "META" : 913303928,
    "DBX" : 925418496,
    "PTON" : 950138392,
    "CRWD" : 950126602,
    "NVST" : 950135009,
    "HUBS" : 913254682,
    "EPAM" : 913254390,
    "PINS" : 950118597,
    "TTD" : 913431510,
    "SNAP" : 925186755,
    "APPS" : 913253434,
    "ASAN" : 950172459,
    "AFRM" : 950178219,
    "DOCN" : 950181409,
    "ETSY" : 913255993,
    "DDOG" : 950136998,
    "SHOP" : 913254746,
    "NIO" : 950076017,
    "U" : 950172451,
    "GME" : 913255341,
    "RBLX" : 950178170,
    "CRSR" : 950172441,
    #@CHIC
    "ATHE" : 913323301,
    "MU" : 913324077,
    "CRM" : 913255140,
    "SNPS" : 913323483,
    "DHI" : 913255191,
    "MPWR" : 913323959,
    "CZR" : 913255942,
    "NOW" : 913254427,
    "BBWI" : 913255499,
    "DXCM" : 913256616,
    "TER" : 913324414,
    "KLAC" : 913257399,
    "ALGN" : 913256164,
    "CARV" : 913253685,
    "UONE" : 913323315,
    "SPG" : 913324356,
    "STAG" : 913254301,
    "O" : 913324022,
    "PSEC" : 913323566}



