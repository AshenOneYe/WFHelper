# WFHelper
世界弹射物语护肝宝，24小时自动混铃铛共斗

## Feature
轻量级项目，无需复杂CV库和深度学习库
低开销，图片比对基于pHash匹配，有效提高运行效率，减少计算
兼具高精度和容错率

缺点：无法适配不同分辨率

## Usage

环境配置

> 1. 安装配置python3环境
> 2. 安装依赖库 `pip install imagehash`
> 3. 安装adb并配置adb到环境变量


由于不同设备分辨率不同，需要参考template目录，将其中的截图替换为自己手机的截图，具体来说：
> 1. 使用命令`python .\main.py -s template\picture.png`进行截图，其中`picture.png`为目标文件名，最好和template目录中的文件名一致
> 2. 当连接多个设备时使用`-d`参数来指定设备名称，设备名称可以通过`adb devices`获取
> 3. 完成截图后修改`Config.py`文件，将所有的area修改为对应截图的对应按钮范围，比如`canjia.png`的area，即为参加按钮的左上角x,y坐标和右下角x,y坐标

配置完成后输入`python .\main.py`即可开始挂机

对于一加9R用户：
完成环境配置后，确保手机开启全面屏即可省略截图环节

## 效果如图
![Demo](pics/demo.jpg)