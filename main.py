import streamlit as st
from crewai import Agent, Task, Crew, Process
from langchain_openai import ChatOpenAI
import os

# --- 网页标题设置 ---
st.set_page_config(page_title="多智能体自动化运营中枢", layout="wide")
st.title("🤖 多智能体协同运营自动化系统")
st.markdown("---")

# --- 侧边栏：配置 API Key ---
with st.sidebar:
    st.header("配置中心")
    api_key = st.text_input("请输入 API Key", type="password")
    api_base = st.text_input("API Base (可选)", value="https://api.openai.com/v1")
    model_name = st.selectbox("选择模型", ["gpt-4-turbo", "gpt-3.5-turbo", "claude-3-opus"])

# --- 主界面 ---
topic = st.text_input("请输入运营主题", value="银龄智护：智慧养老短视频策划")

if st.button("开始协同工作"):
    if not api_key:
        st.error("请先在侧边栏配置 API Key")
    else:
        # 配置环境
        os.environ["OPENAI_API_KEY"] = api_key
        os.environ["OPENAI_API_BASE"] = api_base
        llm = ChatOpenAI(model=model_name, temperature=0.7)

        with st.status("Agent 正在协同工作中...", expanded=True) as status:
            # 1. 定义 Agent (这里精简了描述，保持核心逻辑)
            coordinator = Agent(
                role='首席运营统筹官',
                goal=f'针对 {topic} 设定 SMART 运营目标',
                backstory='资深团队管理者，擅长规划。',
                llm=llm
            )

            scriptwriter = Agent(
                role='高级视觉编导',
                goal='撰写高规格分镜脚本（要求16:9，ARRI镜头感）',
                backstory='追求电影质感的艺术家。',
                llm=llm
            )

            reviewer = Agent(
                role='视觉品控员',
                goal='审查脚本，剔除盔甲/婚纱，设定蜡笔质感海报提示词',
                backstory='逻辑严密的质检员。',
                llm=llm
            )

            # 2. 定义任务
            t1 = Task(description=f"策划 {topic} 的推广大纲", agent=coordinator, expected_output="大纲文本")
            t2 = Task(description="生成分镜脚本", agent=scriptwriter, expected_output="脚本表格")
            t3 = Task(description="品控审查并输出蜡笔风格 Prompt", agent=reviewer, expected_output="最终方案")

            # 3. 运行
            crew = Crew(agents=[coordinator, scriptwriter, reviewer], tasks=[t1, t2, t3], verbose=True)
            result = crew.kickoff()

            status.update(label="任务完成！", state="complete", expanded=False)

        # 展示结果
        st.subheader("🏆 最终产出成果")
        st.markdown(result)