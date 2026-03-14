from dotenv import load_dotenv
from langchain_community.cache import SQLiteCache
from langchain_core.globals import set_llm_cache
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
import streamlit as st

st.write('## 白熊翻译')
col1, col2 = st.columns([4, 1])
with col1:
    content = st.text_input(label='',placeholder='请输入翻译内容：',label_visibility='collapsed')
with col2:
    button = st.button('翻译', type='primary')

set_llm_cache(SQLiteCache('cache.db'))
load_dotenv()
llm = ChatOpenAI(
    base_url='https://api.deepseek.com',
    model='deepseek-chat',
    temperature=0.2,
    max_tokens=1024,
)

language = '英文'

prompt = ChatPromptTemplate.from_messages([
    ('system','你是一个专业的翻译助手，擅长给出信达雅的翻译。'),
    ('user','请将下面的内容翻译成{language}：\n{content}')
])

chain = prompt | llm

if button and content.strip():
    for language in ['英语', '日语', '德语', '法语']:
        msg = chain.invoke({'language': language, 'content': content})
        st.warning(f'{language}:{msg.content}')
        # st.write_stream(f'{language}:{msg.content}')

