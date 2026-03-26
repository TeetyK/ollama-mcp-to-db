from dotenv import load_dotenv
import ollama
import streamlit as st
from src.db_tools import read_database , modify_database , tools_schema


load_dotenv()

def app():
    st.set_page_config(page_title="AI DB Agent", page_icon="🗄️")
    st.title("🗄️ AI(Qwen3:4b)")

    SYSTEM_PROMPT = """คุณคือ AI จัดการฐานข้อมูล PostgreSQL คุณมีตารางชื่อ 'users' (id, name, age, email).
    - ห้ามใส่คอลัมน์ id ในคำสั่ง INSERT INTO เด็ดขาด ให้ใส่แค่ name, age, email
    สร้าง SQL ให้ถูกต้องและเรียกใช้ tools ให้เหมาะสม สรุปผลลัพธ์เป็นภาษาไทยที่เข้าใจง่าย"""

    if "messages" not in st.session_state:
        st.session_state.messages = [{"role": "system", "content": SYSTEM_PROMPT}]

    for msg in st.session_state.messages:
        if msg["role"] not in ["system", "tool"]:
            with st.chat_message(msg["role"]):
                st.markdown(msg["content"])

    if prompt := st.chat_input("พิมพ์คำสั่งที่นี่..."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        with st.chat_message("assistant"):
            status_placeholder = st.empty()
            status_placeholder.info("🤖 กำลังวิเคราะห์คำสั่ง...")

            response = ollama.chat(
                model='qwen3:4b',
                messages=st.session_state.messages,
                tools=tools_schema
            )
            message = response['message']
            st.session_state.messages.append(message)

            if message.get('tool_calls'):
                for tool in message['tool_calls']:
                    tool_name = tool['function']['name']
                    arguments = tool['function']['arguments']
                    sql_query = arguments.get('sql_query', '')

                    st.warning(f"🔧 **Tool Called:** `{tool_name}`\n\n**SQL:** `{sql_query}`")

                    if tool_name == 'read_database':
                        result = read_database(sql_query)
                    elif tool_name == 'modify_database':
                        result = modify_database(sql_query)
                    else:
                        result = "Tool not found."
                    
                    with st.expander("ดูผลลัพธ์ดิบจาก Database"):
                        st.code(result, language="json")

                    st.session_state.messages.append({
                        "role": "tool",
                        "content": result,
                        "name": tool_name
                    })

                status_placeholder.info("✍️ กำลังสรุปผล...")
                final_response = ollama.chat(
                    model='qwen3:4b',
                    messages=st.session_state.messages
                )
                status_placeholder.empty()
                st.markdown(final_response['message']['content'])
                st.session_state.messages.append(final_response['message'])
                
            else:
                status_placeholder.empty()
                st.markdown(message['content'])


if __name__ == "__main__":
    app()