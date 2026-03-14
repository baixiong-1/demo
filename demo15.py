from dotenv import load_dotenv
from langchain_community.cache import SQLiteCache
from langchain_core.globals import set_llm_cache
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
import streamlit as st

col11, col22,col33 = st.columns([1.2,1,1])
with col22:
    st.write('## 白熊翻译')

# st.write('## 白熊翻译')
language = ['英语', '日语', '德语', '法语','火星文','维吾尔语','藏语']
targets = st.multiselect(label='',placeholder='选择目标语言',options = language)

# col1, col2 = st.columns([5,1])
# with col1:
#     content = st.text_input(label='',placeholder='请输入翻译内容：',label_visibility='collapsed')
# with col2:
#     button = st.button('翻译', type='primary')

content = st.text_input(label='',placeholder='请输入翻译内容：',label_visibility='collapsed')


col1, col2,col3 = st.columns([2.5,1,2.5])
with col2:
    button = st.button('翻译', type='primary',use_container_width=True)


set_llm_cache(SQLiteCache('cache.db'))

# load_dotenv()
llm = ChatOpenAI(
    base_url='https://api.deepseek.com',
    api_key=st.secrets['DEEPSEEK_API_KEY'],#授权密钥，替换成你自己的密钥
    model='deepseek-chat',
    temperature=0.2,
    max_tokens=1024,
)

prompt = ChatPromptTemplate.from_messages([
    ('system','你是一个专业的翻译助手，擅长给出信达雅的翻译。'),
    ('user','请将下面的内容翻译成{target}：\n{content}')
])

chain = prompt | llm

if button:
    if content.strip() and targets:
        with st.spinner('翻译中...', show_time=True):  # type: ignore
            for target in targets:
                msg = chain.invoke({'target': target, 'content': content})
                st.warning(f'{target}:{msg.content}')
    elif content.strip():
        st.write('- **请选择目标语言**')
    elif targets:
        st.write('- **请输入翻译内容**')
    else:
        st.write('- **请输入翻译内容和选择目标语言**')


