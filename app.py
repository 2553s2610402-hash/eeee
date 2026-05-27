import streamlit as st
import google.generativeai as genai

# 1. 페이지 설정 및 디자인
st.set_page_config(page_title="달콤살벌 연애소", page_icon="💖", layout="centered")

st.title("💖 달콤살벌 연애 챗봇")
st.caption("연애 고민, 짝사랑, 이별 등 말 못 할 고민을 들어드릴게요.")

# 2. API 키 설정 (Streamlit Secrets에서 불러오기)
try:
    # Streamlit Cloud 환경이나 .streamlit/secrets.toml 파일에서 키를 읽어옵니다.
    GOOGLE_API_KEY = st.secrets["GOOGLE_API_KEY"]
    genai.configure(api_key=GOOGLE_API_KEY)
except KeyError:
    st.error("⚠️ API 키를 찾을 수 없습니다. `.streamlit/secrets.toml` 파일이나 Streamlit 설정에 'GOOGLE_API_KEY'를 등록해주세요.")
    st.stop()
except Exception as e:
    st.error(f"⚠️ API 설정 중 오류가 발생했습니다: {e}")
    st.stop()

# 3. 모델 설정 (gemini-2.5-flash-lite)
# 챗봇의 성격(Persona)을 프롬프트 주입(System Instruction)으로 설정합니다.
system_instruction = (
    "당신은 공감 능력이 뛰어나고 위트 있는 전문 연애 상담사입니다. "
    "사용자의 연애 고민에 대해 진정성 있게 공감해주되, 때로는 현실적이고 명쾌한 조언을 제공해야 합니다. "
    "친근한 반말이나 다정한 존댓말을 섞어 부드러운 톤앤매너를 유지하세요. 이모지도 적극적으로 사용해 주세요."
)

try:
    model = genai.GenerativeModel(
        model_name="gemini-2.5-flash-lite",
        system_instruction=system_instruction
    )
except Exception as e:
    st.error(f"⚠️ 모델 로드 중 오류가 발생했습니다: {e}")
    st.stop()

# 4. 세션 상태(Session State)를 활용한 채팅 기록 유지
if "messages" not in st.session_state:
    st.session_state.messages = []
if "chat_session" not in st.session_state:
    # Gemini의 자체 채팅 세션을 초기화합니다.
    st.session_state.chat_session = model.start_chat(history=[])

# 5. 기존 채팅 기록 화면에 표시
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 6. 사용자 입력 처리
if user_input := st.chat_input("연애 고민을 들려주세요... (예: 썸남이 선톡을 안 해ㅠ)"):
    # 6-1. 사용자 메시지 화면에 표시 및 저장
    st.chat_message("user").markdown(user_input)
    st.session_state.messages.append({"role": "user", "content": user_input})

    # 6-2. 챗봇 답변 생성 및 예외 처리
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        
        try:
            with st.spinner("다정한 조언을 생각 중이에요... 💬"):
                # Gemini API 호출
                response = st.session_state.chat_session.send_message(user_input)
                ai_response = response.text
            
            # 답변 화면 표시 및 저장
            message_placeholder.markdown(ai_response)
            st.session_state.messages.append({"role": "assistant", "content": ai_response})
            
        except genai.types.generation_types.BlockedPromptException:
            st.error("⚠️ 부적절하거나 안전 정책에 위배되는 내용이 포함되어 답변을 생성할 수 없습니다.")
        except Exception as e:
            st.error(f"😞 답변을 생성하는 동안 오류가 발생했습니다. 다시 시도해주세요.\n(오류 내용: {e})")
