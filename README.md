# 中国A股数据分析平台

一个基于Streamlit开发的A股数据分析可视化平台，提供实时数据查询、可视化分析和AI辅助分析功能。

## 功能特点

1. 数据查询与展示
   - 股票基本信息查询
   - 历史行情数据(支持前复权、后复权、不复权)
   - 实时资金流向分析
   - 龙虎榜数据展示

2. 数据可视化
   - 交互式K线图展示
   - 成交量分析图表
   - 资金流向趋势图
   - 主力资金分析图表

3. AI智能分析
   - 基于LangChain的智能分析报告
   - 使用Ollama模型生成投资建议
   - 技术面和资金面综合分析

## 主要模块

1. 基础数据模块
   - 公司基本信息(股票代码、简称、行业等)
   - 市值信息(总市值、流通市值等)
   - 财务指标(市盈率、市净率等)
   - 交易信息(振幅、换手率等)

2. 行情分析模块
   - K线图展示与分析
   - 成交量分析
   - 价格趋势分析
   - 技术指标统计

3. 资金流向模块
   - 主力资金净流入分析
   - 超大单/大单/小单资金分析
   - 历史资金流向趋势
   - 主力资金占比分析

4. 龙虎榜模块
   - 近期龙虎榜数据展示
   - 机构席位交易明细
   - 上榜原因分析

## 技术架构

- 前端框架: Streamlit
- 数据源: AKShare金融数据接口
- 数据分析: Pandas
- 数据可视化: Plotly
- AI模型: LangChain + Ollama

## 使用说明

1. 数据查询
   - 输入股票代码(例如: 600126)
   - 选择时间范围
   - 选择复权方式
   - 点击"获取数据"按钮

2. 数据分析
   - 查看基本信息和统计数据
   - 浏览K线图和成交量图表
   - 分析资金流向趋势
   - 查看龙虎榜数据

3. AI分析报告
   - 点击"生成股票分析报告"
   - 等待AI模型分析完成
   - 查看综合分析结果和投资建议

## 数据更新说明

- 基础数据: 实时更新
- 行情数据: 每日收盘后更新
- 资金流向: T+1更新
- 龙虎榜数据: T+1更新

## 注意事项

- 所有数据仅供参考，不构成投资建议
- 历史数据存在一小时缓存，减少API调用
- AI分析报告基于历史数据，需要结合实际情况判断
- 建议在交易时段使用，以获取最新数据

## 后续规划

1. 功能扩展
   - 添加更多技术指标分析
   - 扩展板块及行业分析
   - 增加股票筛选功能
   - 添加自定义分析策略

2. 性能优化
   - 优化数据加载速度
   - 改进缓存机制
   - 提升AI分析效率

3. 用户体验
   - 优化界面布局
   - 添加更多交互功能
   - 完善数据导出功能