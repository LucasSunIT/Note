Power Spectral Density (PSD)  功率谱
projector : signal space projector (SSP) 是一种数学方法 去除EEG MEG 数据中的噪声 和 伪迹
（常见用途 眼电伪迹EOG 心电伪迹ECG 外部磁场干扰）
togging = on/off  on: 显示去噪后的数据 off: 原始数据
projector toggling
 (ICA) 独立成分分析： 一种灵活的盲源分离算法  把混在一起的不同信号拆开 在挑出那些 属于噪声的成分去掉


预处理技术
Maxwell filtering  麦克斯韦滤波
Signal-space projection （SSP） 信号空间投影
Independent Components Analysis (ICA) 独立成分分析
Filtering 滤波（取消某些频段的噪声 High Pass(去掉慢漂移 如0.1 hz以下) Low pass （去掉高频噪声 如 >40 hz）
                Band Pass(保留指定频段 如1-40hz) Notch(陷波滤波 去掉特定频率 如 50HZ/60HZ 电源干扰）)

Downsampling 降采样 减少采样率 比如从1000HZ ---> 250 HZ
典型的处理流程 ： 原始数据、滤波、去噪、Epoch、Analyse(特征提取、平均 时频分析 脑区绘图 统计检验 机器学习)

Detecting experimental events  事件检测
在设备中 有一个或者多个专门的刺激通道 STIM channals 记录的是从实验控制 电脑发出的数字信号 trigger 脉冲 这些信号在脑电信号表现为 短暂的方波 squarewave pulses
电压阶跃 brief DC shift  每个不同的脉冲电压对应一种事件类型
Evoked 针对特定事件 经过平均后的脑电、脑磁信号  是由多个 epochs 平均而来 常用于分析 ERP ERF  事件相关电位 事件相关磁场

🧠 一、大脑主要叶（Lobes）及功能
人类大脑大体分为 四个主要脑叶（lobes），加上几个功能性结构区域：
脑区
英文
主要功能
常见 ERP 来源
枕叶
Occipital lobe
视觉加工（形状、颜色、运动等）
P1、N1（视觉）
颞叶
Temporal lobe
听觉加工、语言理解、记忆
N1（听觉）、N400（语义）
顶叶
Parietal lobe
空间感知、注意、感觉整合
P3（注意、目标识别）
额叶
Frontal lobe
决策、执行控制、情绪、运动计划
ERN（错误监控）、CNV（准备电位）

ERP 成分
主要脑区来源
功能含义
P1、N1（视觉）
枕叶
视觉感知加工
N1（听觉）
颞叶
听觉识别
P2、P3
顶叶
注意与目标识别
ERN、CNV
前额叶/扣带回
错误监控、准备
N400
颞叶-顶叶联合区
语义加工

区域
英文
功能
前额叶皮层
Prefrontal Cortex
高级认知（计划、推理、判断、工作记忆）
中央沟
Central Sulcus
分隔额叶和顶叶，是运动区与体感区的界限
运动皮层
Motor Cortex
控制身体运动
体感皮层
Somatosensory Cortex
接收身体感觉（触觉、温度、痛觉）
扣带回
Cingulate Cortex
注意、情绪、错误检测（ERP 的 ERN 来源之一）
海马
Hippocampus
学习与记忆形成
小脑
Cerebellum
协调运动和平衡，有时也参与认知功能



一、多文件组成的 EEG 数据格式（必须一起使用）
数据格式
文件后缀
说明
BrainVision
.vhdr, .vmrk, .eeg
三个文件组成：.vhdr 是头文件，.vmrk 是事件标记，.eeg 是数据。必须成组存在。
EEGLAB
.set, .fdt
.set 是主文件，描述数据结构；.fdt 存储二进制 EEG 数据。某些 .set 文件可独立存在（数据嵌入其中）。
Persyst EEG
.lay, .dat
.lay 是头文件（通道、采样率等），.dat 是原始数据。必须成对存在。
Nihon Kohden EEG
.eeg, .21e, .pnt, .log
Nihon Kohden 专用格式，多个文件共同组成一个完整记录。 .eeg 为主要信号文件。
EGI MFF
.mff（文件夹）
实际是一个目录，内部包含多个 XML 和 bin 文件。整体作为一个数据集使用。


二、单文件 EEG 数据格式（一个文件就是一个数据集）
数据格式
文件后缀
说明
European data format (EDF)
.edf
通用的 EEG 医疗数据格式
BioSemi data format (BDF)
.bdf
EDF 扩展版本，BioSemi 专用
General data format (GDF)
.gdf
通用 EEG 格式，含更多事件信息
Neuroscan CNT
.cnt
Neuroscan 连续 EEG 文件
ANT Neuro CNT
.cnt
ANT Neuro 设备使用的 CNT 文件
EGI simple binary
.egi
EGI 旧版二进制格式
Nicolet
.data
Nicolet EEG 系统专用格式
eXimia EEG
.nxe
eXimia 系统专用格式
XDF data
.xdf, .xdfz
LabRecorder 常见格式，可包含多通道同步数据
Curry8 data
.cdt, .ceo, .dpo
Curry 软件生成的 EEG 数据格式


F： 额叶（Frontal）

C： 中央（Central）

P： 顶叶（Parietal）

O： 枕叶（Occipital）

T： 颞叶（Temporal）

奇数：左侧，偶数：右侧，中线用 Z（如 Fz、Cz）

脑电节律（频率波段）

波段
频率
特点/功能
δ 波
0.5–4 Hz
深睡眠、无意识状态
θ 波
4–8 Hz
浅睡眠、记忆编码、任务准备
α 波
8–13 Hz
放松闭眼、抑制背景活动
β 波
13–30 Hz
活跃思维、注意、运动准备
γ 波
30–100 Hz
高级认知、信息整合、意识相关


事件相关电位（ERP）

大脑对特定事件或刺激的时间锁定电位变化
 通过多次刺激试次平均得到，增强信号、降低噪声

常见 ERP 成分

成分
时间（ms）
极性
典型脑区
功能
P1
~100
正
枕叶
视觉刺激早期加工
N1
~150
负
枕叶 / 颞叶
感觉辨别、注意分配
P2
~200
正
颞顶叶
感觉整合
P3 / P300
~300
正
顶叶
注意与目标识别、工作记忆
N400
~400
负
颞叶 / 顶叶
语义加工、语言理解
ERN
~100（反应后）
负
前额叶 / 扣带回
错误检测、行为监控


sreq 采样速率   freq绘图中显示的频率坐标点

freq 范围通常是 (0 - sfreq / 2)

























