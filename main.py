import streamlit as st
import akshare as ak
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import datetime
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_community.llms import Ollama

# 页面配置
st.set_page_config(page_title="中国A股数据分析平台", layout="wide")

# 添加缓存装饰器

# 获取股票历史数据
@st.cache_data(ttl=3600)  # 缓存1小时
def get_stock_history(symbol, start_date, end_date, adjust):
    """获取股票历史数据"""
    return ak.stock_zh_a_hist(
        symbol=symbol,
        period="daily",
        start_date=start_date,
        end_date=end_date,
        adjust=adjust
    )

# 获取股票基本信息
@st.cache_data(ttl=3600)
def get_stock_info(symbol):
    """获取股票基本信息"""
    return ak.stock_individual_info_em(symbol=symbol)

# 获取龙虎榜数据
@st.cache_data(ttl=3600)
def get_stock_lhb_detail(start_date, end_date):
    """获取龙虎榜数据"""

    return ak.stock_lhb_detail_em(start_date=start_date, end_date=end_date)

# 获取东方财富个股资金流向数据
@st.cache_data(ttl=3600)
def get_stock_individual_fund_flow_df(stock_code):
    """获取东方财富个股资金流向数据"""
    try:
        # 判断市场类型
        market = "sh" if stock_code.startswith("6") else "sz"
        df = ak.stock_individual_fund_flow(stock=stock_code, market=market)
        if df is None or df.empty:
            return None
        return df
    except Exception as e:
        st.error(f"获取个股资金流向数据失败: {str(e)}")
        return None

# 生成股票分析报告
def generate_analysis_report(stock_df,flow_df):
        # 定义信息抽取器
        template = """
        你是一个专业的股票分析师，擅长从股票数据中提取有价值的信息。
        请根据以下数据，生成一份关于{stock_code}股票的分析报告。
        并提供投资建议，包括买入、卖出或持有的中长期趋势。
        

        数据：
        
        """

        # 创建提示模板
        prompt = PromptTemplate(
            template=template,
            input_variables=["stock_df","flow_df"]
        )
        
        # 使用Ollama作为LLM
        llm = Ollama(model="deepseek-r1:7b", temperature=0.7)
        output_parser = StrOutputParser()
        chain = prompt | llm | output_parser
        
        return chain.invoke({"stock_df": stock_df,"flow_df":flow_df})


# 标题和说明
# st.title('陈超的中国A股数据分析平台')

st.markdown("""
<div style='background-color: #f0f2f6; padding: 20px; border-radius: 10px; margin: 10px 0;'>
    <h3 style='color: #1f77b4; text-align: center; margin-bottom: 15px;'>陈超的中国A股数据分析平台</h3>
    <p style='text-align: center; line-height: 2; color: #2c3e50; font-size: 1.1em; font-family: "STKaiti", "楷体", serif;'>
        <span style='display: block; margin: 10px 0;'>平阳之耀，</span>
        <span style='display: block; margin: 10px 0;'>顺溪守护者，</span>
        <span style='display: block; margin: 10px 0;'>财富镇守者与金权之主，</span>
        <span style='display: block; margin: 10px 0;'>钢骨铁躯与十挫不折之躯，</span>
        <span style='display: block; margin: 10px 0;'>双嗣血脉的奠基人，</span>
        <span style='display: block; margin: 10px 0;'>玄铁麒麟之子，</span>
        <span style='display: block; margin: 10px 0;'>百战涅槃者，</span>
        <span style='display: block; margin: 10px 0;'>股海真龙与财富统御者，</span>
        <span style='display: block; margin: 10px 0;'>断骨重铸的钢心战神，</span>
        <span style='display: block; margin: 10px 0;'>鳌江流域的荣耀象征，</span>
        <span style='display: block; margin: 10px 0;'>金靴永驻的玄甲门神，</span>
        <span style='display: block; margin: 10px 0;'>钢钉铸魂的陈氏麒麟儿·超</span>
    </p>
    <div style='text-align: center; margin-top: 20px; padding-top: 15px; border-top: 1px solid #ccc; color: #34495e;'>
        提供A股数据查询、分析和可视化功能
    </div>
</div>
""", unsafe_allow_html=True)



# 侧边栏配置
with st.sidebar:

    st.header("查询配置")
    stock_code = st.text_input('股票代码（例如：600126）', '600126')
    
    # 日期选择
    today = datetime.date.today()
    start_date = st.date_input('开始日期', today - datetime.timedelta(days=365))
    end_date = st.date_input('结束日期', today)
    
    # 复权选择
    adjust = st.selectbox('复权方式', ['qfq', 'hfq', ''],
                         format_func=lambda x: {'qfq': '前复权', 'hfq': '后复权', '': '不复权'}[x])

