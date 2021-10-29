from os import path
from ImageUtil import getImageHash

class Config():
    lingdangPath = "images\lingdang.png"
    lingdangArea = (30,157,111,237)
    lingdangPos = ((lingdangArea[0]+lingdangArea[2])/2,((lingdangArea[1]+lingdangArea[3])/2))
    lingdangHash = getImageHash(path=lingdangPath)

    canjiaPath = "images\canjia.png"
    canjiaArea = (557,1792,1000,1906)
    canjiaPos = ((canjiaArea[0]+canjiaArea[2])/2,((canjiaArea[1]+canjiaArea[3])/2))
    canjiaHash = getImageHash(path=canjiaPath)

    zhunbeiPath = "images\zhunbei.png"
    zhunbeiArea = (311,1567,770,1710)
    zhunbeiPos = ((zhunbeiArea[0]+zhunbeiArea[2])/2,((zhunbeiArea[1]+zhunbeiArea[3])/2))
    zhunbeiHash = getImageHash(path=zhunbeiPath)

    yijingkaishiOKPath = "images\yijingkaishiOK.png"
    yijingkaishiOKArea = (316,1422,760,1528)
    yijingkaishiOKPos = ((yijingkaishiOKArea[0]+yijingkaishiOKArea[2])/2,((yijingkaishiOKArea[1]+yijingkaishiOKArea[3])/2))
    yijingkaishiOKHash = getImageHash(path=yijingkaishiOKPath)

    manyuanOKPath = "images\manyuanOK.png"
    manyuanOKArea = (316,1422,760,1528)
    manyuanOKPos = ((manyuanOKArea[0]+manyuanOKArea[2])/2,((manyuanOKArea[1]+manyuanOKArea[3])/2))
    manyuanOKHash = getImageHash(path=manyuanOKPath)

    jixuPath = "images\jixu.png"
    jixuArea = (368,1995,711,2090)
    jixuPos = ((jixuArea[0]+jixuArea[2])/2,((jixuArea[1]+jixuArea[3])/2))
    jixuHash = getImageHash(path=jixuPath)

    likaiPath = "images\likai.png"
    likaiArea = (151,1996,493,2090)
    likaiPos = ((likaiArea[0]+likaiArea[2])/2,((likaiArea[1]+likaiArea[3])/2))
    likaiHash = getImageHash(path=likaiPath)

    jixuguankaPath = "images\jixuguanka.png"
    jixuguankaArea = (563,1429,1003,1533)
    jixuguankaPos = ((jixuguankaArea[0]+jixuguankaArea[2])/2,((jixuguankaArea[1]+jixuguankaArea[3])/2))
    jixuguankaHash = getImageHash(path=jixuguankaPath)
    

    

    