# import json
from src.packthub.packthub import PacktHub


duties = {
"PacktHub" : "runJob"
}

if __name__ == '__main__':
    for key, value in duties.items():
        tmp_class = eval(key + "()")
        eval("tmp_class." + value + "()")
        eval("tmp_class." + 'getStatus' + "()")