# 主要内容
try:
    if 'stock_data' not in st.session_state:
        st.session_state.stock_data = None
        st.session_state.stock_info = None

    # 确保在点击"获取数据"按钮后才执行数据获取
    if st.sidebar.button('获取数据', key="get_data"):  # 添加唯一的key
        with st.spinner("正在获取数据..."):
            # 获取个股信息并存储在session state中
            st.session_state.stock_info = get_stock_info(stock_code)
            # 获取股票数据并存储在session state中
            st.session_state.stock_data = get_stock_history(
                stock_code,
                start_date.strftime('%Y%m%d'),
                end_date.strftime('%Y%m%d'),
                adjust
            )
            st.success("数据获取成功！")

    # 检查数据是否存在
    if st.session_state.stock_data is not None and st.session_state.stock_info is not None:
        stock_info = st.session_state.stock_info
        individual_df = st.session_state.stock_data

        # 显示个股信息
        st.subheader("🏢 公司基本信息")
        
        # 创建4列布局
        cols = st.columns(4)
        
        # 定义要显示的信息组
        info_groups = [
            {
                "title": "公司信息",
                "items": ['股票简称', '股票代码', '行业', '上市时间']
            },
            {
                "title": "市值信息",
                "items": ['总市值', '流通市值', '总股本', '流通股本']
            },
            {
                "title": "财务指标",
                "items": ['市盈率-动态', '市净率', '每股收益', '每股净资产']
            },
            {
                "title": "交易信息",
                "items": ['振幅', '换手率', '量比', '成交量']
            }
        ]
        
        # 显示信息块
        for col, info_group in zip(cols, info_groups):
            with col:
                st.markdown(f"**{info_group['title']}**")
                for item in info_group['items']:
                    try:
                        value = stock_info.loc[stock_info['item'] == item, 'value'].values[0]
                        # 对特定字段进行格式化
                        if item in ['总市值', '流通市值']:
                            value = f"¥{float(value)/100000000:.2f}亿"
                        elif item in ['总股本', '流通股本']:
                            value = f"{float(value)/100000000:.2f}亿股"
                        elif item in ['换手率', '量比']:
                            value = f"{float(value):.2f}%"
                        st.markdown(f"- {item}：{value}")
                    except:
                        st.markdown(f"- {item}：--")
                st.markdown("---")

        # 显示统计数据
        st.subheader("📊 数据统计")
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("最新收盘价", f"¥{individual_df['收盘'].iloc[-1]:.2f}",
                     f"{(individual_df['收盘'].iloc[-1] - individual_df['收盘'].iloc[-2]):.2f}")
        with col2:
            st.metric("成交量(万手)", f"{individual_df['成交量'].iloc[-1]/10000:.2f}",
                     f"{(individual_df['成交量'].iloc[-1] - individual_df['成交量'].iloc[-2])/10000:.2f}")
        with col3:
            st.metric("换手率", f"{individual_df['换手率'].iloc[-1]:.2f}%")
        
        # K线图和成交量
        st.divider()
        st.subheader("📈 股票走势图")
        with st.expander("点击查看K线图"):
            fig = make_subplots(rows=2, cols=1, shared_xaxes=True,
                            vertical_spacing=0.03,
                            row_heights=[0.7, 0.3])


            # 添加K线图
            fig.add_trace(go.Candlestick(x=individual_df['日期'],
                                        open=individual_df['开盘'],
                                        high=individual_df['最高'],
                                        low=individual_df['最低'],
                                        close=individual_df['收盘'],
                                        name='K线'), row=1, col=1)

            # 添加成交量柱状图
            colors = ['red' if row['收盘'] >= row['开盘'] else 'green' for _, row in individual_df.iterrows()]
            fig.add_trace(go.Bar(x=individual_df['日期'],
                                y=individual_df['成交量'],
                                name='成交量',
                                marker_color=colors), row=2, col=1)

            # 更新布局
            fig.update_layout(
                title=f'{stock_code} 股票走势图',
                yaxis_title='价格',
                yaxis2_title='成交量',
                xaxis_rangeslider_visible=False,
                height=800
            )

            st.plotly_chart(fig, use_container_width=True)

            # 显示统计数据
            st.subheader("📊 数据表格")
            st.write("详细数据")
            st.dataframe(individual_df.describe())
            st.write("最近交易日数据")
            st.dataframe(individual_df.tail())

            # 下载按钮
            csv = individual_df.to_csv(index=False).encode('utf-8')
            st.download_button(
            label="📥 下载CSV数据",
            data=csv,
            file_name=f'{stock_code}_stock_data.csv',
            mime='text/csv',
        )

        # 添加资金流向分析
        st.subheader("💰 资金流向分析")
        individual_flow_df = get_stock_individual_fund_flow_df(stock_code)
        
        if individual_flow_df is not None and not individual_flow_df.empty:
            # 显示最近的资金流向数据
            st.subheader("最近交易日资金流向")
            st.dataframe(individual_flow_df)
            
            # 创建4列布局
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                st.metric(
                    "当日主力净流入-净额",
                    f"¥{individual_flow_df['主力净流入-净额'].iloc[-1]/10000:.2f}万",
                    f"{individual_flow_df['主力净流入-净占比'].iloc[-1]:.2f}%"
                )
            

            with col2:
                st.metric(
                    "当日超大单净流入-净额",
                    f"¥{individual_flow_df['超大单净流入-净额'].iloc[-1]/10000:.2f}万",
                    f"{individual_flow_df['超大单净流入-净占比'].iloc[-1]:.2f}%"
                )

            

            with col3:
                st.metric(
                    "当日大单净流入-净额",
                    f"¥{individual_flow_df['大单净流入-净额'].iloc[-1]/10000:.2f}万",
                    f"{individual_flow_df['大单净流入-净占比'].iloc[-1]:.2f}%"
                )

            

            with col4:
                st.metric(
                    "当日小单净流入-净额",
                    f"¥{individual_flow_df['小单净流入-净额'].iloc[-1]/10000:.2f}万",
                    f"{individual_flow_df['小单净流入-净占比'].iloc[-1]:.2f}%"
                )

            

            # 添加历史资金流向趋势图
            fig = go.Figure()
            
            # 添加主力净流入趋势线
            fig.add_trace(go.Scatter(
                x=individual_flow_df.index,
                y=individual_flow_df['主力净流入-净额']/10000,
                name='主力净流入(万元)',
                line=dict(color='red')
            ))

            
            # 添加超大单净流入趋势线
            fig.add_trace(go.Scatter(
                x=individual_flow_df.index,
                y=individual_flow_df['超大单净流入-净额']/10000,
                name='超大单净流入(万元)',
                line=dict(color='orange')
            ))

            
            fig.update_layout(
                title='',
                xaxis_title='日期',
                yaxis_title='净流入金额(万元)',
                height=400
            )
            
            st.divider()
            st.subheader("💰 历史资金流向趋势图")
            st.plotly_chart(fig, use_container_width=True)
            
            # 下载按钮
            csv = individual_flow_df.to_csv(index=False).encode('utf-8')

            st.download_button(
                label="📥 下载CSV数据",
                data=csv,
                file_name=f'{stock_code}_individual_flow_data.csv',
                mime='text/csv',
            )
            
        else:
            st.info("暂无个股资金流向数据")


        # 添加龙虎榜数据
        st.subheader("🏆 龙虎榜数据")
        lhb_tab1 = st.tabs(["龙虎榜数据"])[0]
        with lhb_tab1:

            lhb_df = get_stock_lhb_detail(
                start_date=(datetime.date.today() - datetime.timedelta(days=30)).strftime('%Y%m%d'),
                end_date=datetime.date.today().strftime('%Y%m%d')
            )
            
            if not lhb_df.empty:
                st.dataframe(lhb_df)
            else:
                st.info("近期无龙虎榜数据")
    else:
        st.info("请先点击'获取数据'按钮获取股票数据。")
        
    # 分析报告
    tab1 = st.tabs(["股票分析报告"])[0]  # 获取第一个tab
    with tab1:
        if st.button("生成股票分析报告", key="generate_report"):  # 添加唯一的key
            with st.spinner("正在生成股票分析报告..."):
                stock_analysis_report = generate_analysis_report(individual_df,individual_flow_df)
                if stock_analysis_report:
                    st.markdown("📊 分析结果：")
                    st.markdown(stock_analysis_report)
                    # 保存到session_state
                    st.session_state.stock_analysis_report = stock_analysis_report
                    st.success("股票分析报告生成完成！")

except Exception as e:
    st.error(f'获取数据失败: {str(e)}')
