# NeuroStudioRehab 架构笔记

> 源码仓库：`E:\code\NeuroStudioRehab`  
> 产品：脑机接口肢体康复桌面软件（Qt/C++17 + 嵌入式 Python/MNE）  
> 文档生成目的：梳理分层、组件关系与典型数据流，便于 onboarding 与排错。

## 文档索引

| 文件 | 内容 |
|------|------|
| [01-分层与模块架构.md](./01-分层与模块架构.md) | 目录分层、依赖方向、构建单元 |
| [02-主界面与工作区协调.md](./02-主界面与工作区协调.md) | MainWindow 布局、Config/Content、EEGWorkspaceCoordinator |
| [03-Session状态与事件总线.md](./03-Session状态与事件总线.md) | WorkspaceState、DataManagerController、AppEventBus |
| [04-实时采集与硬件数据流.md](./04-实时采集与硬件数据流.md) | Hardware、Settings、采集链、触发、录制 |
| [05-离线处理与可视化.md](./05-离线处理与可视化.md) | Pipeline、CppBridge、EegPlotKit、Plot |
| [06-插件Survey与Rehab.md](./06-插件Survey与Rehab.md) | IApplicationPlugin、量表任务、康复模块 |
| [07-关系图与排错清单.md](./07-关系图与排错清单.md) | Mermaid 总图、常见问题排查顺序 |

仓库内同步维护的专题文档（可对照阅读）：

- `docs/EEG_WORKSPACE.md` — Config/Content 职责
- `docs/SESSION_WORKFLOW.md` — Session 写入与 Bus 映射
- `docs/HARDWARE_DEVICE_CUTOVER.md` — Hardware 取代 Device legacy
